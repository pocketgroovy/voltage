from django.shortcuts import render_to_response
import ConfigParser
from Voltage.settings import CFG_FILE

__author__ = 'yoshi.miyamoto'


def get_properties(err_type, err_code):
    try:
        properties = ConfigParser.RawConfigParser()
        properties.readfp(open(CFG_FILE))

        return properties.get(str(err_type), str(err_code))
    except ConfigParser.NoSectionError:
        raise Exception("Error Type Doesn't Exist")
    except ConfigParser.NoOptionError:
        raise Exception("Error Doesn't Exist")

def throw_error(template, context, obj_dict):
    response = render_to_response(template, obj_dict, context_instance=context)
    response['Error'] = "Client Error"
    return response