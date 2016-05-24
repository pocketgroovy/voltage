__author__ = 'yoshi.miyamoto'

from datetime import datetime
from witcheskpi.utils.date_util import get_utc_datetime_from_pacific_time, add_twentyfour_hours_minus_a_second, \
    get_start_end_a_day_ago, combine_date_and_time, get_start_end_of_month_from_str
from pymongo import MongoClient
from django.utils import unittest


def get_db(db_name=None):
    client = MongoClient('localhost', 27017)
    return client[db_name]


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.db = get_db('witches')

    def test_get_utc_datetime_from_pacific(self):
        start_date = datetime(2015, 2, 1, 0, 0, 1)
        end_date = datetime(2015, 3, 1, 0, 0, 0)
        utc_start_date, utc_end_date = get_utc_datetime_from_pacific_time(start_date, end_date)
        self.assertEqual(utc_start_date, datetime(2015, 2, 1, 7, 0, 1), 'start date in UTC should be ' +
                         datetime(2015, 2, 1, 7, 0, 1).strftime('%Y-%m-%d %H:%M:%S') + ' but got ' +
                         utc_start_date.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(utc_end_date, datetime(2015, 3, 1, 7, 0, 0), 'start date in UTC should be ' +
                         datetime(2015, 3, 1, 7, 0, 0).strftime('%Y-%m-%d %H:%M:%S') + ' but got ' +
                         utc_end_date.strftime('%Y-%m-%d %H:%M:%S'))

    def test_get_utc_datetime_from_pacific_leap_year(self):
        start_date = datetime(2016, 2, 1, 0, 0, 1)
        end_date = datetime(2016, 3, 1, 0, 0, 0)
        utc_start_date, utc_end_date = get_utc_datetime_from_pacific_time(start_date, end_date)
        self.assertEqual(utc_start_date, datetime(2016, 2, 1, 7, 0, 1), 'start date in UTC should be ' +
                         datetime(2016, 2, 1, 7, 0, 1).strftime('%Y-%m-%d %H:%M:%S') + ' but got ' +
                         utc_start_date.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(utc_end_date, datetime(2016, 3, 1, 7, 0, 0), 'start date in UTC should be ' +
                         datetime(2016, 3, 1, 7, 0, 0).strftime('%Y-%m-%d %H:%M:%S') + ' but got ' +
                         utc_end_date.strftime('%Y-%m-%d %H:%M:%S'))

    def test_add_twentyfour_hours_minus_a_second(self):
        start_date = datetime(2015, 2, 1, 0, 0, 1)
        end_date = datetime(2015, 2, 2, 0, 0, 0)
        calculated_end_date = add_twentyfour_hours_minus_a_second(start_date)

        self.assertEqual(calculated_end_date, end_date, 'calculated datetime should be ' +
                         end_date.strftime('%Y-%m-%d %H:%M:%S') + ' but got ' +
                         calculated_end_date.strftime('%Y-%m-%d %H:%M:%S'))

    def test_get_start_and_end_of_a_day_ago(self):
        start_date = datetime(2015, 2, 1, 0, 0, 1)
        a_day_ago_start = datetime(2015, 1, 31, 0, 0, 1)
        a_day_ago_end = datetime(2015, 2, 1, 0, 0, 0)

        calculated_a_day_ago_start,  calculated_a_day_ago_end = get_start_end_a_day_ago(start_date)
        self.assertEqual(calculated_a_day_ago_start, a_day_ago_start, 'calculated datetime should be ' +
                 a_day_ago_start.strftime('%Y-%m-%d %H:%M:%S') + ' but got ' +
                 calculated_a_day_ago_start.strftime('%Y-%m-%d %H:%M:%S'))

        self.assertEqual(calculated_a_day_ago_end, a_day_ago_end, 'calculated datetime should be ' +
                 a_day_ago_end.strftime('%Y-%m-%d %H:%M:%S') + ' but got ' +
                 calculated_a_day_ago_end.strftime('%Y-%m-%d %H:%M:%S'))

    def test_get_start_and_end_from_String_date(self):
        selected_date = 'February/2015'
        month_start = datetime(2015, 2, 1)
        month_end = datetime(2015, 3, 1)
        start_date, end_date = get_start_end_of_month_from_str(selected_date)
        start_date_datetime_obj = combine_date_and_time(start_date, datetime.min.time())
        end_date_datetime_obj = combine_date_and_time(end_date, datetime.min.time())

        self.assertEqual(start_date_datetime_obj, month_start, 'datetime should be ' +
                 month_start.strftime('%Y-%m-%d') + ' but got ' + start_date.strftime('%Y-%m-%d'))

        self.assertEqual(end_date_datetime_obj, month_end, 'datetime should be ' +
                 month_end.strftime('%Y-%m-%d') + ' but got ' + end_date.strftime('%Y-%m-%d'))