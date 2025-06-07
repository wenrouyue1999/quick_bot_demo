#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午6:51
# @Author  : wenrouyue
# @File    : config.py
import os
import yaml


def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.yaml')

    with open(config_path, 'r') as file:
        yaml_config = yaml.safe_load(file)

    env = yaml_config.get('environment', 'dev')
    env_config_file = os.path.join(base_dir, f'config_{env}.yaml')

    with open(env_config_file, 'r', encoding='utf-8') as file:
        env_config = yaml.safe_load(file)

    yaml_config.update(env_config)
    return yaml_config
