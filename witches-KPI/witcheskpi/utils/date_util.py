__author__ = 'yoshi.miyamoto'

from calendar import isleap
from dateutil.relativedelta import relativedelta
from witcheskpi import const
import datetime


def get_utc_datetime_from_pacific_time(pt_start_date, pt_end_date):
    utc_start_date = pt_start_date + datetime.timedelta(seconds=25200)
    utc_end_date = pt_end_date + datetime.timedelta(seconds=25200)
    return utc_start_date, utc_end_date

def get_utc_datetime_by_adding_7hrs_to_pt(pt_start_date, pt_end_date):
    utc_start_date = combine_date_and_time(pt_start_date, datetime.time(7, 0, 0))
    utc_end_date = combine_date_and_time(pt_end_date, datetime.time(7, 0, 0))
    return utc_start_date, utc_end_date

def add_twentyfour_hours_minus_a_second(start_date):
    end_datetime = start_date + datetime.timedelta(seconds=86399)
    return end_datetime

def add_twentyfour_hours(start_date):
    end_datetime = start_date + datetime.timedelta(seconds=86400)
    return end_datetime

def add_3_days(start_date):
    end_datetime = start_date + datetime.timedelta(seconds=259200)
    return end_datetime

def add_7_days(start_date):
    end_datetime = start_date + datetime.timedelta(seconds=604800)
    return end_datetime

def add_14_days(start_date):
    end_datetime = start_date + datetime.timedelta(seconds=1209600)
    return end_datetime

def add_30_days(start_date):
    end_datetime = start_date + datetime.timedelta(seconds=2592000)
    return end_datetime

def get_start_end_a_day_ago(start_date):
    a_day_ago_start = start_date - datetime.timedelta(seconds=86400)
    a_day_ago_end = start_date - datetime.timedelta(seconds=1)
    return a_day_ago_start, a_day_ago_end

def get_start_end_three_days_ago(start_date):
    three_days_ago_start = start_date - datetime.timedelta(seconds=259200)
    three_days_ago_end = start_date - datetime.timedelta(seconds=172801)
    return three_days_ago_start, three_days_ago_end

def get_start_end_seven_days_ago(start_date):
    seven_days_ago_start = start_date - datetime.timedelta(seconds=604800)
    seven_days_ago_end = start_date - datetime.timedelta(seconds=518401)
    return seven_days_ago_start, seven_days_ago_end

def get_start_end_fourteen_days_ago(start_date):
    fourteen_days_ago_start = start_date - datetime.timedelta(seconds=1209600)
    fourteen_days_ago_end = start_date - datetime.timedelta(seconds=1123201)
    return fourteen_days_ago_start, fourteen_days_ago_end

def get_start_end_thirty_days_ago(start_date):
    thirty_days_ago_start = start_date - datetime.timedelta(seconds=2592000)
    thirty_days_ago_end = start_date - datetime.timedelta(seconds=2505601)
    return thirty_days_ago_start, thirty_days_ago_end

def combine_date_and_time(date, time):
    date_time = datetime.datetime.combine(date, time)
    return date_time

def get_start_end_of_month_from_str(selected_month):
    monthDict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                 'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
    days_in_month = {'January': 31, 'February': 28, 'March': 31, 'April': 30, 'May': 31, 'June': 30,
                    'July': 31, 'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}
    month, year = selected_month.split('/')

    startDate = monthDict[month] + '/01/' + year
    start_date = convert_to_datetime_obj(startDate)

    if month == 'February' and is_leap_year(start_date):
        days = const.leap_year_feb_end
    else:
        days = days_in_month[month]

    end_date = start_date + datetime.timedelta(days=days)

    return start_date, end_date

def is_leap_year(selected_date):
    year = selected_date.year
    return isleap(year)

# format is 12/31/2015
def convert_to_datetime_obj(string_date):
    date_obj = datetime.datetime.strptime(string_date, '%m/%d/%Y').date()
    return date_obj

def get_previous_month(selected_month, num_month):
    start_date_in_pt, end_date_in_pt = get_start_end_of_month_from_str(selected_month)
    start_date, end_date = get_utc_datetime_by_adding_7hrs_to_pt(start_date_in_pt, end_date_in_pt)
    prev_date_start = start_date - relativedelta(months=num_month)
    prev_date_end = end_date - relativedelta(months=num_month)
    return prev_date_start, prev_date_end

def get_longDates(sel_date):
    monthDict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    seldate = monthDict[sel_date.month] + ' / ' + str(sel_date.year)
    return seldate
