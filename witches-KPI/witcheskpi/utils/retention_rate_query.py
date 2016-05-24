__author__ = 'yoshi.miyamoto'

import datetime
from witcheskpi.models import UserLoginHistory
from witcheskpi.utils.date_util import add_twentyfour_hours_minus_a_second, add_twentyfour_hours, add_3_days, \
    add_7_days, add_14_days, add_30_days
from witcheskpi.utils.users_query import get_installed_users
import logging
logger = logging.getLogger(__name__)

now = datetime.datetime.utcnow().replace(tzinfo=None)


def get_loggedin_users_phone_id(startDate, endDate, device_type):
    if device_type == 'ALL':
        logged_in_users = UserLoginHistory.objects.filter(install_date__gte=startDate, install_date__lte=endDate,
                                                          delete_flag=False).distinct('phone_id')
    else:
        logged_in_users = UserLoginHistory.objects.filter(install_date__gte=startDate, install_date__lte=endDate,
                                                          device=device_type, delete_flag=False).distinct('phone_id')
    return logged_in_users


def get_returned_users_num(selected_date, end_of_day, logged_in_users_phone_id, device_type):
        counter = 0
        installed_on_selected_date = get_installed_users(selected_date, end_of_day, device_type)
        for user_phone_id in logged_in_users_phone_id:
            for install in installed_on_selected_date:
                if install.phone_id == user_phone_id:
                    counter += 1
        return counter


def calculate_retention_rate(selected_date, logged_in_users_ids, device_type):
    rate = 0
    end_of_day = add_twentyfour_hours_minus_a_second(selected_date)
    installed_on_selected_date = get_installed_users(selected_date, end_of_day, device_type)
    returned_users_num = get_returned_users_num(selected_date, end_of_day, logged_in_users_ids, device_type)
    if installed_on_selected_date.__len__() > 0:
        rate = (float(returned_users_num) / installed_on_selected_date.__len__()) * 100
    return rate


def get_retention_rate_day1(selected_date, device_type):
    next_day = add_twentyfour_hours(selected_date)
    end_of_next_day = add_twentyfour_hours_minus_a_second(next_day)
    logged_in_next_day_users_ids = get_loggedin_users_phone_id(next_day, end_of_next_day, device_type)
    retention_rate_in_float = 0
    if logged_in_next_day_users_ids.__len__() > 0:
        retention_rate = calculate_retention_rate(selected_date, logged_in_next_day_users_ids, device_type)
        retention_rate_in_float = "%.1f" % retention_rate
    return float(retention_rate_in_float)


def get_retention_rate_day3(selected_date, device_type):
    three_days_later = add_3_days(selected_date)
    end_of_three_days = add_twentyfour_hours_minus_a_second(three_days_later)
    logged_in_3_days_later_users_ids = get_loggedin_users_phone_id(three_days_later, end_of_three_days, device_type)
    retention_rate_in_float = 0
    if logged_in_3_days_later_users_ids.__len__() > 0:
        retention_rate = calculate_retention_rate(selected_date, logged_in_3_days_later_users_ids, device_type)
        retention_rate_in_float = "%.1f" % retention_rate

    return float(retention_rate_in_float)


def get_retention_rate_day7(selected_date, device_type):
    seven_days_later = add_7_days(selected_date)
    end_of_seven_days = add_twentyfour_hours_minus_a_second(seven_days_later)
    logged_in_7days_later_users_ids = get_loggedin_users_phone_id(seven_days_later, end_of_seven_days, device_type)
    retention_rate_in_float = 0
    if logged_in_7days_later_users_ids.__len__() > 0:
        retention_rate = calculate_retention_rate(selected_date, logged_in_7days_later_users_ids, device_type)
        retention_rate_in_float = "%.1f" % retention_rate

    return float(retention_rate_in_float)


def get_retention_rate_day14(selected_date, device_type):
    fourteen_days_later = add_14_days(selected_date)
    end_of_fourteen_days = add_twentyfour_hours_minus_a_second(fourteen_days_later)
    logged_in_14days_later_users_ids = get_loggedin_users_phone_id(fourteen_days_later, end_of_fourteen_days, device_type)
    retention_rate_in_float = 0
    if logged_in_14days_later_users_ids.__len__() > 0:
        retention_rate = calculate_retention_rate(selected_date, logged_in_14days_later_users_ids, device_type)
        retention_rate_in_float = "%.1f" % retention_rate

    return float(retention_rate_in_float)


def get_retention_rate_day30(selected_date, device_type):
    thirty_days_later = add_30_days(selected_date)
    end_of_thirty_days = add_twentyfour_hours_minus_a_second(thirty_days_later)
    logged_in_users_30days_later_ids = get_loggedin_users_phone_id(thirty_days_later, end_of_thirty_days, device_type)
    retention_rate_in_float = 0
    if logged_in_users_30days_later_ids.__len__() > 0:
        retention_rate = calculate_retention_rate(selected_date, logged_in_users_30days_later_ids, device_type)
        retention_rate_in_float = "%.1f" % retention_rate

    return float(retention_rate_in_float)
