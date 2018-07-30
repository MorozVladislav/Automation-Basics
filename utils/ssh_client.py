import logging
import time
from collections import namedtuple

import paramiko

logger = logging.getLogger(__name__)


class SSHClient(object):

    def __init__(self,
                 host=None,
                 username=None,
                 password=None,
                 key=None,
                 passphrase=None,
                 allow_unknown_hosts=False,
                 environment=None):

        self.host = host
        self.username = username
        self.password = password
        self.key = key
        self.passphrase = passphrase
        self.allow_unknown_hosts = allow_unknown_hosts
        self.environment = environment
        self.host_keys = paramiko.HostKeys()
        self.client = paramiko.SSHClient()
        self.host_keys = self.client.get_host_keys()

    def __del__(self):
        self.client.close()
        logger.info('SSH client was closed')

    def add_system_known_hosts(self, path=None):
        self.client.load_system_host_keys(path)

    def clear_host_keys(self):
        self.host_keys.clear()

    def connect(self, use_key=False, *args, **kwargs):

        if self.allow_unknown_hosts:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.username is None:
            message = 'Username is not specified'.format(self.host)
            logger.error(message)
            raise ConnectionFailedException(message)

        try:
            if use_key:
                if self.key is None:
                    message = 'Private key file is not specified'.format(self.host)
                    logger.error(message)
                    raise ConnectionFailedException(message)
                self.client.connect(self.host, username=self.username, key_filename=self.key,
                                    passphrase=self.passphrase, *args, **kwargs)
            else:
                if self.password is None:
                    message = 'Password is not specified'.format(self.host)
                    logger.error(message)
                    raise ConnectionFailedException(message)
                self.client.connect(self.host, username=self.username, password=self.password, *args, **kwargs)

        except paramiko.SSHException:
            message = 'Failed to connect to {}'.format(self.host)
            logger.error(message)
            raise ConnectionFailedException(message)

    def execute(self, command, raise_on_error=False, **kwargs):
        result = namedtuple('result', ['stdout', 'stderr', 'r_code', 'exec_time'])
        start = time.time()
        stdin, stdout, stderr = self.client.exec_command(command.strip('\n'), environment=self.environment, **kwargs)
        result.r_code = stdout.channel.recv_exit_status()

        if raise_on_error and result.r_code != 0:
            message = 'Failed to execute {}'.format(command.strip('\n'))
            logger.error(message)
            raise CommandExecutionException(message)

        result.exec_time = time.time() - start
        result.stdout = ''.join(stdout.readlines())
        result.stderr = ''.join(stderr.readlines())
        logger.info('Command {} executed in {} sec'.format(command.strip('\n'), result.exec_time))
        return result


class SSHClientException(Exception):
    pass


class ConnectionFailedException(SSHClientException):
    pass


class CommandExecutionException(SSHClientException):
    pass
