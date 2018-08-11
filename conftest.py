#!/usr/bin/env python3
# -*- coding: ascii -*-
import pytest

import config
from steps.github_api_steps import GitHubAPISteps
from utils.ssh_client import SSHClient
from steps.linux_steps import LinuxSteps


@pytest.fixture
def github_api_steps():
    return GitHubAPISteps(host=config.API.HOST,
                          login=config.API.LOGIN,
                          password=config.API.PASSWORD)


@pytest.fixture
def ssh_client():
    return SSHClient(host=config.SSH.HOST,
                     username=config.SSH.USERNAME,
                     password=config.SSH.PASSWORD,
                     key=config.SSH.KEY,
                     passphrase=config.SSH.PASSPHRASE)


@pytest.fixture
def linux_steps():
    return LinuxSteps(host=config.SSH.HOST,
                      username=config.SSH.USERNAME,
                      key=config.SSH.KEY,
                      passphrase=config.SSH.PASSPHRASE,
                      add_system_known_hosts=True)
