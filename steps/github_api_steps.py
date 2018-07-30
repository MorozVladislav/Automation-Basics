import logging
import time
from functools import wraps

from requests.auth import HTTPBasicAuth

from utils.http_client import HttpClient

logger = logging.getLogger(__name__)


def credentials_checkup(func):
    @wraps(func)
    def wrapped(obj, *args, **kwargs):
        if obj.login is None or obj.password is None:
            logger.error('Credentials are not specified')
            raise AuthorizationError
        return func(obj, *args, **kwargs)
    return wrapped


def token_checkup(func):
    @wraps(func)
    def wrapped(obj, *args, **kwargs):
        if obj.use_token and obj.token is None:
            logger.error('Token is empty')
            raise AuthorizationError
        return func(obj, *args, **kwargs)
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
            self.get_username()
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
    def get_token(self, scopes):
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
        self._username = self.authorised_request('GET', 'user', expected_code=200, **kwargs).json()['login']
        return self._username

    def get_repos(self, **kwargs):
        return self.authorised_request('GET', 'user/repos', expected_code=200, **kwargs)

    def get_user_repos(self, username, **kwargs):
        return self.authorised_request('GET', 'users/{}/repos'.format(username), expected_code=200, **kwargs)

    def create_repo(self, name, repo_properties={}, **kwargs):
        body = {'name': name}
        body.update(repo_properties)
        return self.authorised_request('POST', 'user/repos', json=body, expected_code=201, **kwargs)

    def delete_repo(self, name, wait_for_deletion=True, **kwargs):
        resp = self.authorised_request(
            'DELETE', 'repos/{}/{}'.format(self.username, name), expected_code=204, **kwargs)
        if wait_for_deletion:
            self.wait_for_repo_deletion(name)
        return resp

    def wait_for_repo_deletion(self, name, repo_delete_timeout=5, repo_delete_sleep=0.5):
        del_time = time.time()
        params = {'type': 'owner'}
        while time.time() - del_time < repo_delete_timeout:
            if name not in self.get_repos(params=params).json():
                return True
            else:
                time.sleep(repo_delete_sleep)
        message = 'Failed to delete repository within {} sec'.format(repo_delete_timeout)
        logger.error(message)
        raise DeletionError(message)

    def edit_repo(self, name, repo_properties={}, **kwargs):
        body = {'name': name}
        body.update(repo_properties)
        return self.authorised_request('PATCH', 'repos/{}/{}'.format(self.username, name), json=body,
                                       expected_code=200, **kwargs)

    def get_repo_topics(self, repo_name, username=None, **kwargs):
        if username is None:
            return self.authorised_request('GET', 'repos/{}/{}/topics'.format(self.username, repo_name),
                                           expected_code=200, **kwargs)
        else:
            return self.authorised_request('GET', 'repos/{}/{}/topics'.format(username, repo_name),
                                           expected_code=200, **kwargs)


class APIStepsError(Exception):
    pass


class AuthorizationError(APIStepsError):
    pass


class DeletionError(APIStepsError):
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
