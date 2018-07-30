import pytest

import api_tests_config
import ssh_tests_config
from steps.github_api_steps import GitHubAPISteps
from utils.ssh_client import SSHClient
from steps.linux_steps import LinuxSteps


@pytest.fixture
def github_api_steps():
    return GitHubAPISteps(host=api_tests_config.HOST,
                          login=api_tests_config.LOGIN,
                          password=api_tests_config.PASSWORD)


@pytest.fixture
def ssh_client():
    return SSHClient(host=ssh_tests_config.HOST,
                     username=ssh_tests_config.USERNAME,
                     password=ssh_tests_config.PASSWORD,
                     key=ssh_tests_config.KEY,
                     passphrase=ssh_tests_config.PASSPHRASE)


@pytest.fixture
def linux_steps():
    return LinuxSteps(host=ssh_tests_config.HOST,
                      username=ssh_tests_config.USERNAME,
                      key=ssh_tests_config.KEY,
                      passphrase=ssh_tests_config.PASSPHRASE,
                      use_key=True,
                      add_system_known_hosts=True)
