#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from lya import AttrDict

CONFIG = 'settings.yaml'
CONFIG_LOCAL = 'settings_local.yaml'


def load_config():
    with open(CONFIG, 'r') as cfg_file:
        cfg = AttrDict.from_yaml(cfg_file)

    if os.path.exists(CONFIG_LOCAL):
        with open(CONFIG_LOCAL, 'r') as cfg_local_file:
            cfg_local = AttrDict.from_yaml(cfg_local_file)
            cfg.update_dict(cfg_local)

    return cfg


config = load_config()
