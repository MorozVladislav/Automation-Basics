#!/usr/bin/env python3
# -*- coding: ascii -*-
import time

from utils.ssh_client import SSHClientError, SSHConnectionFailed


class TestSSH(object):

    def test_connection_to_unknown_host(self, ssh_client):
        try:
            ssh_client.connect(use_credentials=True)
        except SSHClientError as exc:
            exc_type = type(exc)
        finally:
            assert exc_type == SSHConnectionFailed

    def test_connection_allowing_unknown_hosts(self, ssh_client):
        ssh_client.allow_unknown_hosts = True
        ssh_client.connect(use_credentials=True)

    def test_connection_to_system_known_host(self, ssh_client):
        ssh_client.add_system_known_hosts()
        ssh_client.connect(use_credentials=True)

    def test_delete_known_hosts(self, ssh_client):
        ssh_client.add_system_known_hosts()
        ssh_client.connect(use_credentials=True)
        ssh_client.clear_host_keys()
        try:
            ssh_client.connect(use_credentials=True)
        except SSHClientError as exc:
            exc_type = type(exc)
        finally:
            assert exc_type == SSHConnectionFailed

    def test_execute_command(self, ssh_client):
        ssh_client.add_system_known_hosts()
        assert 'INTEL' in ssh_client.execute("grep 'AGP' /boot/config-3.10.0-862.6.3.el7.x86_64",
                                             raise_on_error=True).stdout

    def test_cd_and_ls(self, linux_steps):
        file = 'config-3.10.0-862.6.3.el7.x86_64'
        result = linux_steps.script(
            linux_steps.cd('/boot/', get_signature=True),
            ';',
            linux_steps.ls(long_listing_format=True, get_signature=True),
            raise_on_error=True
        )
        assert file in result.stdout

    def test_mkdir_and_rm(self, linux_steps):
        linux_steps.mkdir('~/test_dir', raise_on_error=True)
        assert 'test_dir' in linux_steps.ls('~/', raise_on_error=True).stdout
        linux_steps.rm('~/test_dir', recursive=True, raise_on_error=True)
        assert 'test_dir' not in linux_steps.ls('~/', raise_on_error=True).stdout

    def test_cp(self, linux_steps):
        linux_steps.mkdir('~/test_dir', raise_on_error=True)
        linux_steps.cp('~/test_dir', '/', recursive=True, raise_on_error=True)
        assert 'test_dir' in linux_steps.ls('/', raise_on_error=True).stdout
        linux_steps.rm('~/test_dir', recursive=True, raise_on_error=True)
        linux_steps.rm('/test_dir', recursive=True, raise_on_error=True)
        assert 'test_dir' not in linux_steps.ls('~/', raise_on_error=True).stdout
        assert 'test_dir' not in linux_steps.ls('/', raise_on_error=True).stdout

    def test_mv(self, linux_steps):
        linux_steps.mkdir('~/test_dir', raise_on_error=True)
        linux_steps.mv('~/test_dir', '~/new_dir', raise_on_error=True)
        assert 'test_dir' not in linux_steps.ls('~/', raise_on_error=True).stdout
        assert 'new_dir' in linux_steps.ls('~/', raise_on_error=True).stdout
        linux_steps.rm('~/new_dir', recursive=True, raise_on_error=True)
        assert 'new_dir' not in linux_steps.ls('~/', raise_on_error=True).stdout

    def test_date(self, linux_steps):
        assert linux_steps.date(date_format='%H:%M').stdout.strip('\n') == time.strftime('%H:%M')
