from witcheskpi import const
from witcheskpi.utils.users_query import get_installed_users, get_unique_users, get_purchased_unique_users
from witcheskpi.utils.date_util import get_utc_datetime_from_pacific_time
from witcheskpi.models import *
from django.utils import unittest
from pymongo import MongoClient


class ModelsTestCase(unittest.TestCase):
    test_device = 'IPhonePlayer'  # IPhonePlayer, Android, Amazon, ALL   change the variables to test for those platform
    test_shop = 'APPLE'  # APPLE, GOOGLE, AMAZON, ALL

    def setUp(self):
        install_date = datetime.datetime(2015, 1, 5, 0, 0, 1)
        install_date2 = datetime.datetime(2015, 2, 6, 0, 0, 1)
        install_date3 = datetime.datetime(2015, 2, 7, 0, 0, 1)
        install_date4 = datetime.datetime(2015, 4, 8, 0, 0, 1)

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
                              delete_flag=0,phone_id='12345678', closet=30, install_date=utc_install_date2, device=self.test_device)

        WUsers.objects.create(last_name='t_last2', first_name='t_user1', gender='Male', work=[], email='t_user1@test.com',
                              birthday='08/21/1999', free_currency=1000, premium_currency=20, ticket=5, focus=2,
                              delete_flag=0,phone_id='98765432', closet=30, install_date=utc_install_date3, device=self.test_device)

        WUsers.objects.create(last_name='t_last2', first_name='t_user1', gender='Male', work=[], email='t_user1@test.com',
                              birthday='08/21/1999', free_currency=1000, premium_currency=20, ticket=5, focus=2,
                              delete_flag=0,phone_id='qwertyui', closet=30, install_date=utc_install_date4, device=self.test_device)

        user1 = WUsers.objects.get(phone_id='abcdefgh')
        user2 = WUsers.objects.get(phone_id='12345678')
        user3 = WUsers.objects.get(phone_id='qwertyui')

        PaymentHistory.objects.create(user_id=user1.id, store_product_id='com.voltage.ent.witch.003', quantity=1,
                                      original_purchase_date_pst=utc_install_date, purchase_date_pst=utc_install_date,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user1.id, store_product_id='com.voltage.ent.witch.002', quantity=1,
                                      original_purchase_date_pst=utc_install_date2, purchase_date_pst=utc_install_date2,
                                      original_purchase_date=utc_install_date2, purchase_date=utc_install_date2,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user2.id, store_product_id='com.voltage.ent.witch.004', quantity=1,
                                      original_purchase_date_pst=utc_install_date, purchase_date_pst=utc_install_date,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user2.id, store_product_id='com.voltage.ent.witch.005', quantity=1,
                                      original_purchase_date_pst=utc_install_date2, purchase_date_pst=utc_install_date2,
                                      original_purchase_date=utc_install_date2, purchase_date=utc_install_date2,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user1.id, store_product_id='com.voltage.ent.witch.006', quantity=1,
                                      original_purchase_date_pst=utc_install_date2, purchase_date_pst=utc_install_date2,
                                      original_purchase_date=utc_install_date2, purchase_date=utc_install_date2,
                                      shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user2.id, store_product_id='com.voltage.ent.witch.006', quantity=1,
                                      original_purchase_date_pst=utc_install_date3, purchase_date_pst=utc_install_date3,
                                      original_purchase_date=utc_install_date3, purchase_date=utc_install_date3,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user3.id, store_product_id='com.voltage.ent.witch.101', quantity=1,
                                      original_purchase_date_pst=utc_install_date3, purchase_date_pst=utc_install_date3,
                                      original_purchase_date=utc_install_date3, purchase_date=utc_install_date3,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user3.id, store_product_id='com.voltage.ent.witch.101', quantity=1,
                                      original_purchase_date_pst=utc_install_date4, purchase_date_pst=utc_install_date4,
                                      original_purchase_date=utc_install_date4, purchase_date=utc_install_date4,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user1.id, store_product_id='com.voltage.ent.witch.102', quantity=1,
                                      original_purchase_date_pst=utc_install_date3, purchase_date_pst=utc_install_date3,
                                      original_purchase_date=utc_install_date3, purchase_date=utc_install_date3,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user2.id, store_product_id='com.voltage.ent.witch.102', quantity=1,
                                      original_purchase_date_pst=utc_install_date3, purchase_date_pst=utc_install_date3,
                                      original_purchase_date=utc_install_date3, purchase_date=utc_install_date3,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user3.id, store_product_id='com.voltage.ent.witch.102', quantity=1,
                                      original_purchase_date_pst=utc_install_date4, purchase_date_pst=utc_install_date4,
                                      original_purchase_date=utc_install_date4, purchase_date=utc_install_date4,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user3.id, store_product_id='com.voltage.ent.witch.103', quantity=1,
                                      original_purchase_date_pst=utc_install_date4, purchase_date_pst=utc_install_date4,
                                      original_purchase_date=utc_install_date4, purchase_date=utc_install_date4,
                                      shop_type=self.test_shop)

        UserLoginHistory.objects.create(phone_id=user1.phone_id, device=self.test_device, install_date=install_date2,
                                        last_updated=install_date2)
        UserLoginHistory.objects.create(phone_id=user2.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)
        UserLoginHistory.objects.create(phone_id=user2.phone_id, device=self.test_device, install_date=install_date2,
                                        last_updated=install_date2)
        UserLoginHistory.objects.create(phone_id=user3.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)

    def test_get_monthly_install_num(self):
        start_date = datetime.datetime(2015, 2, 1, 0, 0, 1)
        end_date = datetime.datetime(2015, 3, 1, 0, 0, 0)
        installed = get_installed_users(start_date, end_date, self.test_device)
        self.assertEqual(installed.count(), 2, 'monthly installed number should be 2 but got ' + str(installed.count()))

        start_date = datetime.datetime(2015, 1, 1, 0, 0, 1)
        end_date = datetime.datetime(2015, 2, 1, 0, 0, 0)
        installed = get_installed_users(start_date, end_date, self.test_device)
        self.assertEqual(installed.count(), 1, 'monthly installed number should be 1 but got ' + str(installed.count()))

        start_date = datetime.datetime(2015, 3, 1, 0, 0, 1)
        end_date = datetime.datetime(2015, 4, 1, 0, 0, 0)
        installed = get_installed_users(start_date, end_date,  self.test_device)
        self.assertEqual(installed.count(), 0, 'monthly installed number should be 0 but got ' + str(installed.count()))

    def test_get_monthly_unique_user(self):
        start_date = datetime.datetime(2015, 2, 1, 0, 0, 1)
        end_date = datetime.datetime(2015, 3, 1, 0, 0, 0)
        unique_users = get_unique_users(start_date, end_date, self.test_device)
        self.assertEqual(len(unique_users), 3, 'monthly unique user count should be 3 but got ' + str(len(unique_users)))

    def test_get_daily_install_num(self):
        start_date = datetime.datetime(2015, 2, 6, 0, 0, 1)
        end_date = datetime.datetime(2015, 2, 7, 0, 0, 1)
        installed = get_installed_users(start_date, end_date, self.test_device)
        self.assertEqual(installed.count(), 1, 'daily installed number should be 1 but got ' + str(installed.count()))

        start_date = datetime.datetime(2015, 2, 2, 0, 0, 1)
        end_date = datetime.datetime(2015, 2, 3, 0, 0, 1)
        installed = get_installed_users(start_date, end_date,  self.test_device)
        self.assertEqual(installed.count(), 0, 'daily installed number should be 0 but got ' + str(installed.count()))

    def test_get_daily_unique_user(self):
        start_date = datetime.datetime(2015, 2, 6, 0, 0, 1)
        end_date = datetime.datetime(2015, 2, 7, 0, 0, 0)
        unique_users = get_unique_users(start_date, end_date, self.test_device)
        self.assertEqual(len(unique_users), 2, 'daily unique user count should be 2 but got ' + str(len(unique_users)))

    def test_get_daily_purchased_unique_users(self):
        start_date = datetime.datetime(2015, 4, 8, 0, 0, 1)
        end_date = datetime.datetime(2015, 4, 9, 0, 0, 0)
        purchased_unique_users = get_purchased_unique_users(start_date, end_date, self.test_shop)
        self.assertEqual(len(purchased_unique_users), 1, 'daily purchased unique user count should be 1 but got '
                         + str(len(purchased_unique_users)))

    def test_get_daily_purchased_unique_users_no_found(self):
        start_date = datetime.datetime(2015, 7, 22, 0, 0, 1)
        end_date = datetime.datetime(2015, 7, 23, 0, 0, 0)
        purchased_unique_users = get_purchased_unique_users(start_date, end_date, self.test_shop)
        self.assertEqual(len(purchased_unique_users), 0, 'daily purchased unique user count should be 0 but got '
                         + str(len(purchased_unique_users)))

    def test_get_monthly_purchased_unique_users(self):
        start_date = datetime.datetime(2015, 2, 1, 0, 0, 1)
        end_date = datetime.datetime(2015, 3, 1, 0, 0, 0)
        purchased_unique_users = get_purchased_unique_users(start_date, end_date, self.test_shop)
        self.assertEqual(len(purchased_unique_users), 3, 'monthly purchased unique user count should be 3 but got '
                         + str(len(purchased_unique_users)))

    def tearDown(self):
            client = MongoClient('localhost', 27017)
            client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()