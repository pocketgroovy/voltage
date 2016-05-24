__author__ = 'yoshi.miyamoto'

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from pymongo.errors import ConnectionFailure
from models import *
from utils.util import get_properties, throw_error, throw_error_in_json
from utils.util import date_handler
import json
import logging
import const
from witches.utils.custom_exceptions import BuildVersionFormatError

logger = logging.getLogger(__name__)

const.pw_length = 4

# ticket type
const.stamina_ticket = 0
const.closet_ticket = 2

# currency type
const.currency_coin = 0
const.currency_stamina_potion = 1
const.currency_stone = 2

# mail sender type
const.system = 0
const.chara = 1
const.system_name = 'K&C'

const.received = 'received'
const.stamina_potion_flag = 'stamina_potion_received_flag'
const.premium_flag = 'premium_received_flag'
const.free_flag = 'free_currency_received_flag'

# item type
const.type_ingredient = 0
const.type_avatar = 1
const.type_coordinate = 2
const.type_closet = 3
const.type_potion = 4

const.complete_level = 3
const.howtos_mail_scene = 'FIRST_MAIL_PICKEDUP'

const.system_phone_id = 'system_temp_phone_id'

# seconds in hour
const.seconds_in_hour = 3600

const.current_api_vers = 'current'
const.historical_api_vers = 'historical'
const.sandbox_receipt = 21007
const.receipt_verified = 0

const.admintool = 'admintool'

# login bonus
const.current_index = 1


def ping(request, type_res):
    other = 'ping'
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    context = RequestContext(request, {request: request, 'user': request.user})

    res_dict = {'status': 'success'}
    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_dict, 'function': other}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')


def environment_html(request):
    other = 'get_environment'

    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'environment',
                                       'item_form': 'environment', 'action': other, 'type_res': 0})
    try:
        return render_to_response('home.html', context_instance=context)
    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')


"""
this is used for unittesting for versioning
"""
@never_cache
@csrf_exempt
def get_environment_v2(request, type_res):
    other = 'get_environment2'
    logging.debug("version 2")

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    res_obj = {'status': 'success', 'version': 'B'}
    context = RequestContext(request, {request: request, 'user': request.user})

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_obj, 'function': other}, context_instance=context)
    elif type_res == 1:
        urls_json = json.dumps(res_obj, default=date_handler)
        return HttpResponse(urls_json, content_type='application/json')

@never_cache
@csrf_exempt
def get_environment(request, type_res):
    other = 'get_environment'

    logging.debug("version 1")

    phone_id = const.system_phone_id

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    res_obj = {}

    try:
        build_version = request.POST['build']
        device = request.POST['device']

        context = RequestContext(request, {request: request, 'user': request.user})

        urls = Environment.objects.filter(build_version=build_version, device=device, delete_flag=False)

        if urls.count() == 1:
            res_obj = {'status': 'success', 'base_url': urls[0].base_url, 'latest': True, 'metrics': urls[0].metrics,
                       'obb_path': urls[0].obb_path}

        elif urls.count() > 1:  # if there is more than 1 url associated with the version and the device, production url should be used
            try:
                production_url = urls.get(build_version=build_version, device=device, description='prod')
                res_obj = {'status': 'success', 'base_url': production_url.base_url, 'latest': True,
                           'metrics': production_url.metrics,
                           'obb_path': production_url.obb_path}
            except Environment.DoesNotExist:
                error = get_properties(err_type="Error", err_code="ERR0026")
                res_dict = {'status': 'failed', 'function': other, 'Error': error}
                if type_res == 0:
                    return throw_error(template="home.html", obj_dict=res_dict, context=context)
                elif type_res == 1:
                    return throw_error_in_json(res_dict, phone_id)

        else:  # the version hasn't been found in the database
            versioning = build_version.split("_")
            try:
                environment = versioning[1]
                try:
                    server_url = Environment.objects.get(device=device, description=environment, delete_flag=False)
                    res_obj = {'status': 'success', 'base_url': server_url.base_url, 'latest': True,
                               'metrics': server_url.metrics,
                               'obb_path': server_url.obb_path}

                except Environment.DoesNotExist:
                    error = get_properties(err_type="Error", err_code="ERR0030")
                    res_dict = {'status': 'failed', 'function': other, 'Error': error}
                    if type_res == 0:
                        return throw_error(template="home.html", obj_dict=res_dict, context=context)
                    elif type_res == 1:
                        return throw_error_in_json(res_dict, phone_id)

            except Exception as e:
                try:
                    prod = Environment.objects.filter(device=device, description='prod', delete_flag=False)
                    # prod_versions = prod.build_version.split(".")
                    # versions = versioning[0].split(".")
                    # try:
                    #     check_build_version_format(versions)
                    # except BuildVersionFormatError as e:
                    #     res_dict = {'status': 'failed', 'function': 'environment', 'Error': str(e)}
                    #     if type_res == 0:
                    #         return throw_error(template="home.html", obj_dict=res_dict, context=context)
                    #     elif type_res == 1:
                    #         return throw_error_in_json(res_dict, phone_id)
                    #
                    # if len(versions) < 3:
                    #     error = get_properties(err_type="Error", err_code="ERR0031")
                    #     res_dict = {'status': 'failed', 'function': 'environment', 'Error': error}
                    #     if type_res == 0:
                    #         return throw_error(template="home.html", obj_dict=res_dict, context=context)
                    #     elif type_res == 1:
                    #         return throw_error_in_json(res_dict, phone_id)
                    #
                    # # if the version is smaller than the production, prod url should be used, and tell client it's not latest
                    # if not is_versions_larger_than_prod(versions, prod_versions):
                    res_obj = {'status': 'success', 'base_url': prod[0].base_url, 'latest': False,
                               'metrics': prod[0].metrics,
                               'obb_path': prod[0].obb_path} # we might want to remove extra fields for old users

                    # # if build version is greater than any of the version numbers in database, dev url should be used
                    # else:
                    #     try:
                    #         dev_url = Environment.objects.get(device=device, description='d', delete_flag=False)
                    #         res_obj = {'status': 'success', 'base_url': dev_url.base_url, 'latest': True,
                    #                    'metrics': dev_url.metrics,
                    #                    'obb_path': dev_url.obb_path}
                    #
                    #     except Environment.DoesNotExist:
                    #         error = get_properties(err_type="Error", err_code="ERR0027")
                    #         res_dict = {'status': 'failed', 'function': other, 'Error': error}
                    #         if type_res == 0:
                    #             return throw_error(template="home.html", obj_dict=res_dict, context=context)
                    #         elif type_res == 1:
                    #             return throw_error_in_json(res_dict, phone_id)

                except Environment.DoesNotExist:
                    error = get_properties(err_type="Error", err_code="ERR0026")
                    res_dict = {'status': 'failed', 'function': other, 'Error': error}
                    if type_res == 0:
                        return throw_error(template="home.html", obj_dict=res_dict, context=context)
                    elif type_res == 1:
                        return throw_error_in_json(res_dict, phone_id)

        request.session['environment'] = res_obj

        context = RequestContext(request, {request: request, 'user': request.user, 'option': 'environment',
                                           'action': other, 'type_res': 0})
        if type_res == 0:
            return render_to_response("home.html", {'res_obj': res_obj, 'function': other}, context_instance=context)
        elif type_res == 1:
            urls_json = json.dumps(res_obj, default=date_handler)
            return HttpResponse(urls_json, content_type='application/json')

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, '')

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)


def check_build_version_format(build_version):
    for version in build_version:
        if version == '':
            error = get_properties(err_type="Error", err_code="ERR0061")
            raise BuildVersionFormatError(error)


def is_versions_larger_than_prod(versions, prod_versions):  # exactly the same version won't need this function
    if int(versions[0]) > int(prod_versions[0]):  # compare major number
        return True
    elif int(versions[0]) < int(prod_versions[0]):
        return False
    elif int(versions[1]) > int(prod_versions[1]):  # compare minor number
        return True
    elif int(versions[1]) < int(prod_versions[1]):
        return False
    elif int(versions[2]) > int(prod_versions[2]):  # compare patch number
        return True
    else:
        return False


def get_books_list_from_scenetable():
    scenes = list(SceneTable.objects.filter(delete_flag=False))
    book_unlock_dict = {}
    if scenes.__len__() < 1:
        raise SceneTable.DoesNotExist
    else:
        for scene in scenes:
            if scene.book_id:
                book_unlock_dict[scene.scene_path] = scene.book_id

    return book_unlock_dict

@never_cache
@csrf_exempt
def get_all_master(request, other=None, type_res=0):
    try:
        if type_res:
            type_res = int(type_res)
        else:
            type_res = 0

        phone_id = const.system_phone_id
        context = RequestContext(request, {request: request, 'user': request.user})

        try:
            version = GameProperties.objects.get(name='version')
        except GameProperties.DoesNotExist:
            Error = get_properties(err_type='Error', err_code='ERR0040')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        if 'mst_dict' in cache:
            cache_mst_dict = cache.get('mst_dict')
            if not cache_mst_dict.get('version') == version.value:
                cache.delete('mst_dict')
                set_master_config_cache(phone_id, version, type_res, other, context)
        else:
            set_master_config_cache(phone_id, version, type_res, other, context)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    if type_res == 0:
        cache_mst_dict = cache.get('mst_dict')
        return render_to_response("home.html", {'res_obj': cache_mst_dict, 'function': other}, context_instance=context)
    elif type_res == 1:
        cache_mst_dict = json.dumps(cache.get('mst_dict'), default=date_handler)
        return HttpResponse(cache_mst_dict, content_type='application/json')


def set_master_config_cache(phone_id, version, type_res, other, context):
        ticket_refresh_rate = GameProperties.objects.get(name='default_ticket_Refresh_Rate', delete_flag=False)
        max_tickets = GameProperties.objects.get(name='max_tickets', delete_flag=False)
        ingredient_mst = list(Ingredients.objects.filter(delete_flag=False).values())
        book_mst = list(Books.objects.filter(delete_flag=False).values())
        affinity_mst = list(Affinities.objects.filter(delete_flag=False).values())
        game_mst = list(
                GameProperties.objects.filter(delete_flag=False).exclude(name='default_howtos_mail').values())  # exclude this to avoid conflict with client parsing
        category_mst = list(Categories.objects.filter(delete_flag=False).values())

        shop_items_mst = list(ShopItems.objects.filter(delete_flag=False).values())
        characters_mst = list(Characters.objects.filter(delete_flag=False).values())
        potions_mst = list(Potions.objects.filter(delete_flag=False).values())
        recipes_mst = list(Recipes.objects.filter(delete_flag=False).values())
        avatar_items_mst = list(AvatarItems.objects.filter(delete_flag=False).values())
        book_prizes = list(BookPrizes.objects.filter(delete_flag=False).values())
        try:
            book_unlock_list = get_books_list_from_scenetable()
        except SceneTable.DoesNotExist:
            Error = get_properties(err_type='Error', err_code='ERR0068')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        mst_dict = {'status': 'success', 'version': version.value, 'ticketRefreshRate': ticket_refresh_rate.value,
                    'ingredient_mst': ingredient_mst, 'book_mst': book_mst, 'game_mst': game_mst,
                    'category_mst': category_mst, 
                    'affinity_mst': affinity_mst,'shop_items_mst': shop_items_mst,
                    'characters_mst': characters_mst, 'potions_mst': potions_mst, 'recipes_mst': recipes_mst,
                    'avatar_items_mst': avatar_items_mst, 
                    'book_prizes': book_prizes, 'max_tickets': max_tickets.value, 'book_unlock': book_unlock_list}

        print(mst_dict)

        # set master dic with unique key in redis cache
        cache.set('mst_dict', mst_dict, 1000)


def get_type_res(type_res):
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0
    return type_res


def get_stamina_max_routine():
    return int(GameProperties.objects.get(name='max_tickets', delete_flag=False).value)


def get_stamina_max(other, context, type_res):
    phone_id = const.system_phone_id
    try:
        stamina_max = GameProperties.objects.get(name='max_tickets', delete_flag=False)

    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0035")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    return stamina_max

    
def get_stamina_refresh_rate(): # return in min
    return int(GameProperties.objects.get(name='default_ticket_Refresh_Rate', delete_flag=False).value)


def get_stamina_refresh_rate_from_db(other, context, type_res):  # return in min
    phone_id = const.system_phone_id
    try:
        stamina_refresh_rate = GameProperties.objects.get(name='default_ticket_Refresh_Rate', delete_flag=False)

    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0037")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    return stamina_refresh_rate


def get_howtos_mail(other, context, type_res):
    phone_id = const.system_phone_id
    try:
        howtos_mail = GameProperties.objects.get(name='default_howtos_mail', delete_flag=False)
    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0062")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
    return howtos_mail


# This naming is due to the need to preserve the old copy. Eventually, get_item_exchange_rate should be unnecessary,
#  and all these kind of routines can be handled in this kind of simple manner
def get_item_exchange_rate_routine(ticket_number):
    return ItemExchangeRate.objects.get(ticket=ticket_number, delete_flag=False)


def get_item_exchange_rate(ticket_number, other, context, type_res):
    phone_id = const.system_phone_id
    try:
        exchange_rate = ItemExchangeRate.objects.get(ticket=ticket_number, delete_flag=False)
    except ItemExchangeRate.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0057")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
    return exchange_rate


def get_login_bonus_interval_in_sec(phone_id):
    function = 'get_login_bonus_interval_in_sec'
    try:
        # interval is in minutes
        login_bonus_interval = GameProperties.objects.get(name='login_bonus_interval', delete_flag=False)
    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0090")
        res_dict = {'status': 'failed', 'function': function, 'Error': error}
        return throw_error_in_json(res_dict, phone_id)
    return int(login_bonus_interval.value) * 60


def get_login_bonus_list(index_list):
    item_list = []
    for item in LogInBonusesMaster.objects.filter(bonus_index__in=index_list):
        item_list.append(item)

    return item_list


def get_shop_item(product_id):
    try:
        currency_item = ShopItems.objects.get(product_id=product_id, delete_flag=False)
        return currency_item
    except ShopItems.DoesNotExist:
        Error = get_properties(err_type='Error', err_code='ERR0029')
        return {'status': 'failed', 'function': 'get_shop_item', 'Error': Error}
