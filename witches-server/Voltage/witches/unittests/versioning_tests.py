import json
from pymongo import MongoClient
from witches.models import *

__author__ = 'yoshi.miyamoto'

import unittest
from django.test.client import Client


class MyTestCase(unittest.TestCase):
    def setUp(self):
        Environment.objects.create(description='prod', build_version='1.1.4', device='IPhonePlayer', base_url='prod_url', current_api=True)
        Environment.objects.create(description='prod', build_version='1.1.4', device='Android', base_url='prod_url', current_api=False)
        Environment.objects.create(description='d', build_version='1.1.5_d', device='Android', base_url='dev_url', current_api=False)
        Environment.objects.create(description='d', build_version='1.1.5_d', device='IPhonePlayer', base_url='dev_url', current_api=False)

    # to test this, urls_current must have get_environment_v2 instead of get_environment
    # def test_versioning(self):
    #     c = Client()
    #     param = {'build': '1.1.4', 'device': 'IPhonePlayer'}
    #     r = c.post('/witches/get_environment/1', param)
    #     dic = json.loads(r.content)
    #     status = dic['status']
    #     version = dic['version']
    #     self.assertEqual(status, 'success')
    #     self.assertEqual(version, 'B')
    #
    #     param = {'build': '1.1.4', 'device': 'Android'}
    #     r = c.post('/witches/get_environment/1', param)
    #     dic = json.loads(r.content)
    #     status = dic['status']
    #     latest = dic['latest']
    #     self.assertEqual(status, 'success')
    #     self.assertTrue(latest)

    def test_versioning_missing_param(self):
        c = Client()
        param = {'build': '1.1.4'}
        r = c.post('/witches/get_environment/1', param)
        dic = json.loads(r.content)
        status = dic['status']
        error = dic['Error']
        self.assertEqual(status, 'failed')
        self.assertTrue('Key \'device\' not found in' in error,)

    def test_versioning_old_version(self):
        c = Client()
        param = {'build': '1.1.2', 'device': 'IPhonePlayer'}
        r = c.post('/witches/get_environment/1', param)
        dic = json.loads(r.content)
        status = dic['status']
        latest = dic['latest']
        self.assertEqual(status, 'success')
        self.assertFalse(latest)

    def test_versioning_dev_wrong_version(self):
        c = Client()
        param = {'build': '1.1.6_d', 'device': 'IPhonePlayer'}
        r = c.post('/witches/get_environment/1', param)
        dic = json.loads(r.content)
        status = dic['status']
        url = dic['base_url']
        self.assertEqual(status, 'success')
        self.assertEqual(url, 'dev_url')

    def tearDown(self):
            client = MongoClient('localhost', 27017)
            client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()
