from django.utils import unittest
from pymongo import MongoClient
from witcheskpi.utils.date_util import get_utc_datetime_from_pacific_time
from witcheskpi.utils.sales_query import get_total_sales_price_in_cents, get_product_price_in_cents, get_total_units_sold, \
    get_total_units_sold_by_item, get_total_sales_price_by_item_in_cents, convert_cents_to_dollars
from witcheskpi.models import *

__author__ = 'yoshi.miyamoto'


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

        PaymentHistory.objects.create(user_id=user2.id, store_product_id='com.voltage.ent.witch.004', quantity=1,
                                      original_purchase_date_pst=utc_install_date, purchase_date_pst=utc_install_date,
                                      original_purchase_date=utc_install_date, purchase_date=utc_install_date,
                                      shop_type=self.test_shop)

        PaymentHistory.objects.create(user_id=user1.id, store_product_id='com.voltage.ent.witch.002', quantity=1,
                                      original_purchase_date_pst=utc_install_date2, purchase_date_pst=utc_install_date2,
                                      original_purchase_date=utc_install_date2, purchase_date=utc_install_date2,
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

        UserLoginHistory.objects.create(phone_id=user1.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)
        UserLoginHistory.objects.create(phone_id=user2.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)
        UserLoginHistory.objects.create(phone_id=user3.phone_id, device=self.test_device, install_date=install_date2,
                                        last_updated=install_date2)
        UserLoginHistory.objects.create(phone_id=user3.phone_id, device=self.test_device, install_date=install_date4,
                                        last_updated=install_date4)

    def test_get_total_monthly_sales_price(self):
        start_date = datetime.datetime(2015, 2, 1, 0, 0, 1)
        end_date = datetime.datetime(2015, 3, 1, 0, 0, 0)
        total_sales_price_in_cents = get_total_sales_price_in_cents(start_date, end_date, self.test_shop)
        total_sales_price = convert_cents_to_dollars(total_sales_price_in_cents)
        self.assertEqual(total_sales_price, 221.88, 'total sales should be 221.88 but got ' + str(total_sales_price))

    def test_get_total_daily_sales_price(self):
        start_date = datetime.datetime(2015, 2, 5, 0, 0, 1)
        end_date = datetime.datetime(2015, 2, 6, 0, 0, 0)
        total_sales_price_in_cents = get_total_sales_price_in_cents(start_date, end_date, self.test_shop)
        total_sales_price = convert_cents_to_dollars(total_sales_price_in_cents)
        self.assertEqual(total_sales_price, 29.98, 'total sales should be 29.98 but got ' + str(total_sales_price))

        decimal_places = 7
        self.assertAlmostEqual(total_sales_price, 29.98, decimal_places, 'total sales should be 29.98 but got ' + str(total_sales_price))

    def test_get_product_price(self):
        product_id = 'com.voltage.ent.witch.003'
        price_in_cents = get_product_price_in_cents(product_id)
        price = price_in_cents / 100
        self.assertEqual(price, 9.99, 'product price should be 9.99 but got ' + str(price))

    def test_get_total_monthly_purchases(self):
        start_date = datetime.datetime(2015, 2, 1, 0, 0, 1)
        end_date = datetime.datetime(2015, 3, 1, 0, 0, 0)
        total_purchases = get_total_units_sold(start_date, end_date, self.test_shop)
        self.assertEqual(len(total_purchases), 12, 'total purchases count should be 12 but got '
                                                     + str(len(total_purchases)))

    def test_get_total_daily_purchases(self):
        start_date = datetime.datetime(2015, 2, 7, 0, 0, 1)
        end_date = datetime.datetime(2015, 2, 8, 0, 0, 0)
        total_purchases = get_total_units_sold(start_date, end_date, self.test_shop)
        self.assertEqual(len(total_purchases), 4, 'total purchases count should be 4 but got '
                                                     + str(len(total_purchases)))

    def test_get_total_purchases_daily_no_purchase(self):
        start_date = datetime.datetime(2015, 3, 1, 0, 0, 1)
        end_date = datetime.datetime(2015, 3, 2, 0, 0, 0)
        total_purchases = get_total_units_sold(start_date, end_date, self.test_shop)
        self.assertEqual(len(total_purchases), 0, 'total purchases count should be 0 but got '
                                                     + str(len(total_purchases)))

    def test_get_total_monthly_purchases_by_item(self):
        start_date = datetime.datetime(2015, 2, 1, 0, 0, 1)
        end_date = datetime.datetime(2015, 3, 1, 0, 0, 0)
        product_id = 'com.voltage.ent.witch.002'
        total_purchases_by_item = get_total_units_sold_by_item(start_date, end_date, product_id, self.test_shop)
        self.assertEqual(len(total_purchases_by_item), 1, 'total purchases count by item should be 1 but got '
                                                     + str(len(total_purchases_by_item)))

    def test_get_total_daily_purchases_by_item(self):
        start_date = datetime.datetime(2015, 2, 8, 0, 0, 1)
        end_date = datetime.datetime(2015, 2, 9, 0, 0, 0)
        product_id = 'com.voltage.ent.witch.103'
        total_purchases_by_item = get_total_units_sold_by_item(start_date, end_date, product_id, self.test_shop)
        self.assertEqual(len(total_purchases_by_item), 1, 'total purchases count by item should be 1 but got '
                                                     + str(len(total_purchases_by_item)))

    def test_get_total_daily_sale_price_by_item_no_purchase(self):
        start_date = datetime.datetime(2015, 1, 25, 0, 0, 1)
        end_date = datetime.datetime(2015, 1, 26, 0, 0, 0)
        product_id = 'com.voltage.ent.witch.103'
        total_purchases_by_item = get_total_sales_price_by_item_in_cents(start_date, end_date, product_id, self.test_shop)
        self.assertEqual(total_purchases_by_item, 0, 'total purchases price by item should be 0 but got '
                                                     + str(total_purchases_by_item))

    def tearDown(self):
            client = MongoClient('localhost', 27017)
            client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()