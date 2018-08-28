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
    def create_signature(command, options_map, options):
        signature = [command]
        for option in options_map:
            if not options_map[option]:
                continue
            else:
                signature.append(option)
        if options is not None:
            for option in options:
                signature.append(option)
        return ' '.join(signature)

    def step(self, signature, cd=None, **kwargs):
        if cd is not None:
            return self.execute('cd {}; {}'.format(cd, signature), **kwargs)
        else:
            return self.execute(signature, **kwargs)

    def mkdir(self,
              path,
              mode=None,
              parents=False,
              verbose=False,
              options=None,
              **kwargs):
        options_map = {
            '--mode={}'.format(mode): mode,
            '-p': parents,
            '-v': verbose,
            path: True
        }
        return self.step(self.create_signature('mkdir', options_map, options), **kwargs)

    def rm(self,
           path,
           force=True,
           recursive=False,
           options=None,
           **kwargs):
        options_map = {
            '-f': force,
            '-r': recursive,
            path: True
        }
        return self.step(self.create_signature('rm', options_map, options), **kwargs)

    def ls(self,
           path='',
           show_all=False,
           long_listing_format=False,
           options=None,
           **kwargs):
        options_map = {
            '-a': show_all,
            '-l': long_listing_format,
            path: True
        }
        return self.step(self.create_signature('ls', options_map, options), **kwargs)

    def cp(self,
           source,
           destination='',
           force=False,
           recursive=False,
           options=None,
           **kwargs):
        options_map = {
            '-f': force,
            '-r': recursive,
            source: True,
            destination: True
        }
        return self.step(self.create_signature('cp', options_map, options), **kwargs)

    def mv(self,
           source,
           directory='',
           force=False,
           update=False,
           options=None,
           **kwargs):
        options_map = {
            '-f': force,
            '-u': update,
            source: True,
            directory: True
        }
        return self.step(self.create_signature('mv', options_map, options), **kwargs)

    def date(self,
             set_time=None,
             universal=False,
             date_format='',
             options=None,
             **kwargs):
        options_map = {
            '--set={}'.format(set_time): set_time,
            '-u': universal,
            '+"{}"'.format(date_format): True
        }
        return self.step(self.create_signature('date', options_map, options), **kwargs)
