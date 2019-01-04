#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

import config
from steps.github_api_steps import GitHubAPISteps
from steps.linux_steps import LinuxSteps
from utils.ssh_client import SSHClient

config = config.load()


@pytest.fixture
def github_api_steps():
    return GitHubAPISteps(host=config.github_api.host,
                          login=config.github_api.login,
                          password=config.github_api.password)


@pytest.fixture
def ssh_client():
    return SSHClient(host=config.ssh.host,
                     username=config.ssh.user,
                     password=config.ssh.password,
                     key=config.ssh.key,
                     passphrase=config.ssh.passphrase)


@pytest.fixture
def linux_steps():
    return LinuxSteps(host=config.ssh.host,
                      username=config.ssh.user,
                      key=config.ssh.key,
                      passphrase=config.ssh.passphrase)
