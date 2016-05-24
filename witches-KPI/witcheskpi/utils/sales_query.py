from __future__ import division
__author__ = 'yoshi.miyamoto'
from witcheskpi.models import PaymentHistory, ShopItems
import logging
logger = logging.getLogger(__name__)


def get_all_items():
    all_items = ShopItems.objects.all()
    return all_items

def get_total_sales_price_in_cents(startDate, endDate, shop_type):
    total_purchases = get_total_units_sold(startDate, endDate, shop_type)
    total_price = 0
    if total_purchases.count() > 0:
        total_price = get_total_price_in_cents(total_purchases)
    else:
        logging.debug('No Purchases found between ' + startDate.strftime('%Y-%m-%d %H:%M:%S') + ' and '
                      + endDate.strftime('%Y-%m-%d %H:%M:%S') + ' in UTC')
    return total_price

def get_total_sales_price_by_item_in_cents(startDate, endDate, product_id, shop_type):
    total_price_by_item = 0
    total_purchases_by_item = get_total_units_sold_by_item(startDate, endDate, product_id, shop_type)
    if total_purchases_by_item.count() > 0:
        total_price_by_item = get_total_price_in_cents(total_purchases_by_item)
    else:
        logging.debug('No Purchases found between ' + startDate.strftime('%Y-%m-%d %H:%M:%S') + ' and '
                      + endDate.strftime('%Y-%m-%d %H:%M:%S' + ' in UTC'))
    return total_price_by_item

def get_total_units_sold_by_item(startDate, endDate, product_id, shop_type):
    if shop_type == 'ALL':
        total_purchases_by_item = PaymentHistory.objects.filter(original_purchase_date__gte=startDate,
                                                                original_purchase_date__lte=endDate,
                                                                delete_flag=False, store_product_id=product_id)
    else:
        try:
            total_purchases_by_item = PaymentHistory.objects.filter(original_purchase_date__gte=startDate,
                                                                original_purchase_date__lte=endDate,
                                                                delete_flag=False, store_product_id=product_id, shop_type=shop_type)
        except Exception as e:
            print('>>>>>>>>>>>>Exception get_total_units_sold_by_item :' + str(e))

    return total_purchases_by_item

def get_total_units_sold(startDate, endDate, shop_type):
    if shop_type == 'ALL':
        total_units = PaymentHistory.objects.filter(original_purchase_date__gte=startDate, original_purchase_date__lte=endDate,
                                                    delete_flag=False)
    else:
        try:
            total_units = PaymentHistory.objects.filter(original_purchase_date__gte=startDate, original_purchase_date__lte=endDate,
                                                    shop_type=shop_type, delete_flag=False)
        except Exception as e:
            print('>>>>>>>>>>>>Exception get_total_units_sold :' + str(e))
    return total_units


def get_purchase_rate(purchased_unique_users, unique_users):
    purchased_rate = 0
    try:
        purchased_rate_in_float = purchased_unique_users / unique_users
        purchased_rate = "%.4f" % purchased_rate_in_float
    except ZeroDivisionError as e:
        logging.debug(str(e))
    return float(purchased_rate)

def get_average_revenue_per_user(sales_amount, unique_users):
    arpu = 0
    try:
        arpu_in_float = sales_amount / unique_users
        arpu = "%.2f" % arpu_in_float
    except ZeroDivisionError as e:
        logging.debug(str(e))
    return float(arpu)

def get_average_revenue_per_paid_user(sales_amount, paid_users):
    arppu = 0
    try:
        arppu_in_float = sales_amount / paid_users
        arppu = "%.2f" % arppu_in_float
    except ZeroDivisionError as e:
        logging.debug(str(e))
    return float(arppu)

# sales util tools
def get_total_price_in_cents(purchases):
    total_price_in_cents = 0
    for purchase in purchases:
        total_price_in_cents += get_product_price_in_cents(purchase.store_product_id)
    return total_price_in_cents

def get_product_price_in_cents(product_id):
    item = ShopItems.objects.get(product_id=product_id)
    item_price_in_cents = convert_dollars_to_cents(item.price)
    return item_price_in_cents

def convert_dollars_to_cents(price_in_dollar):
    price_in_cents = price_in_dollar * 100
    return price_in_cents

def convert_cents_to_dollars(price_in_cents):
    price_in_dollars = 0
    try:
        price_in_dollars_in_float = price_in_cents / 100
        price_in_dollars = "%.2f" % price_in_dollars_in_float
    except ZeroDivisionError as e:
        logging.debug(str(e))
    return float(price_in_dollars)

def get_total_price_by_item_in_dollars(start_date, end_date, item, shop_type):
        item_in_cents = get_total_sales_price_by_item_in_cents(start_date, end_date, item, shop_type)
        item_in_dollars = convert_cents_to_dollars(item_in_cents)
        return item_in_dollars


def combine_all_platform_responses(responses):
    total_sales_amount = 0.00
    total_sales_units = 0
    stone_quintet = 0.00
    stone_quintet_units = 0
    stone_cache = 0.00
    stone_cache_units = 0
    stone_assembly= 0.00
    stone_assembly_units = 0
    stone_satchel = 0.00
    stone_satchel_units = 0
    stone_hoard = 0.00
    stone_hoard_units = 0
    stone_constel = 0.00
    stone_constel_units = 0
    stamina_batch = 0.00
    stamina_batch_units = 0
    stamina_set = 0.00
    stamina_set_units = 0
    stamina_case = 0.00
    stamina_case_units = 0
    stamina_hoard = 0.00
    stamina_hoard_units = 0
    installed_users = 0
    unique_users = 0
    purchased_unique_users = 0
    arpu = 0.00
    arppu = 0.00

    purchase_rate_in_percentage = 0.0

    for response in responses:
        total_sales_amount += response['total_sales_amount']
    for response in responses:
        total_sales_units += response['total_sales_units']
    for response in responses:
        stone_quintet += response['total_sales_stone_quintet']
    for response in responses:
        stone_quintet_units += response['total_units_stone_quintet']
    for response in responses:
        stone_cache += response['total_sales_stone_cache']
    for response in responses:
        stone_cache_units += response['total_units_stone_cache']
    for response in responses:
        stone_assembly += response['total_sales_stone_assembly']
    for response in responses:
        stone_assembly_units += response['total_units_stone_assembly']
    for response in responses:
        stone_satchel += response['total_sales_stone_satchel']
    for response in responses:
        stone_satchel_units += response['total_units_stone_satchel']
    for response in responses:
        stone_hoard += response['total_sales_stone_hoard']
    for response in responses:
        stone_hoard_units += response['total_units_stone_hoard']
    for response in responses:
        stone_constel += response['total_sales_stone_constel']
    for response in responses:
        stone_constel_units += response['total_units_stone_constel']
    for response in responses:
        stamina_batch += response['total_sales_stamina_batch']
    for response in responses:
        stamina_batch_units += response['total_units_stamina_batch']
    for response in responses:
        stamina_set += response['total_sales_stamina_set']
    for response in responses:
        stamina_set_units += response['total_units_stamina_set']
    for response in responses:
        stamina_case += response['total_sales_stamina_case']
    for response in responses:
        stamina_case_units += response['total_units_stamina_case']
    for response in responses:
        stamina_hoard += response['total_sales_stamina_hoard']
    for response in responses:
        stamina_hoard_units += response['total_units_stamina_hoard']
    for response in responses:
        installed_users += response['installed_user_number']
    for response in responses:
        unique_users += response['unique_users_number']
    for response in responses:
        purchased_unique_users += response['purchase_unique_users_number']
    for response in responses:
        arpu += response['arpu']
    for response in responses:
        arppu += response['arppu']

        date = response['date']
        weekend = response['weekend']

    all_responses = {
        'total_sales_amount': total_sales_amount,
        'total_sales_units': total_sales_units,

        'total_sales_stone_quintet': stone_quintet,
        'total_units_stone_quintet': stone_quintet_units,

        'total_sales_stone_cache': stone_cache,
        'total_units_stone_cache': stone_cache_units,

        'total_sales_stone_assembly': stone_assembly,
        'total_units_stone_assembly': stone_assembly_units,

        'total_sales_stone_satchel': stone_satchel,
        'total_units_stone_satchel': stone_satchel_units,

        'total_sales_stone_hoard': stone_hoard,
        'total_units_stone_hoard': stone_hoard_units,

        'total_sales_stone_constel': stone_constel,
        'total_units_stone_constel': stone_constel_units,

        'total_sales_stamina_batch': stamina_batch,
        'total_units_stamina_batch': stamina_batch_units,

        'total_sales_stamina_set': stamina_set,
        'total_units_stamina_set': stamina_set_units,

        'total_sales_stamina_case': stamina_case,
        'total_units_stamina_case': stamina_case_units,

        'total_sales_stamina_hoard': stamina_hoard,
        'total_units_stamina_hoard': stamina_hoard_units,

        'installed_user_number': installed_users,
        'unique_users_number': unique_users,
        'purchase_rate': purchase_rate_in_percentage,
        'purchase_unique_users_number': purchased_unique_users,
        'arpu': arpu,
        'arppu': arppu,
        'date': date,
        'weekend': weekend
    }

    return all_responses
