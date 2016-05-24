from django.db.models import Q
from witches.utils.util import get_now_datetime

__author__ = 'yoshi.miyamoto'

import datetime
from witches.models import UserLoginHistory
from django.utils import unittest
from django.test.client import Client


class ModelsTestCase(unittest.TestCase):

    def test_http_login(self):
        c = Client()
        r = c.post('/witches/login/1', {'phone_id': '39364868', 'device': 'Android'})
        self.assertEqual(r.status_code, 200, 'getting all master data failed')
        user = UserLoginHistory.objects.filter(phone_id='39364868')
        now = get_now_datetime()
        minus_now = now - datetime.timedelta(seconds=60)

        self.assertTrue(Q(user[user.__len__()-1].install_date.strftime('%Y-%m-%d %H:%M:%S') == minus_now.strftime('%Y-%m-%d %H:%M:%S'))
                        | Q(user[user.__len__()-1].install_date.strftime('%Y-%m-%d %H:%M:%S') == now.strftime('%Y-%m-%d %H:%M:%S')))
        self.assertEqual(user[user.__len__()-1].device, 'Android', 'User device should be Android but got '
                         + user[user.__len__()-1].device)
        self.assertEqual(user.__len__(), 1, 'user login count should be 1 but got ' + str(user.__len__()))

    def tearDown(self):
        user = UserLoginHistory.objects.filter(phone_id='39364868')
        user[user.__len__()-1].delete()
