#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.ssh_client import SSHClient


class LinuxSteps(SSHClient):

    def __init__(self,
                 host=None,
                 username=None,
                 password=None,
                 key=None,
                 passphrase=None,
                 load_system_known_hosts=True,
                 **kwargs):

        super().__init__(host, username, password, key, passphrase, **kwargs)
        if load_system_known_hosts:
            self.load_system_known_hosts()

    @staticmethod
    def create_signature(head, options_map=(), options=()):
        signature = [head]
        for option, is_exist in options_map:
            if is_exist:
                signature.append(option)
        signature.extend(options)
        return ' '.join(signature)

    def step(self, command, cd=None, **kwargs):
        cmd = 'cd {}; {}'.format(cd, command) if cd is not None else command
        return self.execute(cmd, **kwargs)

    def mkdir(self,
              path,
              mode=None,
              parents=False,
              verbose=False,
              options=None,
              **kwargs):
        options_map = (
            ('--mode={}'.format(mode), mode),
            ('-p', parents),
            ('-v', verbose),
            (path, True),
        )
        cmd = self.create_signature('mkdir', options_map, options)
        return self.step(cmd, **kwargs)

    def rm(self,
           path,
           force=True,
           recursive=False,
           options=None,
           **kwargs):
        options_map = (
            ('-f', force),
            ('-r', recursive),
            (path, True),
        )
        cmd = self.create_signature('rm', options_map, options)
        return self.step(cmd, **kwargs)

    def ls(self,
           path='',
           show_all=False,
           long_listing_format=False,
           options=None,
           **kwargs):
        options_map = (
            ('-a', show_all),
            ('-l', long_listing_format),
            (path, True),
        )
        cmd = self.create_signature('ls', options_map, options)
        return self.step(cmd, **kwargs)

    def cp(self,
           source,
           destination='',
           force=False,
           recursive=False,
           options=None,
           **kwargs):
        options_map = (
            ('-f', force),
            ('-r', recursive),
            (source, True),
            (destination, True),
        )
        cmd = self.create_signature('cp', options_map, options)
        return self.step(cmd, **kwargs)

    def mv(self,
           source,
           directory='',
           force=False,
           update=False,
           options=None,
           **kwargs):
        options_map = (
            ('-f', force),
            ('-u', update),
            (source, True),
            (directory, True),
        )
        cmd = self.create_signature('mv', options_map, options)
        return self.step(cmd, **kwargs)

    def date(self,
             set_time=None,
             universal=False,
             date_format='',
             options=None,
             **kwargs):
        options_map = (
            ('--set={}'.format(set_time), set_time),
            ('-u', universal),
            ('+"{}"'.format(date_format), True),
        )
        cmd = self.create_signature('date', options_map, options)
        return self.step(cmd, **kwargs)
