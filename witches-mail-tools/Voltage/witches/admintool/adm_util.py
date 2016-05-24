from django.shortcuts import render_to_response
import ConfigParser
from Voltage.settings import CFG_FILE
from witches.models import WUsers

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


def get_user_id_from_phone_id(phone_id):
    other = 'get_user_id_from_phone_id'
    sanitized_phone_id = remove_extra_space(phone_id)
    user_id = WUsers.objects.filter(phone_id=sanitized_phone_id)
    if user_id and len(user_id) == 1:
        return user_id[0].id
    else:
        error = get_properties(err_type="Error", err_code="ERR0042")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        raise Exception(res_dict)


def remove_extra_space(phone_id):
    sanitized = phone_id.replace(" ", "")
    return sanitized
