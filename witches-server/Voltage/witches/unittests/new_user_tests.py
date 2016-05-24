__author__ = 'yoshi.miyamoto'

import datetime
from django.utils import unittest
from django.test.client import Client
from pymongo import MongoClient
from django.core.cache import cache
from witches.models import *


now = datetime.datetime.utcnow().replace(tzinfo=None)


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        WUsers.objects.create(last_name='', first_name='', gender='Female', work=[],
                              email='t_user3@test.com', birthday='08/20/1999', free_currency=0,
                              premium_currency=0, ticket=2, delete_flag=0,
                              phone_id='a1b2c3d4', closet=3)

    def test_get_first_last_name_from_request(self):
        cache.clear()
        c = Client()
        param = {'phone_id': 'a1b2c3d4', 'first_name': 'test_first', 'last_name':'test_last'}
        r = c.post('/witches/input_names/1', param)
        user = WUsers.objects.get(phone_id='a1b2c3d4')
        self.assertEqual(user.first_name, 'test_first', 'first name should be test_first but got ' + user.first_name)
        self.assertEqual(user.last_name, 'test_last', 'first name should be test_last but got ' + user.last_name)

    def test_get_first_last_name_from_request_missing_first_name(self):
        cache.clear()
        c = Client()
        param = {'phone_id': 'a1b2c3d4', 'last_name':'test_last'}
        r = c.post('/witches/input_names/1', param)
        user = WUsers.objects.get(phone_id='a1b2c3d4')
        if not user.last_name:
            user.last_name = ''
        if not user.first_name:
            user.first_name = ''
        self.assertEqual(user.last_name, '',  'last name should be empty but got ' + user.last_name)
        self.assertEqual(user.first_name, '', 'first name should be None type but got ' + user.first_name)

    def test_tutorial_progress(self):
        cache.clear()
        c = Client()
        param = {'phone_id': 'a1b2c3d4', 'tutorial_progress': 1, 'tutorial_name': 'home screen'}
        r = c.post('/witches/tutorial_progress/1', param)
        self.assertTrue("success" in r.content, 'tutorial progress failed')

        user = WUsers.objects.get(phone_id='a1b2c3d4')
        self.assertEqual(user.tutorial_progress, 1, 'tutorial progress should be 1 but got ' + str(user.tutorial_progress))

    def test_tutorial_finish(self):
        cache.clear()
        c = Client()
        param = {'phone_id': 'a1b2c3d4'}
        r = c.post('/witches/finish_tutorial/1', param)
        self.assertTrue("success" in r.content, 'tutorial finish failed')

        user = WUsers.objects.get(phone_id='a1b2c3d4')
        self.assertFalse(user.tutorial_flag, 'tutorial flag should be false')

    def tearDown(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()