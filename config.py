#!/usr/bin/env python3
# -*- coding: ascii -*-
import os


class API:
    HOST = 'https://api.github.com/'
    LOGIN = os.environ['GITHUB_USER']
    PASSWORD = os.environ['GITHUB_PSWD']
    CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
    CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
    REPO_NAME = 'test-repo'
    REPO_DESCRIPTION = 'Just a test repo'


class SSH:
    HOST = '192.168.56.101'
    USERNAME = os.environ['SSH_USER']
    PASSWORD = os.environ['SSH_PSWD']
    KEY = os.environ['SSH_KEY']
    PASSPHRASE = os.environ['SSH_PASSPHRASE']
