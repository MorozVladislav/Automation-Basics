#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from lya import AttrDict

CONFIG = 'settings.yaml'
LOCAL_CONFIG = 'settings_local.yaml'


def load():
    with open(os.path.expanduser(CONFIG), 'r') as cfg:
        config = AttrDict.from_yaml(cfg)
    local_config_path = os.path.expanduser(LOCAL_CONFIG)
    if os.path.isfile(local_config_path):
        with open(local_config_path, 'r') as cfg:
            local_config = AttrDict.from_yaml(cfg)
            config.update_dict(local_config)
    return config
