from pymongo import MongoClient
from witcheskpi.data import get_results
from witcheskpi.models import *
from witcheskpi.utils.date_util import get_utc_datetime_from_pacific_time
import datetime
__author__ = 'yoshi.miyamoto'
from django.utils import unittest

class ModelsTestCase(unittest.TestCase):
    test_device = 'Amazon'  # IPhonePlayer, Android, Amazon, ALL   change the variables to test for those platform
    test_shop = 'AMAZON'  # APPLE, GOOGLE, AMAZON, ALL

    def setUp(self):
        install_date = datetime.datetime(2015, 2, 5, 0, 0, 1)
        install_date2 = datetime.datetime(2015, 2, 6, 0, 0, 0)
        install_date3 = datetime.datetime(2015, 2, 7, 0, 0, 1)
        install_date4 = datetime.datetime(2015, 2, 8, 0, 0, 0)

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
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user1.id, store_product_id='com.voltage.ent.witch.002', quantity=1,
                                      original_purchase_date_pst=utc_install_date2, purchase_date_pst=utc_install_date2,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user2.id, store_product_id='com.voltage.ent.witch.004', quantity=1,
                                      original_purchase_date_pst=utc_install_date, purchase_date_pst=utc_install_date,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user2.id, store_product_id='com.voltage.ent.witch.005', quantity=1,
                                      original_purchase_date_pst=utc_install_date2, purchase_date_pst=utc_install_date2,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user1.id, store_product_id='com.voltage.ent.witch.006', quantity=1,
                                      original_purchase_date_pst=utc_install_date2, purchase_date_pst=utc_install_date2,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user2.id, store_product_id='com.voltage.ent.witch.006', quantity=1,
                                      original_purchase_date_pst=utc_install_date3, purchase_date_pst=utc_install_date3,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user3.id, store_product_id='com.voltage.ent.witch.101', quantity=1,
                                      original_purchase_date_pst=utc_install_date3, purchase_date_pst=utc_install_date3,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user3.id, store_product_id='com.voltage.ent.witch.101', quantity=1,
                                      original_purchase_date_pst=utc_install_date4, purchase_date_pst=utc_install_date4,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user1.id, store_product_id='com.voltage.ent.witch.102', quantity=1,
                                      original_purchase_date_pst=utc_install_date3, purchase_date_pst=utc_install_date3,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user2.id, store_product_id='com.voltage.ent.witch.102', quantity=1,
                                      original_purchase_date_pst=utc_install_date3, purchase_date_pst=utc_install_date3,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user3.id, store_product_id='com.voltage.ent.witch.102', quantity=1,
                                      original_purchase_date_pst=utc_install_date4, purchase_date_pst=utc_install_date4,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)
        PaymentHistory.objects.create(user_id=user3.id, store_product_id='com.voltage.ent.witch.103', quantity=1,
                                      original_purchase_date_pst=utc_install_date4, purchase_date_pst=utc_install_date4,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date, shop_type=self.test_shop)

        UserLoginHistory.objects.create(phone_id=user1.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)
        UserLoginHistory.objects.create(phone_id=user2.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)
        UserLoginHistory.objects.create(phone_id=user3.phone_id, device=self.test_device, install_date=install_date2,
                                        last_updated=install_date2)
        UserLoginHistory.objects.create(phone_id=user3.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)

    def test_get_monthly_results(self):
        start_date_in_pt = datetime.datetime(2015, 2, 1, 0, 0, 1)
        end_date_in_pt = datetime.datetime(2015, 3, 1, 0, 0, 0)
        start_date_in_utc, end_date_in_utc = get_utc_datetime_from_pacific_time(start_date_in_pt, end_date_in_pt)
        monthly_result = get_results(start_date_in_utc, end_date_in_utc, self.test_shop)

        # total sales amount
        self.assertEqual(monthly_result['total_sales_amount'],  221.88,
                         'total_sales_amount should be 221.88 but got ' +
                         str(monthly_result['total_sales_amount']))
        # total sales units
        self.assertEqual(monthly_result['total_sales_units'], 12,
                         'total_sales_units should be 12 but got ' +
                         str(monthly_result['total_sales_units']))

        #buy item
        self.assertEqual(monthly_result['total_sales_stone_quintet'], 0,
                         'total_sales_stone_quintet should be 0 but got ' +
                         str(monthly_result['total_sales_stone_quintet']))

        self.assertEqual(monthly_result['total_units_stone_quintet'], 0,
                         'total_units_stone_quintet should be 0 but got ' +
                         str(monthly_result['total_units_stone_quintet']))

        self.assertEqual(monthly_result['total_sales_stone_cache'], 4.99,
                         'total_sales_stone_cache should be 4.99 but got ' +
                         str(monthly_result['total_sales_stone_cache']))

        self.assertEqual(monthly_result['total_units_stone_cache'], 1,
                         'total_units_stone_cache should be 1 but got ' +
                         str(monthly_result['total_units_stone_cache']))

        self.assertEqual(monthly_result['total_sales_stone_assembly'], 9.99,
                         'total_sales_stone_assembly should be 9.99 but got ' +
                         str(monthly_result['total_sales_stone_assembly']))

        self.assertEqual(monthly_result['total_units_stone_assembly'], 1,
                         'total_units_stone_assembly should be 1 but got ' +
                         str(monthly_result['total_units_stone_assembly']))

        self.assertEqual(monthly_result['total_sales_stone_satchel'], 19.99,
                         'total_sales_stone_satchel should be 19.99 but got ' +
                         str(monthly_result['total_sales_stone_satchel']))

        self.assertEqual(monthly_result['total_units_stone_satchel'], 1,
                         'total_units_stone_satchel should be 1 but got ' +
                         str(monthly_result['total_units_stone_satchel']))

        self.assertEqual(monthly_result['total_sales_stone_hoard'], 39.99,
                         'total_sales_stone_hoard should be 39.99 but got ' +
                         str(monthly_result['total_sales_stone_hoard']))

        self.assertEqual(monthly_result['total_units_stone_hoard'], 1,
                         'total_units_stone_hoard should be 1 but got ' +
                         str(monthly_result['total_units_stone_hoard']))

        self.assertEqual(monthly_result['total_sales_stone_constel'], 119.98,
                         'total_sales_stone_constel should be 119.98 but got ' +
                         str(monthly_result['total_sales_stone_constel']))

        self.assertEqual(monthly_result['total_units_stone_constel'], 2,
                         'total_units_stone_constel should be 2 but got ' +
                         str(monthly_result['total_units_stone_constel']))

        self.assertEqual(monthly_result['total_sales_stamina_batch'], 1.98,
                         'total_sales_stamina_batch should be 4.99 but got ' +
                         str(monthly_result['total_sales_stamina_batch']))

        self.assertEqual(monthly_result['total_units_stamina_batch'], 2,
                         'total_units_stamina_batch should be 2 but got ' +
                         str(monthly_result['total_units_stamina_batch']))

        self.assertEqual(monthly_result['total_sales_stamina_set'], 14.97,
                         'total_sales_stamina_set should be 14.97 but got ' +
                         str(monthly_result['total_sales_stamina_set']))

        self.assertEqual(monthly_result['total_units_stamina_set'], 3,
                         'total_units_stamina_set should be 3 but got ' +
                         str(monthly_result['total_units_stamina_set']))

        self.assertEqual(monthly_result['total_sales_stamina_case'], 9.99,
                         'total_sales_stamina_case should be 9.99 but got ' +
                         str(monthly_result['total_sales_stamina_case']))

        self.assertEqual(monthly_result['total_units_stamina_case'], 1,
                         'total_units_stamina_case should be 1 but got ' +
                         str(monthly_result['total_units_stamina_case']))

        self.assertEqual(monthly_result['total_sales_stamina_hoard'], 0,
                         'total_sales_stamina_hoard should be 0 but got ' +
                         str(monthly_result['total_sales_stamina_hoard']))

        self.assertEqual(monthly_result['total_units_stamina_hoard'], 0,
                         'total_units_stamina_hoard should be 0 but got ' +
                         str(monthly_result['total_units_stamina_hoard']))

        # installed users
        self.assertEqual(monthly_result['installed_user_number'], 4,
                         'installed_user_number should be 4 but got ' +
                         str(monthly_result['installed_user_number']))
        # unique users
        self.assertEqual(monthly_result['unique_users_number'], 4,
                         'unique_users_number should be 4 but got ' +
                         str(monthly_result['unique_users_number']))
        # purchased users
        self.assertEqual(monthly_result['purchase_unique_users_number'], 3,
                         'purchase_unique_users_number should be 3 but got ' +
                         str(monthly_result['purchase_unique_users_number']))
        # purchase rate
        self.assertEqual(monthly_result['purchase_rate'], 75.0,
                         'purchase_rate should be 75.0 but got ' +
                         str(monthly_result['purchase_rate']))

        # arpu
        self.assertEqual(monthly_result['arpu'], 55.47,
                         'arpu should be 55.47 but got ' + str(monthly_result['arpu']))

        # arppu
        self.assertEqual(monthly_result['arppu'], 73.96,
                         'arppu should be 73.96(python couldn\'t round 49.985 to 49.99) but got ' +
                         str(monthly_result['arppu']))
    def tearDown(self):
            client = MongoClient('localhost', 27017)
            client.drop_database(name_or_database='UnitTest')


if __name__ == '__main__':
    unittest.main()