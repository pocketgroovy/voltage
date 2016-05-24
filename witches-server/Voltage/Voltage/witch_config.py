__author__ = 'yoshi.miyamoto'

import os

# get environment settings
from ConfigParser import RawConfigParser
config = RawConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'configs/settings.cfg').replace('\\', '/')

if(not os.path.exists(config_file)):
    raise Exception("No local configuration ('settings.cfg') found for settings.py")

config.read(config_file)


def get_environment(environment, target):
    return config.get(environment, target)
