#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from lya import AttrDict

logger = logging.getLogger(__name__)


class Config(AttrDict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load(self):
        try:
            self.from_yaml(open('settings.yaml', 'r'))
        except FileNotFoundError as exc:
            message = 'File settings.yaml is missing'
            logger.error(message)
            raise exc
        private_config = {}
        try:
            private_config = AttrDict.from_yaml(open('settings_local.yaml', 'r'))
        except FileNotFoundError:
            logger.warning('File settings_local.yaml is missing')
        self.update_dict(private_config)


config = Config()
config.load()
