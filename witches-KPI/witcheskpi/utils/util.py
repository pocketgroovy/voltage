from witches.settings import CFG_FILE
from witcheskpi import const, views

__author__ = 'yoshi.miyamoto'

import ConfigParser


def get_properties(err_type, err_code):
    try:
        properties = ConfigParser.RawConfigParser()
        properties.readfp(open(CFG_FILE))

        return properties.get(str(err_type), str(err_code))
    except ConfigParser.NoSectionError:
        raise Exception("Error Type Doesn't Exist")
    except ConfigParser.NoOptionError:
        raise Exception("Error Doesn't Exist")


def get_device(shop_type):
    devices = {const.shop_type_apple: const.device_type_apple,
               const.shop_type_google: const.device_type_ggl,
               const.shop_type_amazon: const.device_type_amazon,
               const.shop_type_all: const.device_type_all}
    return devices[shop_type]
