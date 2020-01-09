#!/usr/bin/env python
"""
This script provides useful funcs to all other scripts
"""
import yaml
import os


def read_config():
    # Read in config file
    config = {k: v for d in yaml.load(
        open('config.yaml'),
             Loader=yaml.SafeLoader) for k, v in d.items()}
    return config
