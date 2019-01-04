#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
from functools import wraps

from requests.auth import HTTPBasicAuth

from utils.http_client import HttpClient

logger = logging.getLogger(__name__)


def credentials_checkup(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if self.login is None or self.password is None:
            logger.error('Credentials are not specified')
            raise AuthorizationError
        return func(self, *args, **kwargs)
    return wrapped


def token_checkup(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if self.use_token and self.token is None:
            logger.error('Token is empty')
            raise AuthorizationError
        return func(self, *args, **kwargs)
    return wrapped


class GitHubAPISteps(HttpClient):

    def __init__(self, login=None, password=None, token=None, use_token=False, **kwargs):
        super().__init__(**kwargs)
        self.login = login
        self.password = password
        self.token = token
        self.use_token = use_token
        self.authorization_id = None
        self._username = None

    @property
    def username(self):
        if self._username is None:
            self._username = self.get_username()
        return self._username

    @credentials_checkup
    @token_checkup
    def authorised_request(self, method, url, **kwargs):
        if self.use_token:
            auth = OAuthToken(self.token)
        else:
            auth = HTTPBasicAuth(self.login, self.password)
        return self.request(method, url, auth=auth, **kwargs)

    @credentials_checkup
    def get_token(self, scopes=None):
        if scopes is None:
            scopes = ['public_repo', ]
        auth = HTTPBasicAuth(self.login, self.password)
        body = {
            'scopes': scopes,
            'note': '{} script'.format(__name__)
        }
        resp = self.post('authorizations', auth=auth, json=body, expected_code=201).json()
        self.authorization_id = resp['id']
        self.token = resp['token']
        return self.token

    @credentials_checkup
    def delete_token(self, **kwargs):
        if self.token is None:
            logger.warning('Token is already empty')
            return

        self.use_token = False
        self.token = None
        auth = HTTPBasicAuth(self.login, self.password)
        return self.delete('authorizations/{}'.format(self.authorization_id), auth=auth, expected_code=204, **kwargs)

    def get_username(self, **kwargs):
        return self.authorised_request(self.GET, 'user', expected_code=200, **kwargs).json()['login']

    def get_repos(self, **kwargs):
        return self.authorised_request(self.GET, 'user/repos', expected_code=200, **kwargs)

    def get_user_repos(self, username, **kwargs):
        return self.authorised_request(self.GET, 'users/{}/repos'.format(username), expected_code=200, **kwargs)

    def create_repo(self, name, repo_properties=None, **kwargs):
        if repo_properties is None:
            repo_properties = {}
        body = {'name': name}
        body.update(repo_properties)
        return self.authorised_request(self.POST, 'user/repos', json=body, expected_code=201, **kwargs)

    def delete_repo(self, name, wait_for_deletion=True, **kwargs):
        resp = self.authorised_request(
            self.DELETE, 'repos/{}/{}'.format(self.username, name), expected_code=204, **kwargs)
        if wait_for_deletion:
            self.wait_for_repo_deletion(name)
        return resp

    def wait_for_repo_deletion(self, name, delete_timeout=5, interval=0.5):
        start = time.time()
        params = {'type': 'owner'}
        while time.time() - start < delete_timeout:
            if name not in self.get_repos(params=params).json():
                return True
            else:
                time.sleep(interval)
        message = 'Failed to delete repository within {} sec'.format(delete_timeout)
        logger.error(message)
        raise RepoDeletionTimeout(message)

    def edit_repo(self, name, repo_properties=None, **kwargs):
        if repo_properties is None:
            repo_properties = {}
        body = {'name': name}
        body.update(repo_properties)
        return self.authorised_request(self.PATCH, 'repos/{}/{}'.format(self.username, name), json=body,
                                       expected_code=200, **kwargs)

    def get_repo_topics(self, repo_name, username=None, **kwargs):
        user = username if username is not None else self.username
        return self.authorised_request(self.GET, 'repos/{}/{}/topics'.format(user, repo_name),
                                       expected_code=200, **kwargs)


class GitHubAPIStepsError(Exception):
    pass


class AuthorizationError(GitHubAPIStepsError):
    pass


class RepoDeletionTimeout(GitHubAPIStepsError):
    pass


class OAuthToken(object):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'token {}'.format(self.token)
        return r

    def __eq__(self, other):
        return self.token == getattr(other, 'token', None)

    def __ne__(self, other):
        return not self == other
