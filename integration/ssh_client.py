#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import time
from collections import namedtuple

import paramiko

logger = logging.getLogger(__name__)
CMDResult = namedtuple('CMDResult', ['stdout', 'stderr', 'r_code', 'exec_time'])


class SSHClient(object):

    def __init__(self,
                 host=None,
                 username=None,
                 password=None,
                 key=None,
                 passphrase=None,
                 allow_unknown_hosts=False,
                 environment=None,
                 use_credentials=False):

        self.host = host
        self.username = username
        self.password = password
        self.key = os.path.expanduser(key)
        self.passphrase = passphrase
        self.allow_unknown_hosts = allow_unknown_hosts
        self.environment = environment
        self.client = paramiko.SSHClient()
        self.use_credentials = use_credentials

    def __del__(self):
        self.client.close()
        logger.info('SSH client was closed')

    @property
    def connected(self):
        return False if self.client.get_transport() is None else True

    def load_system_known_hosts(self, path=None):
        host_key_path = os.path.expanduser('~/.ssh/known_hosts') if path is None else path
        self.client.load_host_keys(host_key_path)

    def clear_host_keys(self):
        self.client.get_host_keys().clear()

    def _connect_with_password(self, **kwargs):
        if self.password is None:
            message = 'Password is not specified for {}@{}'.format(self.username, self.host)
            logger.error(message)
            raise SSHConnectionFailed(message)
        self.client.connect(self.host, username=self.username, password=self.password, **kwargs)

    def _connect_with_key(self, **kwargs):
        if self.key is None:
            message = 'Private key is not specified for {}@{}. Attempt to connect using credentials'.format(
                self.username, self.host)
            logger.warning(message)
            raise SSHConnectionFailed(message)
        self.client.connect(self.host, username=self.username, key_filename=self.key, passphrase=self.passphrase,
                            **kwargs)

    def connect(self, use_credentials=None, **kwargs):
        if self.allow_unknown_hosts:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.username is None:
            message = 'Username is not specified for {}'.format(self.host)
            logger.error(message)
            raise SSHConnectionFailed(message)

        force_credentials = self.use_credentials if use_credentials is None else use_credentials

        if force_credentials or self.key is None:
            self._connect_with_password(**kwargs)
        else:
            self._connect_with_key(**kwargs)

    def execute(self, command, raise_on_error=False, **kwargs):
        if not self.connected:
            self.connect()

        logger.info('Executing SSH command: {}'.format(command))
        start = time.time()
        stdin, stdout, stderr = self.client.exec_command(command, environment=self.environment, **kwargs)
        r_code = stdout.channel.recv_exit_status()
        exec_time = time.time() - start
        stdout = ''.join(stdout.readlines())
        stderr = ''.join(stderr.readlines())

        logger.info('Command executed in {} sec\nSTDOUT:\n{}\nSTDERR:\n{}'.format(exec_time, stdout, stderr))
        if raise_on_error and r_code != 0:
            message = 'Command failed, return code {} != 0'.format(r_code)
            logger.error(message)
            raise SSHCommandFailed(message)

        return CMDResult(stdout, stderr, r_code, exec_time)


class SSHClientError(Exception):
    pass


class SSHConnectionFailed(SSHClientError):
    pass


class SSHCommandFailed(SSHClientError):
    pass
