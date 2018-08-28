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
        self.key = key
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
        if path is None:
            self.client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        else:
            self.client.load_host_keys(path)

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
            raise SSHKeyMissing(message)
        if self.passphrase is None:
            message = 'Passphrase is not specified for {}'.format(self.key)
            logger.error(message)
            raise SSHConnectionFailed(message)
        self.client.connect(self.host, username=self.username, key_filename=self.key, passphrase=self.passphrase,
                            **kwargs)

    def connect(self, use_credentials=False, **kwargs):
        if self.allow_unknown_hosts:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.username is None:
            message = 'Username is not specified for {}'.format(self.host)
            logger.error(message)
            raise SSHConnectionFailed(message)

        try:
            if use_credentials:
                self._connect_with_password(**kwargs)
            else:
                try:
                    self._connect_with_key(**kwargs)
                except SSHKeyMissing:
                    self._connect_with_password(**kwargs)

        except paramiko.SSHException:
            message = 'Failed to connect to {}@{}'.format(self.username, self.host)
            logger.error(message)
            raise SSHConnectionFailed(message)

    def execute(self, command, raise_on_error=False, **kwargs):
        if not self.connected:
            self.connect(self.use_credentials)

        logger.info('Executing: {}'.format(command))
        start = time.time()
        stdin, stdout, stderr = self.client.exec_command(command, environment=self.environment, **kwargs)
        r_code = stdout.channel.recv_exit_status()
        exec_time = time.time() - start
        stdout = ''.join(stdout.readlines())
        stderr = ''.join(stderr.readlines())

        stdout_log = ''.join(list(line + '\n\t\t' for line in stdout.splitlines())).strip('\n\t\t')
        stderr_log = ''.join(list(line + '\n\t\t' for line in stderr.splitlines())).strip('\n\t\t')
        logger.info('Command executed in {} sec\n\tSTDOUT: {}\n\tSTDERR: {}'.format(exec_time, stdout_log, stderr_log))
        if raise_on_error and r_code != 0:
            message = 'Command failed. Status code: {}'.format(r_code)
            logger.error(message)
            raise SSHCommandFailed(message)

        return CMDResult(stdout, stderr, r_code, exec_time)


class SSHClientError(Exception):
    pass


class SSHConnectionFailed(SSHClientError):
    pass


class SSHCommandFailed(SSHClientError):
    pass


class SSHKeyMissing(SSHClientError):
    pass
