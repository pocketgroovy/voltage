from witcheskpi import const
from witcheskpi.utils.date_util import get_longDates, get_previous_month
from witcheskpi.utils.sales_query import get_total_sales_price_in_cents, convert_cents_to_dollars, get_total_units_sold, \
    get_purchase_rate, get_average_revenue_per_user, get_average_revenue_per_paid_user, \
    get_total_units_sold_by_item, get_total_price_by_item_in_dollars
from witcheskpi.utils.users_query import get_installed_users, get_unique_users, get_purchased_unique_users
from calendar import monthrange
import datetime
from witcheskpi.utils.date_util import combine_date_and_time
from witcheskpi.utils.retention_rate_query import get_retention_rate_day1, get_retention_rate_day3, \
    get_retention_rate_day7, get_retention_rate_day14, get_retention_rate_day30


def get_results(start_date, end_date, shop_type):
        from witcheskpi.utils.util import get_device
        device_type = get_device(shop_type)
        # Total Sales Amount
        total_sales_amount_in_cents = get_total_sales_price_in_cents(start_date, end_date, shop_type)
        total_sales_amount = convert_cents_to_dollars(total_sales_amount_in_cents)

        # Total Sales Units
        total_sales_units = get_total_units_sold(start_date, end_date, shop_type)

        # first installed users
        installed_users = get_installed_users(start_date, end_date, device_type)

        # unique users
        unique_users = get_unique_users(start_date, end_date, device_type)

        # unique users who has purchased any item
        purchased_unique_users = get_purchased_unique_users(start_date, end_date, shop_type)

        # purchase rate
        purchase_rate = get_purchase_rate(len(purchased_unique_users), len(unique_users))
        purchase_rate_in_percentage = purchase_rate * 100

        # average revenue per user
        arpu_in_cents = get_average_revenue_per_user(total_sales_amount_in_cents, len(unique_users))
        arpu = convert_cents_to_dollars(arpu_in_cents)

        # average revenue per paid user
        arppu_in_cents = get_average_revenue_per_paid_user(total_sales_amount_in_cents, len(purchased_unique_users))
        arppu = convert_cents_to_dollars(arppu_in_cents)

        # sales by items
        stone_quintet = get_total_price_by_item_in_dollars(start_date, end_date, const.stone_quintet, shop_type)
        stone_quintet_units = get_total_units_sold_by_item(start_date, end_date, const.stone_quintet, shop_type)

        stone_cache = get_total_price_by_item_in_dollars(start_date, end_date, const.stone_cache, shop_type)
        stone_cache_units = get_total_units_sold_by_item(start_date, end_date, const.stone_cache, shop_type)

        stone_assembly = get_total_price_by_item_in_dollars(start_date, end_date, const.stone_assembly, shop_type)
        stone_assembly_units = get_total_units_sold_by_item(start_date, end_date, const.stone_assembly, shop_type)

        stone_satchel = get_total_price_by_item_in_dollars(start_date, end_date, const.stone_chest, shop_type)
        stone_satchel_units = get_total_units_sold_by_item(start_date, end_date, const.stone_chest, shop_type)

        stone_hoard = get_total_price_by_item_in_dollars(start_date, end_date, const.stone_hoard, shop_type)
        stone_hoard_units = get_total_units_sold_by_item(start_date, end_date, const.stone_hoard, shop_type)

        stone_constel = get_total_price_by_item_in_dollars(start_date, end_date, const.stone_constel, shop_type)
        stone_constel_units = get_total_units_sold_by_item(start_date, end_date, const.stone_constel, shop_type)

        stamina_batch = get_total_price_by_item_in_dollars(start_date, end_date, const.stamina_batch, shop_type)
        stamina_batch_units = get_total_units_sold_by_item(start_date, end_date, const.stamina_batch, shop_type)

        stamina_set = get_total_price_by_item_in_dollars(start_date, end_date, const.stamina_set, shop_type)
        stamina_set_units = get_total_units_sold_by_item(start_date, end_date, const.stamina_set, shop_type)

        stamina_case = get_total_price_by_item_in_dollars(start_date, end_date, const.stamina_case, shop_type)
        stamina_case_units = get_total_units_sold_by_item(start_date, end_date, const.stamina_case, shop_type)

        stamina_hoard = get_total_price_by_item_in_dollars(start_date, end_date, const.stamina_hoard, shop_type)
        stamina_hoard_units = get_total_units_sold_by_item(start_date, end_date, const.stamina_hoard, shop_type)

        if start_date.isoweekday() < 6:
            weekend = False
        else:
            weekend = True

        response = {
            'total_sales_amount': total_sales_amount,
            'total_sales_units': len(total_sales_units),

            'total_sales_stone_quintet': stone_quintet,
            'total_units_stone_quintet': len(stone_quintet_units),

            'total_sales_stone_cache': stone_cache,
            'total_units_stone_cache': len(stone_cache_units),

            'total_sales_stone_assembly': stone_assembly,
            'total_units_stone_assembly': len(stone_assembly_units),

            'total_sales_stone_satchel': stone_satchel,
            'total_units_stone_satchel': len(stone_satchel_units),

            'total_sales_stone_hoard': stone_hoard,
            'total_units_stone_hoard': len(stone_hoard_units),

            'total_sales_stone_constel': stone_constel,
            'total_units_stone_constel': len(stone_constel_units),

            'total_sales_stamina_batch': stamina_batch,
            'total_units_stamina_batch': len(stamina_batch_units),

            'total_sales_stamina_set': stamina_set,
            'total_units_stamina_set': len(stamina_set_units),

            'total_sales_stamina_case': stamina_case,
            'total_units_stamina_case': len(stamina_case_units),

            'total_sales_stamina_hoard': stamina_hoard,
            'total_units_stamina_hoard': len(stamina_hoard_units),

            'installed_user_number': len(installed_users),
            'unique_users_number': len(unique_users),
            'purchase_rate': purchase_rate_in_percentage,
            'purchase_unique_users_number': len(purchased_unique_users),
            'arpu': arpu,
            'arppu': arppu,
            'date': get_longDates(start_date),
            'weekend': weekend
        }

        return response


def get_weekly_results(selected_month, shop_type):
    from witcheskpi.utils.util import get_device
    device_type = get_device(shop_type)

    week, days = monthrange(selected_month.year, selected_month.month)

    weekly=[]
    for day in range(1, days + 1):
        sdate_date = datetime.datetime.strptime(str(selected_month.month) + '/' + str(day) + '/' + str(selected_month.year),
                                           "%m/%d/%Y").date()
        sdate = combine_date_and_time(sdate_date, datetime.time(7, 0, 1))

        edate = sdate + datetime.timedelta(days=1)
        daily = get_results(sdate, edate, shop_type)
        daily['date'] = str(sdate.month) + '/' + str(sdate.day)  # overwrite date of get_apple_result
        daily['retention1'] = get_retention_rate_day1(sdate, device_type)
        daily['retention2'] = get_retention_rate_day3(sdate, device_type)
        daily['retention3'] = get_retention_rate_day7(sdate, device_type)
        daily['retention4'] = get_retention_rate_day14(sdate, device_type)
        daily['retention5'] = get_retention_rate_day30(sdate, device_type)

        weekly.append(daily)

    return weekly


def get_monthly_results(start_date, end_date, selected_month, shop_type):
    response = get_results(start_date, end_date, shop_type)

    last_month_start, last_month_end = get_previous_month(selected_month, const.last_month)
    response1 = get_results(last_month_start, last_month_end, shop_type)

    two_months_ago_start,  two_months_ago_end = get_previous_month(selected_month, const.two_months_ago)
    response2 = get_results(two_months_ago_start, two_months_ago_end, shop_type)

    three_months_ago_start,  three_months_ago_end = get_previous_month(selected_month, const.three_months_ago)
    response3 = get_results(three_months_ago_start, three_months_ago_end, shop_type)

    four_months_ago_start,  four_months_ago_end = get_previous_month(selected_month, const.four_months_ago)
    response4 = get_results(four_months_ago_start, four_months_ago_end, shop_type)

    five_months_ago_start,  five_months_ago_end = get_previous_month(selected_month, const.five_months_ago)
    response5 = get_results(five_months_ago_start, five_months_ago_end, shop_type)

    return{'response_all': response, 'response_all1': response1, 'response_all2': response2, 'response_all3': response3,
           'response_all4': response4, 'response_all5': response5}

