from pymongo import MongoClient
from witcheskpi import const
from witcheskpi.utils.date_util import get_utc_datetime_from_pacific_time
from witcheskpi.utils.retention_rate_query import get_retention_rate_day1, get_retention_rate_day3, \
    get_retention_rate_day7, get_retention_rate_day14, get_retention_rate_day30
from witcheskpi.models import *
from django.utils import unittest
const.deivce_type_all = 'ALL'
const.device_type_apple = 'IPhonePlayer'


class ModelsTestCase(unittest.TestCase):
    test_device = 'IPhonePlayer'  # IPhonePlayer, Android, Amazon, ALL   change the variables to test for those platform
    test_shop = 'APPLE'  # APPLE, GOOGLE, AMAZON, ALL

    def setUp(self):
        install_date = datetime.datetime(2015, 2, 5, 0, 0, 1)
        install_date2 = datetime.datetime(2015, 2, 6, 0, 0, 1)
        install_date3 = datetime.datetime(2015, 2, 7, 0, 0, 1)
        install_date4 = datetime.datetime(2015, 2, 8, 0, 0, 1)
        install_date8 = datetime.datetime(2015, 2, 12, 0, 0, 1)
        install_date15 = datetime.datetime(2015, 2, 19, 0, 0, 1)
        install_date31 = datetime.datetime(2015, 3, 10, 0, 0, 1)

        utc_install_date, utc_install_date2 = get_utc_datetime_from_pacific_time(install_date, install_date2)
        utc_install_date3, utc_install_date4 = get_utc_datetime_from_pacific_time(install_date3, install_date4)

        ShopItems.objects.create(product_id='com.voltage.ent.witch.001', price=0.99, item_index=0)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.002', price=4.99, item_index=1)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.003', price=9.99, item_index=2)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.004', price=19.99, item_index=3)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.005', price=39.99, item_index=4)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.006', price=59.99, item_index=5)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.101', price=0.99, item_index=6)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.102', price=4.99, item_index=7)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.103', price=9.99, item_index=8)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.104', price=19.99, item_index=9)
        ShopItems.objects.create(product_id='com.voltage.ent.witch.201', price=2.99, item_index=10)

        WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[], email='t_user1@test.com',
                              birthday='08/21/1999', free_currency=1000, premium_currency=20, ticket=5, focus=2,
                              delete_flag=0,phone_id='abcdefgh', closet=30, install_date=utc_install_date, device=self.test_device)

        WUsers.objects.create(last_name='t_last2', first_name='t_user1', gender='Male', work=[], email='t_user1@test.com',
                              birthday='08/21/1999', free_currency=1000, premium_currency=20, ticket=5, focus=2,
                              delete_flag=0,phone_id='12345678', closet=30, install_date=utc_install_date, device=self.test_device)

        WUsers.objects.create(last_name='t_last2', first_name='t_user1', gender='Male', work=[], email='t_user1@test.com',
                              birthday='08/21/1999', free_currency=1000, premium_currency=20, ticket=5, focus=2,
                              delete_flag=0,phone_id='98765432', closet=30, install_date=utc_install_date3, device=self.test_device)

        WUsers.objects.create(last_name='t_last2', first_name='t_user1', gender='Male', work=[], email='t_user1@test.com',
                              birthday='08/21/1999', free_currency=1000, premium_currency=20, ticket=5, focus=2,
                              delete_flag=0,phone_id='qwertyui', closet=30, install_date=utc_install_date4, device=self.test_device)

        user1 = WUsers.objects.get(phone_id='abcdefgh')
        user2 = WUsers.objects.get(phone_id='12345678')
        user3 = WUsers.objects.get(phone_id='qwertyui')

        UserLoginHistory.objects.create(phone_id=user1.phone_id, device=self.test_device, install_date=install_date,
                                        last_updated=install_date)
        UserLoginHistory.objects.create(phone_id=user1.phone_id, device=self.test_device, install_date=install_date2,
                                        last_updated=install_date2)
        UserLoginHistory.objects.create(phone_id=user1.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)
        UserLoginHistory.objects.create(phone_id=user1.phone_id, device=self.test_device, install_date=install_date8,
                                        last_updated=install_date8)

        UserLoginHistory.objects.create(phone_id=user2.phone_id, device=self.test_device, install_date=install_date,
                                        last_updated=install_date)
        UserLoginHistory.objects.create(phone_id=user2.phone_id, device=self.test_device, install_date=install_date3,
                                        last_updated=install_date3)
        UserLoginHistory.objects.create(phone_id=user2.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)
        UserLoginHistory.objects.create(phone_id=user2.phone_id, device=self.test_device, install_date=install_date15,
                                        last_updated=install_date15)

        UserLoginHistory.objects.create(phone_id=user3.phone_id, device=self.test_device, install_date=install_date31,
                                        last_updated=install_date31)

    def test_get_retention_rate_day1(self):
        start_date = datetime.datetime(2015, 2, 5, 0, 0, 1)
        num_rr1 = get_retention_rate_day1(start_date, self.test_device)
        self.assertEqual(num_rr1, 50, 'RR Day 1 should be 50% but got ' + str(num_rr1))

    def test_get_retention_rate_day1_no_found(self):
        start_date = datetime.datetime(2015, 2, 14, 0, 0, 1)
        num_rr1 = get_retention_rate_day1(start_date, self.test_device)
        self.assertEqual(num_rr1, 0, 'RR Day 1 should be 0 but got ' + str(num_rr1))

    def test_get_retention_rate_day3(self):
        start_date = datetime.datetime(2015, 2, 5, 0, 0, 1)
        num_rr3 = get_retention_rate_day3(start_date, self.test_device)
        self.assertEqual(num_rr3, 100, 'RR Day 3 should be 100% but got ' + str(num_rr3))

    def test_get_retention_rate_day7(self):
        start_date = datetime.datetime(2015, 2, 5, 0, 0, 1)
        num_rr7 = get_retention_rate_day7(start_date, self.test_device)
        self.assertEqual(num_rr7, 50, 'RR Day 7 should be 50% but got ' + str(num_rr7))

    def test_get_retention_rate_day14(self):
        start_date = datetime.datetime(2015, 2, 14, 0, 0, 1)
        num_rr14 = get_retention_rate_day14(start_date, self.test_device)
        self.assertEqual(num_rr14, 0, 'RR Day 14 should be 0 but got ' + str(num_rr14))

    def test_get_retention_rate_day30(self):
        start_date = datetime.datetime(2015, 2, 8, 0, 0, 1)
        num_rr30 = get_retention_rate_day30(start_date, self.test_device)
        self.assertEqual(num_rr30, 100, 'RR Day 30 should be 100% but got ' + str(num_rr30))

    def tearDown(self):
            client = MongoClient('localhost', 27017)
            client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()
