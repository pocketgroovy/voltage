from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core import serializers
from django.core.files import File
from random import randint
from datetime import date, datetime
from Voltage.settings import CFG_FILE, MEDIA_ROOT
import datetime as dt
import os
import xlwt
import json
import ConfigParser


import logging
from witches import const
from witches.utils.custom_exceptions import WrongValueError

logger = logging.getLogger(__name__)


def serialize_to_json(object):
    ret_object = serializers.serialize('json', object)
    ret_object = json.loads(ret_object)
    return json.dumps(ret_object, indent=4, sort_keys=True, separators=(',', ': '))


def get_properties(err_type, err_code):
    try:
        properties = ConfigParser.RawConfigParser()
        properties.readfp(open(CFG_FILE))

        return properties.get(str(err_type), str(err_code))
    except ConfigParser.NoSectionError:
        raise Exception("Error Type Doesn't Exist")
    except ConfigParser.NoOptionError:
        raise Exception("Error Doesn't Exist")


def debug_log(res_dict, phone_id):
    logger.debug(str(res_dict) + "[" + phone_id + "]; ")

def error_log(message, phone_id, function):
    logger.debug('FUNCTION: \"' + function + '\":' + str(message) + "[" + phone_id + "]")


def throw_error(template, context, obj_dict):
    response = render_to_response(template, obj_dict, context_instance=context)
    response['Error'] = "Client Error"
    return response


def purchase_error_message(function, user_currency, item_id, quantity, item_price, prev_value='see <user currency>', note='NA'):
    error = "FUNCTION: \"" + function + "\", <USER CURRENCY>:" + str(user_currency) + ", not enough for item: " + \
    item_id + " <QUANTITY>:" + str(quantity) + ", <ITEM PRICE>:" + str(item_price) + ", note:" + note
    return error


def sync_resource_error_message(function, type, req_currency, currency):
    error = 'FUNCTION: \"' + function + '\", requested ' + type + '[' + str(req_currency) +'] was more than the user has in database[' \
            + str(currency) + ']'
    return error


def sync_resource_error_message_max(function, type, req_currency, max):
    error = 'FUNCTION: \"' + function + '\", requested ' + type + '[' + str(req_currency) +'] was over max[' + str(max) + ']'
    return error


def log_out_of_sync_error(message, phone_id):
    logger.debug('OUT_OF_SYNC: user' + "[" + phone_id + "]; " + message)


def throw_error_in_json_response(error, other, phone_id='system_temp_phone_id'):
    res_dict = {'status': 'failed', 'function': other, 'Error': str(error)}
    log_error_without_response(res_dict, phone_id)
    return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')


def throw_error_in_json(res_dict, phone_id):
    log_error_without_response(res_dict, phone_id)
    return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')


def log_error_without_response(res_dict, phone_id):
    logger.debug(str(res_dict) + "[" + phone_id + "]; ")


def openfile(fileName, mode, context):
    try:
        fileHandler = open(name=fileName, mode=mode)
        return {'opened': True, 'handler': fileHandler}
    except IOError:
        context['message'] += get_properties('Error', 'ERR0008') + fileName + '\n'
    except:
        context['message'] += get_properties('Error', 'ERR0009')
    return {'opened': False, 'handler': None}


def writefile_json(content, fileName, context):
    filehandler = openfile(fileName, 'w', context)

    if filehandler['opened']:
        file = File(filehandler['handler'])
        file.write(json.dumps(content))
        file.flush()
        file.close()


def writeToSheet(sheet, fieldname, valuelist):
    datetimeStyle = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm:ss')
    dateStyle = xlwt.easyxf(num_format_str='dd/mm/yyyy')

    for col, val in enumerate(fieldname):
        sheet.write(0, col, val.name)

    for row, rowdata in enumerate(valuelist, start=1):
        for col, val in enumerate(rowdata):
            if isinstance(rowdata[fieldname[col].name], datetime):
                style = datetimeStyle
            elif isinstance(rowdata[fieldname[col].name], date):
                style = dateStyle
            elif isinstance(rowdata[fieldname[col].name], bool):
                if rowdata[fieldname[col].name] is False:
                    rowdata[fieldname[col].name] = 0
                elif rowdata[fieldname[col].name] is True:
                    rowdata[fieldname[col].name] = 1
            else:
                style = xlwt.XFStyle()
            sheet.write(row, col, str(rowdata[fieldname[col].name]), style=style)

    return sheet


def readfile(fileName, context):
    filehandler = openfile(fileName, 'r', context)

    if filehandler['opened']:
        file = File(filehandler['handler'])
        content = ''

        for chunk in file.chunks(10):
            content += chunk

        file.close()

        return content


def randomfilename(prefix, type):
    FILES = MEDIA_ROOT
    #FILES = 'witches'

    if not os.path.exists(FILES):
        os.makedirs(FILES)

    td = (datetime.now()-datetime(1970, 1, 1)).total_seconds()
    td = int(td)
    if prefix:
        filename = prefix + "_" + str(td) + "_" + str(randint(1, 10000)) + '.' + type
    else:
        filename = str(td) + "_" + str(randint(1, 10000)) + '.' + type
    return os.path.join(FILES, filename)


def stringToBool(str):
    return str[0].upper() == 'T'


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def get_time_diff_in_seconds(last_update, current_time):
    time_diff = current_time - last_update

    if time_diff.days > 0:
        time_diff_in_seconds = get_date_in_seconds(time_diff)  # total seconds will be resulted from addition of the days and seconds
    elif time_diff.days < 0:
        time_diff_in_seconds = -1
    else:
        time_diff_in_seconds = time_diff.seconds

    return time_diff_in_seconds


def get_date_in_seconds(time):
    return ((time.days * 24) * const.seconds_in_hour) + time.seconds


def get_max_seconds(max_value, refresh_rate):
    return max_value * refresh_rate


def get_total_seconds_for_update(update_count, refresh_rate_in_seconds):
    return update_count * refresh_rate_in_seconds


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# sanitize float to int and also string float to int. not to be used with alphanumeric
def get_sanitized_int(value, table_name, column_name):
    if not is_int(value):
        if not value.isalnum():
            sanitized_int = get_num_before_decimal_point(value)
            logger.debug(str(value) + ' was string and sanitized to actual int')
        else:
            raise WrongValueError('wrong value: ' + value + ' in column[' + column_name + '] in table[' + table_name + ']')
    else:
        sanitized_int = value
    return int(sanitized_int)


def get_sanitized_string_int(value):
    if not is_int(value):
        if value.isalnum():
            sanitized_value = value
        else:
            if '[' in value or '{' in value:
                sanitized_value = value
            else:
                sanitized_value = get_num_before_decimal_point(value)
    else:
        sanitized_value = int(value)
    return str(sanitized_value)


def sanitize_scene_path(scene_path):
    name_length = len(scene_path)
    if scene_path[name_length - 1] == ' ':
        cleaned_scene_path = scene_path[:name_length - 1]
    else:
        cleaned_scene_path = scene_path
    return cleaned_scene_path

def get_num_before_decimal_point(value):
    before_dec_pt = value.split('.')
    num_before_dec_pt = before_dec_pt[0]
    return num_before_dec_pt

def remove_under_decimal(value):
    number = value.split('.')
    return number[0]

def convert_seconds_to_datetime(seconds):
    s = seconds / 1000.0
    date_time = dt.datetime.utcfromtimestamp(s)
    return date_time

def convert_datetime_to_seconds(datetime_obj):
    seconds = (datetime_obj-dt.datetime(1970,1,1)).total_seconds()
    return int(seconds)

def convert_utc_to_pst(utc):
    pst = utc - dt.timedelta(seconds=25200)
    return pst

def get_now_datetime():
    now = datetime.utcnow()
    return now

def get_next_update_delta(type, current_time_in_sec, last_update_time_in_sec, other, context, type_res):
    refresh_rate_in_sec = get_refresh_rate_in_sec(type, other, context, type_res)
    update_delta_in_sec = refresh_rate_in_sec - (int(current_time_in_sec) - int(last_update_time_in_sec))
    return update_delta_in_sec


def get_refresh_rate_in_sec(type, other, context, type_res):
    from witches.master import get_stamina_refresh_rate_from_db

    if type == 'stamina':
        refresh_rate_in_min = get_stamina_refresh_rate_from_db(other, context, type_res)

    refresh_rate_in_sec = int(refresh_rate_in_min.value) * 60
    return refresh_rate_in_sec

def get_current_time_from_request(request):
    try:
        current_time = request.POST['current_time']
    except Exception as e:
        # logger.debug("current time is set to 0")
        current_time = 0
    return current_time

def get_story_reset_flag_from_request(request):
    try:
        is_story_reset = request.POST['story_reset']
    except Exception as e:
        # logger.debug("story reset flag is set to false: ")
        is_story_reset = False
    return is_story_reset

def get_login_bonus_flag_from_request(request):
    try:
        bonus_ineligible = request.POST['bonus_ineligible']
    except Exception as e:
        # logger.debug("story reset flag is set to false: ")
        bonus_ineligible = False
    return bonus_ineligible

