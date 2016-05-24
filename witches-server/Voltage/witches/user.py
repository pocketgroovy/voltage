__author__ = 'carlos.matsumoto', 'yoshi.miyamoto'

from pymongo.errors import ConnectionFailure
from witches.utils.user_util import get_parameter_for_sync_resources, get_user, \
    get_parameter_for_update_playerstorystate
from witches.book import check_user_book_completeness
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from witches.utils.util import get_properties, throw_error, get_total_seconds_for_update, \
    get_time_diff_in_seconds, throw_error_in_json, convert_seconds_to_datetime, get_now_datetime, \
    get_next_update_delta, convert_datetime_to_seconds, get_current_time_from_request, \
    get_story_reset_flag_from_request, get_login_bonus_flag_from_request, log_out_of_sync_error, \
    sync_resource_error_message, sync_resource_error_message_max
from models import *
from bson import objectid
from utils.util import date_handler
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from witches.master import get_item_exchange_rate, get_type_res, get_item_exchange_rate_routine
from witches.master import get_stamina_max, get_stamina_max_routine
from witches.master import get_stamina_refresh_rate_from_db, get_stamina_refresh_rate
from witches.utils.user_util import get_id_from_phone_id, get_phone_id_from_request, get_first_last_name_from_request
import datetime

import collections
import json
import logging
import random
import string
import const

import traceback


logger = logging.getLogger(__name__)


def get_playerstate_html(request):
    other = 'get_playerstate'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


# expects a POST request
@csrf_exempt
def get_playerstate(request, type_res, extra_parms=None):
    other = 'get_playerstate'
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    context = RequestContext(request, {request: request, 'user': request.user})

    try:
        phone_id = get_phone_id_from_request(request, other, context, type_res)
        context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id'})
        wuser = get_user(phone_id)

        is_story_reset = get_story_reset_flag_from_request(request)
        current_time_in_sec = get_current_time_from_request(request)
        bonus_ineligible = get_login_bonus_flag_from_request(request)

        if objectid.ObjectId.is_valid(wuser.id):
            currency = wuser.free_currency
            premium_currency = wuser.premium_currency
            stamina = wuser.ticket
            closet = wuser.closet
            user_scene_id = wuser.scene_id
            user_node_id = wuser.node_id
            stamina_potion = wuser.stamina_potion
            first_name = wuser.first_name
            last_name = wuser.last_name
            user_id = wuser.phone_id
            howtos_scene_id = wuser.howtos_scene_id
            is_in_tutorial = wuser.tutorial_flag
            tutorial_progress = wuser.tutorial_progress
            current_outfit_ids = wuser.current_outfit
            if current_outfit_ids:
                current_outfit_records = AvatarItems.objects.filter(id__in=current_outfit_ids)
                current_outfit = [x.layer_name for x in current_outfit_records]
            else:
                current_outfit = []

            if wuser.ticket_last_update:
                ticket_last_update = wuser.ticket_last_update
                last_update_time_in_sec = convert_datetime_to_seconds(ticket_last_update)
                stamina_next_update_delta = get_next_update_delta('stamina', current_time_in_sec, last_update_time_in_sec,
                                                                 other, context, type_res)
            else:
                ticket_last_update = convert_seconds_to_datetime(0)
                stamina_next_update_delta = 0
            inventories = UserItemInventory.objects.filter(user_id=wuser.id, delete_flag=False)
            user_books = UserBooks.objects.filter(user_id=wuser.id, delete_flag=False)

            if user_books.count() > 0:
                books = user_books[0].book_list

            mails = UserMailBox.objects.filter(user_id=wuser.id, read_flag=False, delete_flag=False)
            avatar_items = UserAvatarItemsInCloset.objects.filter(user_id=wuser.id, delete_flag=False)

            user_character_list = []
            affinity = 0

            try:
                characters = UserCharacters.objects.get(user_id=wuser.id, delete_flag=False)

                if characters.affinities:
                    character_dict = {'affinities': characters.affinities}
                    user_character_list.append(character_dict)

                affinity_value = 0
                if not is_story_reset:
                    for key in characters.affinities.keys():
                        try:  # catch if value is not int
                            affinity_value += int(characters.affinities[key])
                            wuser.total_affinity = affinity_value
                        except ValueError:
                            continue

                wuser.save()
                affinity = wuser.total_affinity
            except UserCharacters.DoesNotExist:
                logger.debug('seems like create user call didn\'t create characters list for this user [' + phone_id + ']')

        else:
            Error = get_properties(err_type='Error', err_code='ERR0008')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        inventory_dict = {}
        for inventory in inventories:
            if inventory.ingredient_id and not inventory.potion_id:
                inventory_dict[inventory.ingredient_id] = inventory.quantity
            elif inventory.potion_id and not inventory.ingredient_id:
                inventory_dict[inventory.potion_id] = inventory.quantity

        # avatar items are stored in inventory due to client parsing
        for avatar_item in avatar_items:
            if avatar_item.avatar_item_id:
                inventory_dict[avatar_item.avatar_item_id] = avatar_item.quantity

        user_book_array = []
        try:
            books
            if isinstance(books, collections.Iterable):
                # get user book list and get if is complete, it recipes and id
                for book in books:
                    if objectid.ObjectId.is_valid(book):
                        try:
                            user_book_array.append(check_user_book_completeness(book, wuser))

                        except Books.DoesNotExist:
                            Error = get_properties(err_type='Error', err_code='ERR0041')
                            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                            if type_res == 0:
                                return throw_error(template="home.html", obj_dict=res_dict, context=context)
                            elif type_res == 1:
                                return throw_error_in_json(res_dict, phone_id)
                            return throw_error(template="home.html", obj_dict=res_dict, context=context)

                    else:
                        Error = get_properties(err_type='Error', err_code='ERR0013')
                        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                        if type_res == 0:
                            return throw_error(template="home.html", obj_dict=res_dict, context=context)
                        elif type_res == 1:
                            return throw_error_in_json(res_dict, phone_id)
                        return throw_error(template="home.html", obj_dict=res_dict, context=context)

            else:
                if books is not None:
                    if objectid.ObjectId.is_valid(books):
                        try:
                            user_book_array = check_user_book_completeness(books, wuser)

                        except Books.DoesNotExist:
                            Error = get_properties(err_type='Error', err_code='ERR0041')
                            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                            if type_res == 0:
                                return throw_error(template="home.html", obj_dict=res_dict, context=context)
                            elif type_res == 1:
                                return throw_error_in_json(res_dict, phone_id)
                            return throw_error(template="home.html", obj_dict=res_dict, context=context)

                    else:
                        Error = get_properties(err_type='Error', err_code='ERR0013')
                        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                        if type_res == 0:
                            return throw_error(template="home.html", obj_dict=res_dict, context=context)
                        elif type_res == 1:
                            return throw_error_in_json(res_dict, phone_id)
                        return throw_error(template="home.html", obj_dict=res_dict, context=context)

        except NameError:
            Error = get_properties(err_type='Error', err_code='ERR0041')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        available_scenes = []  # could be used for future use(requested by Michael C.)

        completed_scenes = UserCompletedScenes.objects.filter(user_id=wuser.id, delete_flag=False)
        completed_scenes_list = []
        if completed_scenes.__len__() > 0:
            for completed_scene in completed_scenes:
                completed_scenes_list.append(completed_scene.scene_id)

        if bonus_ineligible:
            login_bonus_items = []
        else:
            login_bonus_items = wuser.login_bonus_items

        res_dict = {'status': 'success', 'currency': currency, 'premium_currency': premium_currency, 'stamina_potion': stamina_potion,
                    'total_affinity': affinity, 'stamina': stamina, 'stamina_last_update':ticket_last_update,
                    'inventory': inventory_dict, 'books': user_book_array, 'mail_badge': mails.count(),
                    'closet_space': closet, 'character_affinities': characters.affinities,
                    'current_outfit': current_outfit, 'scene_id': user_scene_id,
                    'node_id': user_node_id, 'first_name': first_name, 'last_name': last_name, 'phone_id': user_id,
                    'howtos_scene_id': howtos_scene_id, 'tutorial_flag': is_in_tutorial, 'available_scenes': available_scenes,
                    'completed_scenes': completed_scenes_list, 'tutorial_progress': tutorial_progress,
                    'stamina_next_update_delta': stamina_next_update_delta,
                    'login_bonus_items': login_bonus_items}

        if extra_parms:
            res_dict.update(extra_parms)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

    except Exception as e:
        phone_id = const.system_phone_id
        logger.error(str(e))
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_dict, 'function': other}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')


def get_restore_response(request):   
    # db = "support"      # can move into a config

    context = RequestContext(request, {request: request, 'user': request.user})
    phone_id = get_phone_id_from_request(request, "get_restore_response", context, 1)

    try:
        wuser = get_user(phone_id)      # can user be retrieved from request.user?
        update_entry = UserClientUpdateJson.objects.get(phone_id=phone_id)        
        
        player_json = json.loads(update_entry.playerjson)
        # player_json['login_bonus_items'] = get_bonus_items(request)

        response = {}
        response['status'] = 'success'
        response['restore_json'] = player_json
        response['login_bonus_items'] = get_bonus_items(request, wuser)

        # cleanup
        wuser.update_client = False
        wuser.save()
        update_entry.delete()

        logger.debug("user::get_restore_response > restoring player: {0}".format(phone_id))
        return HttpResponse(json.dumps(response), content_type='application/json')


    except ConnectionFailure as e:
        return throw_error_in_json({'status': 'failed', 'Error': str(e)}, 'maintenence')

    except Exception as e:
        trace = traceback.format_exc()
        logger.error("user::get_restore_response > {0}\n{1}".format(str(e), trace))
        return get_playerstate(request, 1)      # on failure, allow player to continue play with existing JSON
        # return throw_error_in_json({'status': 'failed', 'Error': str(e)}, phone_id)


    

def get_bonus_items(request, wuser):
    bonus_eligible = not get_login_bonus_flag_from_request(request)

    login_bonus_items = []
    if bonus_eligible:
        login_bonus_items = wuser.login_bonus_items

    return login_bonus_items


def get_password_html(request):
    other = 'get_password'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def get_password(request, type_res):
    other = 'get_password'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0
    try:
        try:
            phone_id = request.POST['phone_id']

            context = RequestContext(request, {request: request, 'user': request.user})

        except Exception as e:
            phone_id = const.system_phone_id
            res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        user_password = generate_password(const.pw_length)
        is_not_unique_pw = True

        while is_not_unique_pw:
            try:
                WUsers.objects.get(phone_id=phone_id, password=user_password, delete_flag=False)
                user_password = generate_password(const.pw_length)
            except WUsers.DoesNotExist:
                is_not_unique_pw = False

        try:
            wuser = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)[0]
            wuser.password = user_password
            wuser.password_date = get_now_datetime()
            wuser.save()

            user_dict = {'user_id': wuser.phone_id, 'password': wuser.password, 'status': 'success'}
        except Exception as e:
            logger.error(e.message)
            res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': user_dict, 'function': other}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(user_dict, default=date_handler), content_type='application/json')


def generate_password(length):
    key = ''
    for i in range(length):
        key += random.choice(string.lowercase + string.uppercase + string.digits)
    return key


def restore_html(request):
    other = 'set_restore_ids'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def set_restore_ids(request, type_res):
    other = 'start_restore'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0
    try:
        try:
            new_id = request.POST['phone_id']

            context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                               'phone_id': new_id, 'action': other, 'item_form': 'restore', 'type_res': 0})

        except Exception as e:
            phone_id = const.system_phone_id
            res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

    user_dict = {'res_obj': {}, 'function': other}

    if type_res == 0:
        return render_to_response("home.html", context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(user_dict, default=date_handler), content_type='application/json')

@csrf_exempt
def start_restore(request, type_res):
    other = 'start_restore'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0
    try:
        try:
            restored_id = request.POST['phone_id']
            password = request.POST['password']

            context = RequestContext(request, {request: request, 'user': request.user})

        except Exception as e:
            phone_id = const.system_phone_id
            res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        try:
            original_user = WUsers.objects.get(phone_id=restored_id, password=password, delete_flag=False)

            original_user.password = None
            original_user.save()

        except WUsers.DoesNotExist:
            phone_id = restored_id
            error = get_properties(err_type="Error", err_code="ERR0023")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

    return get_playerstate(request, type_res)

def use_potion_html(request):
    other = 'use_potion'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'use_potion', 'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def use_potion(request, type_res):
    other = 'use_potion'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0
    try:
        try:
            phone_id = request.POST['phone_id']
            potion_id = request.POST['potion_id']

            context = RequestContext(request, {request: request, 'user': request.user})

        except Exception as e:
            phone_id = const.system_phone_id
            res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        try:
            user = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)[0]

        except WUsers.DoesNotExist:
            error = get_properties(err_type="Error", err_code="ERR0023")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        try:
            user_potion = UserItemInventory.objects.filter(user_id=user.id, potion_id=potion_id, delete_flag=False)
            user_potion_num = user_potion.count()

            if user_potion_num > 0:
                user_potion[0].delete()
            else:
                log_out_of_sync_error('FUNCTION: "use_potion", user doesn\'t have this potion:' + potion_id, phone_id)

        except UserItemInventory.DoesNotExist:
            error = get_properties(err_type="Error", err_code="ERR0025")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

    return get_playerstate(request, type_res)


def use_stamina_html(request):
    other = 'use_stamina'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def use_stamina(request, type_res):
    other = 'use_stamina'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0
    try:
        try:
            phone_id = request.POST['phone_id']

            context = RequestContext(request, {request: request, 'user': request.user})

        except Exception as e:
            phone_id = const.system_phone_id
            res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        handle_stamina_regeneration(request, type_res)

        try:
            user = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)[0]

        except WUsers.DoesNotExist:
            error = get_properties(err_type="Error", err_code="ERR0023")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        user_ticket_num = user.ticket

        stamina_max = get_stamina_max(other, context, type_res)

        if user_ticket_num > 0:
            if user_ticket_num == int(stamina_max.value):
                user.ticket_last_update = get_now_datetime()
            user_ticket_num -= 1
            user.ticket = user_ticket_num
            user.save()
        else:
            error = get_properties(err_type="Warning", err_code="WAR0018")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

    return get_playerstate(request, type_res)


def use_ingredient_html(request):
    other = 'prep_ingredient'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'prep_ingredient', 'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def prep_ingredient(request, type_res):
    other = 'use_ingredient'

    phone_id = request.POST['phone_id']
    ingredient1 = request.POST['ingredient1']
    ingredient2 = request.POST['ingredient2']
    ingredient3 = request.POST['ingredient3']
    ingredient4 = request.POST['ingredient4']

    ingredients_list = []

    ingredients = {ingredient1, ingredient2, ingredient3, ingredient4}

    for ingredient in ingredients:
        if ingredient:
            ingredients_list.append(ingredient)

    context = RequestContext(request, {request: request, 'user': request.user})

    try:
        WUsers.objects.get(phone_id=phone_id, delete_flag=False)

    except WUsers.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0023")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'json_obj': json.dumps(ingredients_list), 'item_form': 'use_ingredient',
                                       'action': other, 'type_res': 0, 'phone_id': phone_id})

    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def use_ingredient(request, type_res):
    other = 'use_ingredient'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        context = RequestContext(request, {request: request, 'user': request.user})
        phone_id = request.POST["phone_id"]

    except Exception as e:
        phone_id = const.system_phone_id
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    user_id = get_id_from_phone_id(phone_id)

    if request.POST.get("ingredients"):
        ingredients_json = request.POST["ingredients"]
        ingredients_list = json.loads(ingredients_json)

    try:
        for ingredient_id in ingredients_list:
            if ingredient_id:
                try:
                    user_ingredient = UserItemInventory.objects.get(~Q(quantity=0), user_id=user_id, delete_flag=False,
                                                                    ingredient_id=ingredient_id)

                    try:  # check if there is the ingredient in master data
                        ingredient = Ingredients.objects.get(id=ingredient_id, delete_flag=False)

                        # if ingredient is not default one, decrease the number in the inventory
                        if not ingredient.isInfinite:
                            user_ingredient.quantity -= 1
                            user_ingredient.save()

                        if user_ingredient.quantity == 0:
                            user_ingredient.delete()

                    except Ingredients.DoesNotExist:
                        error = get_properties(err_type="Warning", err_code="WAR0010")
                        res_dict = {'status': 'failed', 'function': other, 'Error': error}
                        if type_res == 0:
                            return throw_error(template="home.html", obj_dict=res_dict, context=context)
                        elif type_res == 1:
                            return throw_error_in_json(res_dict, phone_id)

                except UserItemInventory.DoesNotExist:
                    error = get_properties(err_type="Warning", err_code="WAR0002")
                    res_dict = {'status': 'failed', 'function': other, 'Error': error}
                    if type_res == 0:
                        return throw_error(template="home.html", obj_dict=res_dict, context=context)
                    elif type_res == 1:
                        return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    return get_playerstate(request, type_res)


def playerstorystate_entry_html(request):
    other = 'playerstorystate_affinities'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'playerstorystate_affinities', 'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

def playerstorystate_affinities(request):
    other = 'playerstorystate_choices'
    char1 = request.POST['char_init1']
    char2 = request.POST['char_init2']
    char3 = request.POST['char_init3']
    affinity1 = request.POST['affinity1']
    affinity2 = request.POST['affinity2']
    affinity3 = request.POST['affinity3']
    affinities = {char1: affinity1, char2: affinity2, char3: affinity3}

    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'playerstorystate_choices', 'action': other, 'type_res': 0,
                                       'json_obj': json.dumps(affinities)})
    return render_to_response('home.html', context_instance=context)

def playerstorystate_choices(request):
    other = 'update_playerstorystate'

    if request.POST.get("affinities"):
        affinities_json = request.POST["affinities"]

    selection_id1 = request.POST['selection_id1']
    selection_id2 = request.POST['selection_id2']
    selection_id3 = request.POST['selection_id3']
    choice1 = request.POST['choice1']
    choice2 = request.POST['choice2']
    choice3 = request.POST['choice3']
    choices = {selection_id1: choice1, selection_id2: choice2, selection_id3: choice3}

    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'update_playerstorystate', 'action': other, 'type_res': 0,
                                       'json_choice': json.dumps(choices), 'json_aff': affinities_json})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def update_playerstorystate(request, type_res):
    other = 'update_playerstorystate'
    context = RequestContext(request, {request: request, 'user': request.user})

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    if request.POST.get("affinities"):
        affinities_json = request.POST["affinities"]
        affinities_dict = json.loads(affinities_json)

    try:
        phone_id, node_id, scene_id, stamina_potion, pending_stamina_potions = \
            get_parameter_for_update_playerstorystate(request)

        user = get_user(phone_id)

        if scene_id:
            user.scene_id = scene_id
            user.save()

        handle_stamina_regeneration(request, type_res)

        user = get_user(phone_id)

        if is_stamina_potion_count_valid(user, stamina_potion):  # validate the user's stamina portion count is not more than the one in DB
            user_ticket_num = user.ticket
            reflect_stamina_potion_count_to_stamina_count(user, stamina_potion, user_ticket_num, request, type_res)
            user.stamina_potion = stamina_potion + pending_stamina_potions
        else:
            error = get_properties(err_type="Error", err_code="ERR0034")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        stamina_max = get_stamina_max(other, context, type_res)

        #  use stamina for story play
        if is_stamina_deduction_needed(scene_id):
            if user.ticket > 0:
                if user.ticket >= int(stamina_max.value):
                    if is_stamina_regeneration_needed(scene_id):
                        user.ticket_last_update = get_now_datetime()
                user.ticket -= 1
            else:
                error = get_properties(err_type="Warning", err_code="WAR0018")
                res_dict = {'status': 'failed', 'function': other, 'Error': error}
                if type_res == 0:
                    return throw_error(template="home.html", obj_dict=res_dict, context=context)
                elif type_res == 1:
                    return throw_error_in_json(res_dict, phone_id)

        try:
            user_character = UserCharacters.objects.get(user_id=user.id, delete_flag=False)
            for key in affinities_dict.keys():
                if key in user_character.affinities:
                    try:  # catch if value is not int
                        affinity_value = int(affinities_dict[key])
                        user_character.affinities[key] = affinity_value
                    except ValueError:
                        continue
                else:
                    user_character.affinities[key] = affinities_dict[key]

            user_character.save()

        except UserCharacters.DoesNotExist:
            error = get_properties(err_type="Error", err_code="ERR0052")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        if node_id:
            user.node_id = node_id

        user.save()

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
            res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

    return get_playerstate(request, type_res)


def refresh_user(phone_id, other, type_res, context):
    try:
        user = get_user(phone_id)
    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
    return user


def is_stamina_deduction_needed(scene_id):
    stamina_flag = False
    if scene_id:
        scene = SceneTable.objects.get(scene_path=scene_id)
        stamina_flag = scene.stamina_deduction_flag

    return stamina_flag


def is_stamina_potion_count_valid(user, stamina_potion):
    if user.stamina_potion < stamina_potion:
        # Stamina potions are only obtained through server purchases -- it should not be possible for us to have a lower value than what the client reports
        return False
    else:
        return True

def requested_stamina_values_are_valid(user, user_stamina, client_stamina_potion):
    '''Determines whether the client's provided values are possible'''
    stamina_max = get_stamina_max_routine()

    if user.stamina_potion < client_stamina_potion:
        # Stamina potions are only obtained through server purchases -- it should not be possible for us to have a lower value than what the client reports
        raise Exception("invalid stamina potion requested. Requested: %s, Actual: %s" % (client_stamina_potion, user.stamina_potion))
        return False
        
    if client_stamina_potion < 0:
        # Client cannot use stamina potions that they don't have
        raise Exception("invalid number requested: %s" % (client_stamina_potion))
        return False
        
    if user_stamina > stamina_max:
        # Client cannot exceed maximum stamina
        raise Exception("requested more than maximum stamina: %s" % (user_stamina))
        return False

    stamina_exchange_rate = get_item_exchange_rate_routine(const.stamina_ticket).ticket_quantity
    total_stamina = user.ticket
        
    # Make sure the total stamina count includes the stamina gained from stamina potions
    used_stamina_potion_count = user.stamina_potion - client_stamina_potion
    stamina_from_potions = used_stamina_potion_count * stamina_exchange_rate
    total_stamina += stamina_from_potions

    result = total_stamina >= user_stamina
    if not result:
        raise Exception("requested too much stamina. Total stamina vs requested stamina: %s, %s" % (total_stamina, user_stamina))

    return total_stamina >= user_stamina

def reflect_stamina_potion_count_to_stamina_count(user, client_stamina_potion, user_stamina, request, type_res):
    other = 'reflect_stamina_potion_count_to_stamina_count'
    used_stamina_potion_count = user.stamina_potion - client_stamina_potion
    context = RequestContext(request, {request: request, 'user': request.user})

    stamina_exchange_rate = get_item_exchange_rate(const.stamina_ticket, other, context, type_res)

    stamina_max = get_stamina_max(other, context, type_res)

    if user.stamina_potion > 0 and used_stamina_potion_count > 0:
        if (used_stamina_potion_count < stamina_exchange_rate.ticket_price) or \
                (used_stamina_potion_count % stamina_exchange_rate.ticket_price != 0): # if the stamina potion used is less than the price, or not multiples of the price shows error
            error = get_properties(err_type='Warning', err_code='WAR0014')
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, user.phone_id)

        if user_stamina < int(stamina_max.value):
            # add stamina
            stamina_count = used_stamina_potion_count / stamina_exchange_rate.ticket_price
            total_stamina_count = stamina_count * stamina_exchange_rate.ticket_quantity

            if total_stamina_count < int(stamina_max.value):
                user.ticket += total_stamina_count
                if user.ticket > int(stamina_max.value):
                    user.ticket = int(stamina_max.value)
            else:
                user.ticket = int(stamina_max.value)
        else:
            # user's stamina limited to max
            user.ticket = int(stamina_max.value)

    user.save()

    return user


def howtos_entry(request):
    other = 'howtos_progress'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'howtos_progress', 'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def howtos_progress(request, type_res):
    from witches.mail import send_first_mail, give_user_howtos_mail_attachment, has_howtos_mail_sent_already

    other = 'howtos_progress'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    context = RequestContext(request, {request: request, 'user': request.user})

    try:
        phone_id = request.POST['phone_id']
        howtos_progress = request.POST['howtos_progress']

    except Exception as e:
        phone_id = const.system_phone_id
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    try:
        user = WUsers.objects.get(phone_id=phone_id, delete_flag=False)
        user.howtos_scene_id = howtos_progress
        if const.howtos_mail_scene in howtos_progress:
            if not has_howtos_mail_sent_already(user):
                send_first_mail(user, context, type_res)
                howtos_mail = UserMailBox.objects.get(user_id=user.id)
                give_user_howtos_mail_attachment(user, howtos_mail.id, other, context, type_res)
        user.save()
    except WUsers.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0023")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    return get_playerstate(request, type_res)


def input_name_entry_html(request):
    other = 'input_names'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'input_names', 'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def input_names(request, type_res):
    other = 'input_names'

    type_res = get_type_res(type_res)
    context = RequestContext(request, {request: request, 'user': request.user})
    phone_id = get_phone_id_from_request(request, other, context, type_res)
    try:
        first_name, last_name = get_first_last_name_from_request(request)
        user = get_user(phone_id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    return get_playerstate(request, type_res)


def refill_stamina_html(request):
    other = 'refill_stamina'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def refill_stamina(request, type_res):
    other = 'handle_stamina_refill'
    type_res = get_type_res(type_res)

    context = RequestContext(request, {request: request, 'user': request.user})

    try:
        phone_id = get_phone_id_from_request(request, other, context, type_res)
        user = get_user(phone_id)

        if user.tutorial_flag:
            stamina_max = get_stamina_max(other, context, type_res)
            user.ticket = int(stamina_max.value)
            user.ticket_last_update = get_now_datetime()
            user.save()
        else:
            Error = get_properties(err_type='Error', err_code='ERR0081')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    return get_playerstate(request, type_res)


def update_stamina_html(request):
    other = 'handle_stamina_regeneration'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


def regenerate_stamina(user, time):
    stamina_max = get_stamina_max_routine()

    if user.scene_id:
        regenerates_stamina = is_stamina_regeneration_needed(user.scene_id)
    else:
        regenerates_stamina = True

    if not regenerates_stamina or (user.ticket >= stamina_max):
        return

    refresh_rate_in_min = get_stamina_refresh_rate()
    refresh_rate_in_seconds = refresh_rate_in_min * 60

    stamina_update_count = get_regeneration_count(user.ticket_last_update, time, const.stamina_ticket,
                                                  stamina_max, refresh_rate_in_seconds)

    new_ticket = stamina_update_count + user.ticket
    if new_ticket > stamina_max:
        new_ticket = stamina_max

    user.ticket = new_ticket

    if user.ticket_last_update:
        total_update_seconds = get_total_seconds_for_update(stamina_update_count, refresh_rate_in_seconds)
        total_update_seconds_in_format = datetime.timedelta(seconds=total_update_seconds)
        user.ticket_last_update += total_update_seconds_in_format
    else:
        user.ticket_last_update = time

    
@csrf_exempt
def handle_stamina_regeneration(request, type_res):
    other = 'handle_stamina_regeneration'
    type_res = get_type_res(type_res)

    context = RequestContext(request, {request: request, 'user': request.user})

    phone_id = get_phone_id_from_request(request, other, context, type_res)

    now = get_now_datetime()
    current_time_in_sec = convert_datetime_to_seconds(now)

    try:
        stamina_max = get_stamina_max(other, context, type_res)
        max_stamina = int(stamina_max.value)

        user = get_user(phone_id)

        if user.scene_id:
            regeneration_flag = is_stamina_regeneration_needed(user.scene_id)
        else:
            regeneration_flag = True

        if regeneration_flag:

            if user.ticket >= max_stamina:
                user.ticket_last_update = now
                return get_playerstate(request, type_res)

            else:
                refresh_rate_in_min = get_stamina_refresh_rate_from_db(other, context, type_res)
                refresh_rate_in_seconds = int(refresh_rate_in_min.value) * 60

                # ticket_last_update could be empty string here, in that cast, max value returned
                stamina_update_count = get_regeneration_count(user.ticket_last_update, now, const.stamina_ticket,
                                                              max_stamina, refresh_rate_in_seconds)

                new_ticket = stamina_update_count + user.ticket

                if new_ticket > max_stamina:
                    new_ticket = max_stamina

                user.ticket = new_ticket

                total_update_seconds = get_total_seconds_for_update(stamina_update_count, refresh_rate_in_seconds)
                total_update_seconds_in_format = datetime.timedelta(seconds=total_update_seconds)

                if user.ticket_last_update:
                    user.ticket_last_update += total_update_seconds_in_format
                else:
                    user.ticket_last_update = now

                user.save()

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    request.POST = request.POST.copy()
    request.POST['current_time'] = current_time_in_sec

    return get_playerstate(request, type_res)


def is_stamina_regeneration_needed(user_scene_id):
    scene = SceneTable.objects.filter(scene_path=user_scene_id)
    regeneration_flag = True

    if len(scene) == 1:
        regeneration_flag = scene[0].regeneration_flag
    elif len(scene) > 1:
        logger.debug('there is more than 1 scene with the user scene name[' + user_scene_id + '] in scene table')
        regeneration_flag = scene[0].regeneration_flag
    else:
        logger.debug('there is no scene with the user scene name[' + user_scene_id + '] in scene table')

    return regeneration_flag

def update_outfit_html(request):
    other = 'update_outfit',
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def update_outfit(request, type_res):
    other = 'update_outfit'

    try:
        type_res = get_type_res(type_res)
        context = RequestContext(request, {request: request, 'user': request.user})
        phone_id = get_phone_id_from_request(request, other, context, type_res)
        user = get_user(phone_id)
        
        new_outfit_raw = request.POST['new_outfit']
        new_outfit = json.loads(new_outfit_raw)
        
        update_outfit_internal(new_outfit, user)
        user.save()

        return get_playerstate(request, type_res)
    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, phone_id)

# Note: Default items are not explicitly wearable -- there is a risk that these items are sent by the user
# it would be a hack, because the client shouldn't send this information, however
# Note: think about a better name than internal -- if we maintain a split between the request entry point and the actual implementation
def update_outfit_internal(new_outfit, user):
    ownedClothingRecords = UserAvatarItemsInCloset.objects.filter(user_id=user.id, delete_flag=False)
    ownedClothing = [ x.id for x in ownedClothingRecords ]

    requestedClothingRecords = AvatarItems.objects.filter(layer_name__in=new_outfit, delete_flag=False)
    requestedClothing = [ x.id for x in requestedClothingRecords ]

    for newClothingItem in ownedClothing:
        if not newClothingItem in ownedClothing:
            raise "User {0} attempted to wear item {1} without ownership" % (user.id, newClothingItem)

    # if the user has proper ownership of all items, then update the outfit
    user.current_outfit = requestedClothing

def get_regeneration_count(last_update, current_time, ticket_type, max_value, refresh_rate_in_seconds):
    if not last_update:
        return max_value

    naive_time = current_time.replace(tzinfo=None)
    time_diff_in_seconds = get_time_diff_in_seconds(last_update, naive_time)

    if ticket_type == const.stamina_ticket:
        if time_diff_in_seconds <= 0 or time_diff_in_seconds < refresh_rate_in_seconds:
            return 0

    update_count = int(time_diff_in_seconds / refresh_rate_in_seconds)
    return update_count


def sync_resources_html(request):
    other = 'sync_resources'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0, 'item_form': 'sync_resources'})
    return render_to_response('home.html', context_instance=context)


def sync_resources_routine(user, stamina, stamina_potions, pending_stamina_potions, time):
    max_stamina = get_stamina_max_routine()

    if stamina > user.ticket:
        error = sync_resource_error_message('sync_resources_routine', 'stamina', stamina, user.ticket)
        log_out_of_sync_error(error, user.phone_id)
        if stamina > max_stamina:
            error = sync_resource_error_message_max('sync_resources_routine', 'stamina', stamina, max_stamina)
            log_out_of_sync_error(error, user.phone_id)
            stamina = max_stamina

    user.ticket = stamina
    user.stamina_potion = stamina_potions + pending_stamina_potions
    regenerate_stamina(user, time)
    
    user.save()


@csrf_exempt
def sync_resources(request, type_res):
    other = 'sync_resources'

    type_res = int(type_res) if type_res else 0

    context = RequestContext(request, {request: request, 'user': request.user})

    time = get_now_datetime()

    try:
        phone_id, stamina, focus, stamina_potions, pending_stamina_potions = \
            get_parameter_for_sync_resources(request, other, type_res, context)
        stamina = int(stamina)
        stamina_potions = stamina_potions
        pending_stamina_potions = pending_stamina_potions

        user = get_user(phone_id)
        if not user:
            return handle_missing_user(context, type_res, phone_id, other)

        sync_resources_routine(user, stamina, stamina_potions, pending_stamina_potions, time)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    current_time_in_sec = convert_datetime_to_seconds(time)
    
    # would prefer to get rid of this approach in the future. the current time is modified so that get_playerstate
    # can calculate the next update times appropriately. Ideally this calculation should be done in a separate function
    request.POST = request.POST.copy()
    request.POST['current_time'] = current_time_in_sec

    return get_playerstate(request, type_res)
        

def handle_missing_user(context, type_res, phone_id, source):
    error = get_properties(err_type="Error", err_code="ERR0023")
    res_dict = {'status': 'failed', 'function': source, 'Error': error}
    if type_res == 0:
        return throw_error(template="home.html", obj_dict=res_dict, context=context)
    else:
        return throw_error_in_json(res_dict, phone_id)



def verify_count(user, stamina):
    if user.ticket < int(stamina):
        logger.debug(get_properties(err_type="Error", err_code="ERR0072"))
        verified_stamina = user.ticket
    else:
        verified_stamina = int(stamina)
    
    return verified_stamina


def revert_stamina(user, user_ticket_num):
    user.ticket = user_ticket_num
    user.save()


def get_seconds(time):
    return ((((time.days * 24) * 60) * 60)*60) + time.seconds



