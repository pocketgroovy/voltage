import os
import datetime
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from Voltage.witch_mail_config import get_environment
from witches.admintool.adm_mail import send_item_to_user, send_all_items_to_user, bulk_send_item_to_users
from witches.admintool.adm_util import throw_error, get_properties, get_user_id_from_phone_id
import logging
from witches.models import WUsers, Ingredients, Potions, AvatarItems

logger = logging.getLogger(__name__)


def home(request):
    context = RequestContext(request)
    ENVIRONMENT = get_environment('Env', 'environment')

    return render_to_response('admintool/adm_home.html', {'environment': ENVIRONMENT}, context_instance=context)


def deliver_window(request):
    context = RequestContext(request)
    ENVIRONMENT = get_environment('Env', 'environment')

    vpn_connection()

    users = WUsers.objects.filter(delete_flag=False)
    ingredients = Ingredients.objects.filter(delete_flag=False)
    potions = Potions.objects.filter(delete_flag=False)
    avatar_items = AvatarItems.objects.filter(delete_flag=False)
    return render_to_response('admintool/adm_deliver.html',
                              {'users': users, 'ingredients_list': ingredients, 'potions_list': potions,
                               'avatar_items_list': avatar_items, 'environment': ENVIRONMENT}, context_instance=context)


def vpn_connection():
    os.system(os.path.join(os.path.dirname(__file__), "../../../call_softlayer.sh"))


def is_selection_currency(item_dict):
    for item_type in item_dict:
        if item_type:
            if item_type == "starstones" or item_type == "coins" or item_type == "stamina_potions":
                return True
            else:
                return False
        else:
            return False


def gather_currencies_in_dict(item_list):
    currency_dict = {}
    for item in item_list:
        if is_selection_currency(item_list[item]):
            for key in item_list[item]:
                if currency_dict.has_key(key):
                    new_num = currency_dict[key] + item_list[item][key]
                else:
                    new_num = item_list[item][key]
                currency_dict[key] = new_num
            currency_dict.update({item: item_list[item]})

    return currency_dict


def gather_selected_item_list(request):
    sel_item_ids_list1 = request.POST.getlist('sel_item_ids1[]')
    sel_item_ids_list2 = request.POST.getlist('sel_item_ids2[]')
    sel_item_ids_list3 = request.POST.getlist('sel_item_ids3[]')
    item_id_list = []
    if len(sel_item_ids_list1) > 0:
        for id in sel_item_ids_list1:
            if id:
                item_id_list.append({'id': id, 'received_flag': False})

    if len(sel_item_ids_list2) > 0:
        for id in sel_item_ids_list2:
            if id:
                item_id_list.append({'id': id, 'received_flag': False})

    if len(sel_item_ids_list3) > 0:
        for id in sel_item_ids_list3:
            if id:
                item_id_list.append({'id': id, 'received_flag': False})
    return item_id_list


def get_user_ids(request):
    phone_id1 = request.POST.get('phone_id1')
    phone_id2 = request.POST.get('phone_id2')
    phone_id3 = request.POST.get('phone_id3')
    phone_id4 = request.POST.get('phone_id4')

    platform = request.POST.get('platform')

    if platform:
        filterArgs = {'delete_flag': False}
        
        if platform and platform != 'All':
            filterArgs['device'] = platform
            
        user_ids = WUsers.objects.filter(**filterArgs).values_list('id', flat=True)
    else:
        user_ids = []

    if phone_id1:
        user_id = get_user_id_from_phone_id(phone_id1)
        user_ids.append(user_id)
    if phone_id2:
        user_id2 = get_user_id_from_phone_id(phone_id2)
        user_ids.append(user_id2)
    if phone_id3:
        user_id3 = get_user_id_from_phone_id(phone_id3)
        user_ids.append(user_id3)
    if phone_id4:
        user_id4 = get_user_id_from_phone_id(phone_id4)
        user_ids.append(user_id4)

    return user_ids


def is_any_selected(item_id_list, currencies):
    if len(item_id_list) > 0:
        return True
    elif len(currencies) > 0:
        return True
    else:
        return False


def deliver(request):
    context = RequestContext(request)
    other = 'deliver'
    start = datetime.datetime.now()

    if request.POST:
        quantity1 = request.POST.get('quantity1')
        quantity2 = request.POST.get('quantity2')
        quantity3 = request.POST.get('quantity3')
        item_type1 = request.POST.get('item_type1')
        item_type2 = request.POST.get('item_type2')
        item_type3 = request.POST.get('item_type3')

        if not quantity1:
            quantity1 = 0
        if not quantity2:
            quantity2 = 0
        if not quantity3:
            quantity3 = 0

        item_list = {1: {item_type1: int(quantity1)}, 2: {item_type2: int(quantity2)}, 3: {item_type3: int(quantity3)}}

        user_ids = get_user_ids(request)
        item_id_list = gather_selected_item_list(request)
        currencies = gather_currencies_in_dict(item_list)

        all_items = request.POST.get('check_all_items')
        message = request.POST.get('message')

        if len(currencies) > 0:
            currency_dict = currencies
        else:
            currency_dict = {}

        if len(user_ids) > 0:
            if not all_items:
                if is_any_selected(item_id_list, currency_dict):
                    bulk_send_item_to_users(item_id_list, message, user_ids, currency_dict, context, other)
                else:
                    Error = get_properties(err_type='Error', err_code='ERR1001')
                    res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                    return throw_error(template='admintool/adm_deliver.html', context=context, obj_dict=res_dict)
            elif not item_type1:
                Error = get_properties(err_type='Error', err_code='ERR1002')
                res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                return throw_error(template='admintool/adm_deliver.html', context=context, obj_dict=res_dict)

            sent_items = {'item_list': item_id_list}
            if currency_dict != {}:
                sent_items.update(currency_dict)
        else:
            Error = get_properties(err_type='Error', err_code='ERR1000')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            return throw_error(template='admintool/adm_deliver.html', context=context, obj_dict=res_dict)

        end = datetime.datetime.now()
        print("time spent: " + str(end-start))
        return render_to_response('admintool/adm_deliver.html', {'recipients': user_ids, 'sent_item': sent_items},
                                  context_instance=context)
