__author__ = 'yoshi.miyamoto'

import logging
from witches import const
from witches.utils.util import get_properties, throw_error, throw_error_in_json
from witches.models import *
from bson import ObjectId

logger = logging.getLogger(__name__)


def get_system_id(context, other):
    try:
        system = Characters.objects.get(first_name='K&C')
    except Characters.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0042")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        return throw_error(template="home.html", obj_dict=res_dict, context=context)

    return system.id


def send_item_to_user(item_id_list, message, user_id, currency_dict, context, other):
    sender_flag = False
    sender_type_for_metrics = get_sender_info_for_metrics(sender_flag)

    system_id = get_system_id(context, other)
    if len(item_id_list) > 0:
        if len(item_id_list) > 4:
            logger.debug('try to send less than or equal to 4 items at a time')

    premium = 0
    free = 0
    stamina_potions = 0

    if len(currency_dict) > 0:
        for currency_name in currency_dict:
            if currency_name == "starstones":
                premium = int(currency_dict[currency_name])
                if premium < 0:
                    premium = 0
            elif currency_name == "coins":
                free = int(currency_dict[currency_name])
                if free < 0:
                    free = 0
            elif currency_name == "stamina_potions":
                stamina_potions = int(currency_dict[currency_name])
                if stamina_potions < 0:
                    stamina_potions = 0

    UserMailBox.objects.create(user_id=user_id, gifts=item_id_list, title="", sender_flag=sender_flag,
                               message_body=message, sender_id=system_id, read_flag=False,
                               premium_currency=premium, free_currency=free, stamina_potion=stamina_potions,
                               login_bonus_id='', stamina_potion_received_flag=False,
                               premium_received_flag=False, free_currency_received_flag=False,
                               multiply_bonus_flag=False, sender_type_for_metrics=sender_type_for_metrics)


def send_all_items_to_user(message, user_id, item_type1, context, other):
    sender_flag = False
    sender_type_for_metrics = get_sender_info_for_metrics(sender_flag)

    system_id = get_system_id(context, other)
    premium = 0
    free = 0
    stamina_potions = 0

    if item_type1 == "avatar_items":
        all_items = AvatarItems.objects.filter(delete_flag=False).values_list('id', flat=True)
    elif item_type1 == "potions":
        all_items = Potions.objects.filter(delete_flag=False).values_list('id', flat=True)
    elif item_type1 == "ingredients":
        all_items = Ingredients.objects.filter(delete_flag=False).values_list('id', flat=True)

    item_id_list = []
    i = 0
    j = 0
    for item in all_items:
        item_id_list.append(item)
        i += 1
        if i == 4:
            UserMailBox.objects.create(user_id=user_id, gifts=item_id_list, title="", sender_flag=sender_flag,
                               message_body=message, sender_id=system_id, read_flag=False,
                               premium_currency=premium, free_currency=free, stamina_potion=stamina_potions,
                               login_bonus_id='', stamina_potion_received_flag=False,
                               premium_received_flag=False, free_currency_received_flag=False,
                               multiply_bonus_flag=False, sender_type_for_metrics=sender_type_for_metrics)
            i = 0
            item_id_list = []
        j += 1

        if j == len(all_items):
            UserMailBox.objects.create(user_id=user_id, gifts=item_id_list, title="", sender_flag=sender_flag,
                               message_body=message, sender_id=system_id, read_flag=False,
                               premium_currency=premium, free_currency=free, stamina_potion=stamina_potions,
                               login_bonus_id='', stamina_potion_received_flag=False,
                               premium_received_flag=False, free_currency_received_flag=False,
                               multiply_bonus_flag=False, sender_type_for_metrics=sender_type_for_metrics)

def convert_str_nullable_int(str_num):
    if str_num == 'None':
        return None
    else:
        return int(str_num)


def avoid_none_for_int(str_num):
    if str_num == 'None':
        return 0
    else:
        return int(str_num)


def get_sender_info_for_metrics(sender_flag):
    if sender_flag:
        sender_type_for_metrics = 'Character'
    else:
        sender_type_for_metrics = 'K&C'
    return sender_type_for_metrics


def get_sender_info(temp_mail_id, context, type_res):
    other = 'check_who_send_mail'
    try:
        mail = get_mail_template(temp_mail_id, other, context, type_res)
        phone_id = const.system_phone_id
    except EmailTemplates.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0043")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    try:
        character = Characters.objects.get(id=ObjectId(mail.sender_id), delete_flag=False)

    except Characters.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0042")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
    return character


def get_mail_template(mail_id, other, context, type_res):
    try:
        mail = EmailTemplates.objects.get(id=ObjectId(mail_id), delete_flag=False)
        phone_id = const.system_phone_id
    except EmailTemplates.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0043")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
    return mail

def is_sender_character(mail_id, context, type_res):
    sender = get_sender_info(mail_id, context, type_res)
    if sender.first_name == const.system_name:
        return False
    else:
        return True
#