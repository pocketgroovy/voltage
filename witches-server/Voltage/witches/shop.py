from witches.support import payment_history_error
from witches.utils.custom_exceptions import ReceiptVerificationError
from witches.utils.user_util import get_user

__author__ = 'carlos.matsumoto', 'yoshi.miyamoto'

import json
import datetime
from pymongo.errors import ConnectionFailure
from witches.master import get_stamina_max, get_shop_item
from witches.utils.string_util import separate_str_by_space
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from witches.utils.util import get_properties, throw_error, throw_error_in_json, convert_seconds_to_datetime, \
    convert_utc_to_pst, log_out_of_sync_error, purchase_error_message, get_now_datetime
from witches.utils.purchase import verify_apple_receipt, verify_amazon_receipt, verify_android_receipt
from models import *
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
from user import get_playerstate
from bson import objectid
from witches import const

import logging

logger = logging.getLogger(__name__)

class MismatchedItemClass(Exception):
    pass


# This likely should not throw mismatcheditemclass anymore -- it knows the requested type, so it can just return None if the item
# is not found in the associated table
def retrieve_item(item_id, requested_item_type):
    # 0: ingredients, 1: avatar, 2: clothing coordination
    item_tables = [ Ingredients, AvatarItems, ClothingCoordinates ]

    item = None
    for idx, table in enumerate(item_tables):
        item_set = table.objects.filter(id=ObjectId(item_id), delete_flag=False)
            
        if len(item_set) > 0:
            if requested_item_type != idx:
                # the found item doesn't match the requested item type
                raise MismatchedItemClass
            item = item_set[0]
            break

    return item

def retrieve_user(user_id):
    user_set = WUsers.objects.filter(phone_id=user_id, delete_flag=False)

    if len(user_set) == 0:
        return None

    # ignore the case of the user id returning multiple rows
    return user_set[0]

def buy_with_coins_html(request):
    other = 'buy_with_coins'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'item_form': 'coins', 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def buy_with_coins(request, type_res):
    other = 'buy_with_coins'

    type_res = int(type_res) or 0

    try:
        phone_id = request.POST['phone_id']
        # 0:inventory 1:avatar 2:clothing coordination
        item_type = int(request.POST['item_type'])
        item_id = request.POST['item_id']
        quantity = int(request.POST['quantity'])

        context = RequestContext(request, {request: request, 'user': request.user})

        try:
            item = retrieve_item(item_id, item_type)
        except MismatchedItemClass:
            return handle_mismatched_item(context, type_res, phone_id, other)

        if not item:
            return handle_no_item_found(context, type_res, phone_id, other)

        # Ensure the item is purchaseable by free currency
        if item.currency_flag != 1 and item.currency_flag != 3:
            return handle_unpurchaseable_item(context, type_res, phone_id, other)

        user = retrieve_user(phone_id)
        if not user:
            return handle_missing_user(context, type_res, phone_id, other)

        if int(user.free_currency) < int(item.coins_price) * quantity:
            error = purchase_error_message(other, user.free_currency, item_id, quantity, item.coins_price)
            log_out_of_sync_error(error, phone_id)

        add_to_inventory(user, item, quantity, item_type, is_premium=False)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    return get_playerstate(request=request, type_res=type_res)


def buy_with_stones_html(request):
    other = 'buy_with_stones'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'item_form': 'stones', 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def buy_with_stones(request, type_res):
    other = 'buy_with_stones'

    type_res = int(type_res) or 0

    try:
        phone_id = request.POST['phone_id']
        # 0:inventory  1:avatar  2:clothing coordination 3:closet
        item_type = int(request.POST['item_type'])
        item_id = request.POST['item_id']
        quantity = int(request.POST['quantity'])
        context = RequestContext(request, {request: request, 'user': request.user})

        user = retrieve_user(phone_id)
        if not user:
            return handle_missing_user(context, type_res, phone_id, other)

        if item_type == const.type_closet:
            buy_closet_space(user, quantity, phone_id, other)
        else:
            try:
                item = retrieve_item(item_id, item_type)
            except MismatchedItemClass:
                return handle_mismatched_item(context, type_res, phone_id, other)

            if not item:
                return handle_no_item_found(context, type_res, phone_id, other)

            # Ensure the item is purchaseable by premium currency
            if item.currency_flag != 2 and item.currency_flag != 3:
                return handle_unpurchaseable_item(context, type_res, phone_id, other)

            if int(user.premium_currency) < int(item.premium_price) * quantity:
                error = purchase_error_message(other, user.premium_currency, item_id, quantity, item.premium_price)
                log_out_of_sync_error(error, phone_id)

            add_to_inventory(user, item, quantity, item_type, is_premium=True)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    return get_playerstate(request=request, type_res=type_res)


CLOSET_SPACE_PRICE=1

# This function could use some attention to edge cases.
# We should really clarify requirements with production
def buy_closet_space(user, quantity, phone_id, other):
    closet_exchange_rate = ItemExchangeRate.objects.get(ticket=const.closet_ticket, delete_flag=False)

    if user.premium_currency < CLOSET_SPACE_PRICE * quantity:
        error = purchase_error_message(other, user.premium_currency, 'Closet', quantity, CLOSET_SPACE_PRICE, user.closet)
        log_out_of_sync_error(error, phone_id)

    if user.closet < closet_exchange_rate.max or closet_exchange_rate.max == 0:
        user.premium_currency = user.premium_currency - CLOSET_SPACE_PRICE * quantity
        # revert this change when we don't want to accept all purchases
        if user.premium_currency < 0:
            user.closet += closet_exchange_rate.ticket_quantity * quantity
            error = 'FUNCTION: "buy_closet_space", <USER CURRENCY>:' + str(user.premium_currency) + ', adjusting it to 0'
            log_out_of_sync_error(error, phone_id)
            user.premium_currency = 0

        if user.closet > closet_exchange_rate.max and closet_exchange_rate.max != 0:
            user.closet = closet_exchange_rate.max
    else:
        user.closet = closet_exchange_rate.max

    user.save()

def add_to_inventory(user, item, quantity, item_type, is_premium):
    new_item = None
    
    if item_type == const.type_ingredient:
        item_set = UserItemInventory.objects.filter(user_id=user.id, ingredient_id=item.id, delete_flag=False)
        if len(item_set) == 0:
            new_item = UserItemInventory.objects.create(user_id=user.id, ingredient_id=item.id, quantity=0)
        else:
            new_item = item_set[0]
        
    elif item_type == const.type_avatar:
        item_set = UserAvatarItemsInCloset.objects.filter(user_id=user.id, avatar_item_id=item.id, delete_flag=False)
        if len(item_set) == 0:
            new_item = UserAvatarItemsInCloset.objects.create(user_id=user.id, avatar_item_id=item.id, quantity=0)
        else:
            new_item = item_set[0]

    elif item_type == const.type_coordinate:
        item_set = UserAvatarItemsInCloset.objects.filter(user_id=user.id, coordinate_item_id=item.id, delete_flag=False)
        if len(item_set) == 0:
            new_item = UserAvatarItemsInCloset.objects.create(user_id=user.id, coordinate_item_id=item.id, quantity=0)
        else:
            new_item = item_set[0]

    currency_field = 'premium_currency' if is_premium else 'free_currency'
    price_field = 'premium_price' if is_premium else 'coins_price'
    new_currency = int(getattr(user, currency_field)) - int(getattr(item, price_field)) * quantity
    # This can be taken out when we no longer want all user transactions to be accepted. For now I don't want to deal with edge cases where the currency goes negative
    if new_currency < 0:
        new_currency = 0
    setattr(user, currency_field, new_currency)
    user.save()

    new_quantity = int(new_item.quantity) + quantity
    new_item.quantity = new_quantity
    new_item.save()


# common error handling function, extract out to a common error handling file/class
def handle_missing_user(context, type_res, phone_id, other):
    error = get_properties(err_type="Error", err_code="ERR0023")
    res_dict = {'status': 'failed', 'function': other, 'Error': error}
    if type_res == 0:
        return throw_error(template="home.html", obj_dict=res_dict, context=context)
    else:
        return throw_error_in_json(res_dict, phone_id)


def handle_mismatched_item(context, type_res, phone_id, other):
    error = get_properties(err_type="Error", err_code="ERR0022")
    res_dict = {'status': 'failed', 'function': other, 'Error': error}
    if type_res == 0:
        return throw_error(template="home.html", obj_dict=res_dict, context=context)
    else:
        return throw_error_in_json(res_dict, phone_id)


def handle_no_item_found(context, type_res, phone_id, other):
    error = get_properties(err_type='Error', err_code='ERR0032')
    res_dict = {'status': 'failed', 'function': other, 'Error': error}
    if type_res == 0:
        return throw_error(template="home.html", obj_dict=res_dict, context=context)
    else:
        return throw_error_in_json(res_dict, phone_id)
    

def handle_unpurchaseable_item(context, type_res, phone_id, other):
    error = get_properties(err_type='Warning', err_code='WAR0011')
    res_dict = {'status': 'failed', 'function': other, 'Error': error}
    if type_res == 0:
        return throw_error(template="home.html", obj_dict=res_dict, context=context)
    else:
        return throw_error_in_json(res_dict, phone_id)


def handle_missing_funds(context, type_res, phone_id, other):
    error = get_properties(err_type='Error', err_code='ERR0006')
    res_dict = {'status': 'failed', 'function': other, 'Error': error}
    if type_res == 0:
        return throw_error(template="home.html", obj_dict=res_dict, context=context)
    else:
        return throw_error_in_json(res_dict, phone_id)


def handle_missing_funds_for_closet(context, type_res, phone_id, other):
    error = get_properties(err_type='Warning', err_code='WAR0015')
    res_dict = {'status': 'failed', 'function': other, 'Error': error}
    if type_res == 0:
        return throw_error(template="home.html", obj_dict=res_dict, context=context)
    else:
        return throw_error_in_json(res_dict, phone_id)


def handle_bundle_purchase(bundle_items, user):
    if 'Starstone' in bundle_items:
        new_quantity = int(user.premium_currency) + int(bundle_items['Starstone'])
        user.premium_currency = new_quantity
        logger.debug('User['+user.phone_id + ']' + ' Starstone should be updating to ' + str(new_quantity))
    if 'Stamina' in bundle_items:
        new_quantity = int(user.stamina_potion) + int(bundle_items['Stamina'])
        user.stamina_potion = new_quantity
        logger.debug('User['+user.phone_id + ']' + ' Stamina potion should be updating to ' + str(new_quantity))
    if 'Closet' in bundle_items:
        new_quantity = int(user.closet) + int(bundle_items.Closet)
        user.closet = new_quantity
        logger.debug('User['+user.phone_id + ']' + ' Closet should be updating to ' + str(new_quantity))

    if 'Avatar' in bundle_items:
        for item in bundle_items['Avatar']:
            item_set = UserAvatarItemsInCloset.objects.filter(user_id=user.id, avatar_item_id=item, delete_flag=False)
            if len(item_set) == 0:
                new_item = UserAvatarItemsInCloset.objects.create(user_id=user.id, avatar_item_id=item, quantity=0)
            else:
                new_item = item_set[0]
            save_item_quantity(new_item)

    if 'Potion' in bundle_items:
        for item in bundle_items['Potion']:
            item_set = UserItemInventory.objects.filter(user_id=user.id, potion_id=item, delete_flag=False)
            if len(item_set) == 0:
                new_item = UserItemInventory.objects.create(user_id=user.id, potion_id=item, quantity=0)
            else:
                new_item = item_set[0]
            save_item_quantity(new_item)

    if 'Ingredient' in bundle_items:
        for item in bundle_items['Ingredient']:
            item_set = UserItemInventory.objects.filter(user_id=user.id, ingredient_id=item, delete_flag=False)
            if len(item_set) == 0:
                new_item = UserItemInventory.objects.create(user_id=user.id, ingredient_id=item, quantity=0)
            else:
                new_item = item_set[0]
            save_item_quantity(new_item)

    user.save()


def save_item_quantity(new_item):
    new_quantity = int(new_item.quantity) + 1
    new_item.quantity = new_quantity
    new_item.save()


def buy_inapp_html(request):
    other = 'buy_inapp'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'item_form': 'premium', 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def buy_inapp(request, type_res):
    other = 'buy_inapp'
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    context = RequestContext(request, {request: request, 'user': request.user})
    try:
        phone_id = request.POST['phone_id']
        premium_id = request.POST['premium_id']
        receipt_data = request.POST['receipt']
        device_os = request.POST['device_os']

        logger.debug('receipt_data:' + receipt_data + '   >>phone_id[' + phone_id + ']' + ', Device[' + device_os + ']')

        wuser = get_user(phone_id)

        currency_item = get_shop_item(premium_id)
        if not isinstance(currency_item, ShopItems) and 'Error' in currency_item:
            return throw_error_in_json(currency_item, phone_id)

        if device_os == 'ios':
            response_json = verify_apple_receipt(receipt_data)
            receipt = response_json['receipt']
            save_ios_receipt_data(wuser, receipt, premium_id)

        elif device_os == 'android':
            save_android_receipt_data(wuser, receipt_data, premium_id)

        elif device_os == 'amazon':
            receipt, amazon_user_id = verify_amazon_receipt(receipt_data)
            save_amazon_receipt_data(wuser, receipt, premium_id, amazon_user_id)
        else:
            logger.error('unknown os!')

        if 'Starstone' in currency_item.name:
            new_quantity = int(wuser.premium_currency) + int(currency_item.premium_qty)
            wuser.premium_currency = new_quantity
            wuser.save()
            logger.debug('User['+wuser.phone_id + ']' + ' Starstone should be updating to ' + str(new_quantity))
        elif 'Stamina' in currency_item.name:
            new_quantity = int(wuser.stamina_potion) + int(currency_item.premium_qty)
            wuser.stamina_potion = new_quantity
            wuser.save()
            logger.debug('User['+wuser.phone_id + ']' + ' Stamina potion should be updating to ' + str(new_quantity))
        elif len(currency_item.bundle_items):
            handle_bundle_purchase(currency_item.bundle_items, wuser)
        else:
            logger.error('unknown item!')

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        payment_history_error(e, phone_id, premium_id, receipt_data, device_os)
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    logger.debug('User['+wuser.phone_id + '] purchased[' + premium_id + ']' + ' on device[' + device_os + ']')

    return get_playerstate(request=request, type_res=type_res)


def save_amazon_receipt_data(user, receipt, premium_id, amazon_user_id):
    product_id = premium_id
    receipt_id = receipt['receiptId']
    quantity = receipt['quantity']
    unique_identifier = amazon_user_id

    purchase_date_since_epoch = receipt['purchaseDate']

    original_purchase_date = convert_seconds_to_datetime(purchase_date_since_epoch)
    original_purchase_date_pst = convert_utc_to_pst(original_purchase_date)

    purchase_date = original_purchase_date  # this should be updated when the item restored. as we only have consumable, use the original one for now.
    purchase_date_pst = original_purchase_date_pst

    original_transaction_id = receipt_id
    transaction_id = receipt_id # this should be updated when the item restored. as we only have consumable, use the original one for now.

    receipt_dict = {'user_id': user.id, 'store_product_id': product_id, 'store_item_id': 'NA', 'shop_type': 'AMAZON',
                    'unique_identifier': unique_identifier, 'unique_vendor_identifier': 'NA', 'original_purchase_date_pst':
                        original_purchase_date_pst, 'original_purchase_date': original_purchase_date, 'purchase_date_pst':
                        purchase_date_pst, 'purchase_date': purchase_date, 'quantity': quantity, 'original_transaction_id':
                        original_transaction_id, 'transaction_id': transaction_id}

    create_payment_history(**receipt_dict)


def save_ios_receipt_data(user, receipt, premium_id):
    product_id = premium_id
    if 'in_app' in receipt:  # new format
        unique_identifier = receipt['version_external_identifier']  # old receipt field 'unique_identifier' not exited in new receipt
        unique_vendor_identifier = receipt['bundle_id']  # old receipt field 'unique_vendor_identifier' not existed in new receipt
        item_id = receipt['app_item_id']

        in_app_list = receipt['in_app']  # Apple is returning a list of dictionary for in_app
        if bool(in_app_list):
            in_app = in_app_list[0]
        else:
            in_app = {}

        common_receipt_fields = get_receipt_common_fields(in_app)

    else:  # old format, before iOS7
        unique_identifier = receipt['unique_identifier']
        unique_vendor_identifier = receipt['unique_vendor_identifier']
        item_id = premium_id  # old receipt doesn't have this info so use product id instead
        common_receipt_fields = get_receipt_common_fields(receipt)

    base_fields = {'user_id': user.id, 'store_product_id': product_id, 'store_item_id': item_id, 'shop_type': 'APPLE',
                    'unique_identifier': unique_identifier, 'unique_vendor_identifier': unique_vendor_identifier}
    receipt_dict = dict(base_fields, **common_receipt_fields)
    create_payment_history(**receipt_dict)


def get_receipt_common_fields(receipt):
    if bool(receipt):
        original_purchase_date_pst = convert_str_date_for_ios(receipt['original_purchase_date_pst'])
        original_purchase_date = convert_str_date_for_ios(receipt['original_purchase_date'])
        purchase_date_pst = convert_str_date_for_ios(receipt['purchase_date_pst'])
        purchase_date = convert_str_date_for_ios(receipt['purchase_date'])
        quantity = receipt['quantity']
        original_transaction_id = receipt['original_transaction_id']
        transaction_id = receipt['transaction_id']
    else:
        error = get_properties(err_type="Error", err_code="ERR0094")
        raise ReceiptVerificationError(error)

    return {'original_purchase_date_pst': original_purchase_date_pst, 'original_purchase_date': original_purchase_date,
            'purchase_date_pst': purchase_date_pst, 'purchase_date': purchase_date, 'quantity': quantity,
            'original_transaction_id': original_transaction_id, 'transaction_id': transaction_id}


from collections import OrderedDict


def save_android_receipt_data(user, receipt_data, premium_id):
    if "json" in receipt_data:
        product_id = premium_id
        sanitized_json = sanitize_receipt_json(receipt_data)
        # key order in dict has to be kept to pass the receipt verification "object_pairs_hook=OrderedDict"
        #  will keep the order
        receipt_json_decode = json.loads(sanitized_json, object_pairs_hook=OrderedDict)
        receipt = receipt_json_decode['json']
        signature = receipt_json_decode['signature']
        purchased_time_in_seconds = receipt['purchaseTime']
        order_id = receipt['orderId']
        purchase_token = receipt['purchaseToken']
        package_name = receipt['packageName']

        original_purchase_date = convert_seconds_to_datetime(purchased_time_in_seconds)
        purchase_date_pst = convert_utc_to_pst(original_purchase_date)
    else:
        raise ReceiptVerificationError('Wrong Android receipt format')

    if verify_android_receipt(receipt, signature):
        item_id = 'The Field Not Exist In Android Receipt'
        unique_identifier = purchase_token
        unique_vendor_identifier = package_name # bundle id as 'com.voltage.curse.en'
        receipt_dict = {'user_id': user.id, 'store_product_id': product_id, 'store_item_id': item_id, 'shop_type':
                        'GOOGLE', 'unique_identifier': unique_identifier, 'unique_vendor_identifier':
                        unique_vendor_identifier, 'original_purchase_date_pst': purchase_date_pst,
                        'original_purchase_date': original_purchase_date, 'purchase_date_pst': purchase_date_pst,
                        'purchase_date': original_purchase_date, 'quantity': 1, 'original_transaction_id':
                        order_id, 'transaction_id': order_id}

        create_payment_history(**receipt_dict)
    else:
        raise ReceiptVerificationError('failed android receipt verification')


def create_payment_history(user_id='', store_product_id='', store_item_id='', shop_type='', unique_identifier='',
                           unique_vendor_identifier='', quantity=0, original_purchase_date_pst=datetime,
                           original_purchase_date=datetime, purchase_date_pst=datetime, purchase_date=datetime,
                           original_transaction_id='', transaction_id=''):
    PaymentHistory.objects.create(user_id=user_id, store_product_id=store_product_id,  # in_app_purchase item id
                                  store_item_id=store_item_id,  # (ios)application ID
                                  quantity=quantity,
                                  shop_type=shop_type,
                                  original_transaction_id=original_transaction_id,
                                  transaction_id=transaction_id,
                                  unique_identifier=unique_identifier,
                                  unique_vendor_identifier=unique_vendor_identifier,
                                  original_purchase_date_pst=original_purchase_date_pst,
                                  purchase_date_pst=purchase_date_pst,
                                  original_purchase_date=original_purchase_date,
                                  purchase_date=purchase_date)


def sanitize_receipt_json(receipt_json):
    clean_receipt_json = receipt_json.replace("\\\"", "\"")
    unwanted_quote_first_index = clean_receipt_json.index("{", 1) - 1
    new_receipt_string = clean_receipt_json[:unwanted_quote_first_index] + clean_receipt_json[unwanted_quote_first_index + 1:]
    unwanted_quote_second_index = new_receipt_string.index("}", 1) + 1
    new_complete_receipt_string = new_receipt_string[:unwanted_quote_second_index] + new_receipt_string[unwanted_quote_second_index + 1:]
    return new_complete_receipt_string


def convert_str_date_for_ios(str_date):
    date_array = separate_str_by_space(str_date)
    date_time = date_array[0] + ' ' + date_array[1]
    date = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    return date


def buy_tickets_html(request):
    other = 'buy_tickets'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'item_form': 'tickets', 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def buy_tickets(request, type_res):
    other = 'buy_tickets'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    context = RequestContext(request, {request: request, 'user': request.user})
    try:
        phone_id = request.POST['phone_id']
        ticket_type = int(request.POST['ticket_type'])  # 0:stamina 1:focus

        wuser = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)[0]

        if not wuser:
            error = get_properties(err_type="Error", err_code='ERR0023')
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        if not objectid.ObjectId.is_valid(wuser.id):
            error = get_properties(err_type='Error', err_code='ERR0008')
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        # exchange stamina potion with stamina
        if ticket_type == const.stamina_ticket:
            stamina_exchange_rate = ItemExchangeRate.objects.filter(ticket=const.stamina_ticket, delete_flag=False)[0]

            if wuser.stamina_potion < stamina_exchange_rate.ticket_price:
                error = get_properties(err_type='Error', err_code='ERR0064')
                res_dict = {'status': 'failed', 'function': other, 'Error': error}
                if type_res == 0:
                    return throw_error(template="home.html", obj_dict=res_dict, context=context)
                elif type_res == 1:
                    return throw_error_in_json(res_dict, phone_id)

            stamina_max = get_stamina_max(other, context, type_res)

            if wuser.ticket < int(stamina_max.value):
                wuser.ticket += stamina_exchange_rate.ticket_quantity
                wuser.stamina_potion -= stamina_exchange_rate.ticket_price
                if wuser.ticket > int(stamina_max.value):
                    wuser.ticket = int(stamina_max.value)
                wuser.save()
            else:
                error = get_properties(err_type='Error', err_code='ERR0063')
                res_dict = {'status': 'failed', 'function': other, 'Error': error}
                if type_res == 0:
                    return throw_error(template="home.html", obj_dict=res_dict, context=context)
                elif type_res == 1:
                    return throw_error_in_json(res_dict, phone_id)


    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    return get_playerstate(request=request, type_res=type_res)

