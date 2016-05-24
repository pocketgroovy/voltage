from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from pymongo.errors import ConnectionFailure
from witches import const
from witches.master import get_login_bonus_interval_in_sec
from witches.models import WUsers, UserLoginHistory, UserCharacters, UserCompletedScenes, UserAvatarItemsInCloset, UserBooks, UserCompleteRecipes, \
    LogInBonusesMaster, Potions, Ingredients, UserItemInventory
from witches.user import get_playerstate, get_restore_response
from witches.utils.custom_exceptions import NoValueFoundError
from witches.utils.user_util import get_user, get_user_playerjson_collection, get_playerjson_from_request, \
    get_user_client_update_json_collection
from witches.utils.util import get_properties, throw_error, throw_error_in_json, get_now_datetime, \
    get_time_diff_in_seconds

from witches.user_functions import create_user_routine, is_new_style_user_id

from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger(__name__)

import json


def login_html(request):
    other = 'login'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'login',
                                       'item_form': 'login', 'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


# Commented out while we need to support restoring users, after DB loss
# @never_cache
# def login(request, type_res=0):
#     other = 'login'

#     if type_res:
#         type_res = int(type_res)
#     else:
#         type_res = 0
#     try:
#         context = RequestContext(request, {request: request, 'user': request.user})
        
#         phone_id = request.GET.get('phone_id')
#         device = request.GET.get('device')
#         update_login_date(phone_id, other, type_res, context)
#         add_user_device(phone_id, device, other, type_res, context)
#         add_user_login_history(phone_id, device)

#     except ConnectionFailure as e:
#         res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
#         return throw_error_in_json(res_dict, 'maintenance')

#     request.POST = request.GET.copy()

#     return get_playerstate(request, type_res)

### This allows user creation when there are unknown user ids. Should be reverted to the old login method when we no longer wish to support this
@never_cache
@csrf_exempt
def login_user(request, type_res=0):
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0
    context = RequestContext(request, {request: request, 'user': request.user})

    phone_id = request.POST.get('phone_id')
    device = request.POST.get('device')
    now = get_now_datetime()

    # 'has_bonus' is a string, so default value is None
    login_bonus_flag = request.POST.get('has_bonus')

    # None state is for old users. Boolean for new users (version 2.1.2), could possibly test request for 'has_bonus'
    # future versions only require a bool (but the client is sending us a string)
    if login_bonus_flag == 'False':     # old users won't have this flag = no action will be taken and no bonus item list will be added to their WUser table
        try:
            handle_login_bonus(phone_id, now, request, type_res)
        except Exception as e:
            res_dict = {'status': 'failed', 'function': 'login_user', 'Error': str(e)}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            else:
                return throw_error_in_json(res_dict, phone_id)
    return handle_user_login(phone_id, device, request, type_res)


def handle_login_bonus(phone_id, current_datetime, request, type_res):
    user = get_user(phone_id)

    if has_time_elapsed_for_next_bonus(user.phone_id, user.last_login_bonus_date, current_datetime):
        bonus_indices_list = get_bonus_index_list(user.next_login_bonus_index)

        update_bonus_items(user, bonus_indices_list)
        update_next_login_bonus_index_and_date(user, current_datetime, bonus_indices_list[2])
        give_user_bonus_item(user)      # new item is saved to the inventory table here
    else:
        request.POST = request.POST.copy()
        request.POST['bonus_ineligible'] = True

    user.save()
    return get_playerstate(request, type_res)


# list of four indices: past, current, next, future
def get_bonus_index_list(user_index):

    master_size = len(LogInBonusesMaster.objects.filter(delete_flag=False))
    if master_size > 0:
        previous_index = get_index(user_index - 1, master_size)
        current_index = get_index(user_index, master_size)
        next_index = get_index(user_index + 1, master_size)
        future_index = get_index(user_index + 2, master_size)
    else:
        error = get_properties(err_type="Error", err_code="ERR0092")
        raise NoValueFoundError(error)

    return [previous_index, current_index, next_index, future_index]


def get_index(given_index, master_table_size):
    return given_index % master_table_size


def has_time_elapsed_for_next_bonus(phone_id, last_login_bonus_date, current_date):
    interval_in_sec = get_login_bonus_interval_in_sec(phone_id)

    if last_login_bonus_date:
        elapsed_time_in_sec = get_time_diff_in_seconds(last_login_bonus_date, current_date)

        return interval_in_sec <= elapsed_time_in_sec

    else:
        # first time login bonus
        return True


# shift and add new bonus item
# [past, current, next, future]
def update_bonus_items(user, new_bonus_index_list):
    if user.login_bonus_items:
        bonus_items_list = user.login_bonus_items
        new_future_bonus_item = get_new_future_bonus_item(new_bonus_index_list[3])  # new item is the last index in list
        user.login_bonus_items = [bonus_items_list[1], bonus_items_list[2], bonus_items_list[3], new_future_bonus_item]
    else:
        user.login_bonus_items = create_login_bonus_list(new_bonus_index_list)


def get_new_future_bonus_item(item_index):
    new_future_item = LogInBonusesMaster.objects.get(bonus_index=item_index)
    new_item = {'id': new_future_item.bonus_id, 'qty': new_future_item.quantity}

    return new_item


def create_login_bonus_list(new_bonus_index_list):
    item_list = []
    for index in new_bonus_index_list:  # LogInBonusesMaster.objects.filter(bonus_index__in=new_bonus_index_list) returns wrong order
        item = LogInBonusesMaster.objects.get(bonus_index=index)
        bonus_item = {'id': item.bonus_id, 'qty': item.quantity}
        item_list.append(bonus_item)
    return item_list


def update_next_login_bonus_index_and_date(user, current_datetime, new_bonus_index):
    user.last_login_bonus_date = current_datetime
    user.next_login_bonus_index = new_bonus_index


def give_user_bonus_item(user):
    current_item = user.login_bonus_items[const.current_index]
    if current_item['id'] == 'stamina_potion':
        user.stamina_potion += current_item['qty']
    elif current_item['id'] == 'coin':
        user.free_currency += current_item['qty']
    elif current_item['id'] == 'starstone':
        user.premium_currency += current_item['qty']
    else:
        handle_inventory_items(user)


# replace with inventory util function shared between: login bonus, shop, email, etc.
def handle_inventory_items(user):
    id = user.login_bonus_items[const.current_index]['id']
    quantity = user.login_bonus_items[const.current_index]['qty']
    potion_item = Potions.objects.filter(id=id)

    if len(potion_item) == 1:
        give_to_user_inventory(user, potion_item[0], quantity, const.type_potion)
    else:
        ingredient_item = Ingredients.objects.filter(id=id)
        if len(ingredient_item) == 1:
            give_to_user_inventory(user, ingredient_item[0], quantity, const.type_ingredient)
        else:
            error = get_properties(err_type="Error", err_code="ERR0093")
            raise NoValueFoundError(error)


def give_to_user_inventory(user, item, quantity, item_type):
    new_item = None

    if item_type == const.type_ingredient:
        item_set = UserItemInventory.objects.filter(user_id=user.id, ingredient_id=item.id, delete_flag=False)
        if len(item_set) == 0:
            new_item = UserItemInventory.objects.create(user_id=user.id, ingredient_id=item.id, quantity=0)
        else:
            new_item = item_set[0]

    elif item_type == const.type_potion:
        item_set = UserItemInventory.objects.filter(user_id=user.id, potion_id=item.id, delete_flag=False)
        if len(item_set) == 0:
            new_item = UserItemInventory.objects.create(user_id=user.id, potion_id=item.id, quantity=0)
        else:
            new_item = item_set[0]

    new_quantity = int(new_item.quantity) + quantity
    new_item.quantity = new_quantity
    new_item.save()


def handle_user_login(phone_id, device, request, type_res):
    other = 'login'
    
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        context = RequestContext(request, {request: request, 'user': request.user})

        # Determine if we already have this user, or if we will need to restore an account for them due to data loss
        matched_users = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)

        if len(matched_users) == 0:
            if is_new_style_user_id(phone_id):
                return handle_missing_user(context, type_res, phone_id, other)
            else:
                user = create_user_routine(phone_id)
        else:
            # Ignoring the case where there are multiple users
            user = matched_users[0]

        save_playerjson(user, request)

        # Reconcile player data
        client_json = get_player_json(request)

        if bool(user.affinity_update):
            add_update_affinities(client_json, user.affinity_update, user.phone_id)  # temporary function for removing minigame mail

        if client_json:
            if user.unrecovered:
                handle_recover_player(user, client_json)
            else:
                # Just update the affinity and currencies, which could have changed since last login
                save_affinities(user.id, client_json["affinities"])
                user.free_currency = client_json["currencyGame"]
                user.premium_currency = client_json["currencyPremium"]

        update_login_date(user)
        add_user_device(user, device)
        user.save()
        add_user_login_history(phone_id, device)

        # restoring player...
        # do we need to perform any of the operations above? behaviour of 'get_restore_response' is to continue normal flow on error so maybe yes.
        if user.update_client:
            response = get_restore_response(request)
            user.affinity_update = {}
            user.update_client = False
            user.save()
            return response

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')
    except Exception as e:
        logger.error(str(e))

    return get_playerstate(request, type_res) #, extra_parms=extra_parms)


def get_client_update_json():

    return {}


def add_update_affinities(client_json, affinity_update, phone_id):
    merge_affinities(affinity_update, client_json["affinities"])
    raw_json = json.dumps(client_json)  # convert to string to store

    update_json_doc = get_user_client_update_json_collection(phone_id)
    update_json_doc.playerjson = raw_json
    update_json_doc.save()


def merge_affinities(update, current):
    for key in update.keys():
            if key in current:
                affinity_value = int(update[key])
                current[key] += affinity_value
            else:
                logger.debug('Missing affinity key: {key} in client json: '.format(key=key))

    return current


def save_playerjson(user, request):
    player_json = get_playerjson_from_request(request, user.phone_id)
    user_player_json = get_user_playerjson_collection(user)
    user_player_json.playerjson = player_json
    user_player_json.phone_id = user.phone_id
    user_player_json.save()


def update_login_date(user):
    user.login_date = get_now_datetime()


def add_user_device(user, device):
    user.device = device


def handle_missing_user(context, type_res, phone_id, other):
    error = get_properties(err_type="Error", err_code="ERR0023")
    res_dict = {'status': 'failed', 'function': other, 'Error': error}
    if type_res == 0:
        return throw_error(template="home.html", obj_dict=res_dict, context=context)
    else:
        return throw_error_in_json(res_dict, phone_id)


def add_user_login_history(phone_id, device):
    UserLoginHistory.objects.create(phone_id=phone_id, device=device)


def get_player_json(request):
    if 'player_json' in request.POST:
        return json.loads(request.POST['player_json'])
    else: 
        return None


def handle_recover_player(user, json):
    if not json:
        return

    try:
        user.first_name = json["firstName"]
        user.last_name = json["lastName"]

        user.ticket = json["stamina"]
        user.stamina_potion  = json["staminaPotions"]
        user.free_currency = json["currencyGame"]
        user.premium_currency = json["currencyPremium"]
        user.tutorial_flag = json["tutorialFlag"]
        user.tutorial_progress = json["tutorialProgress"]

        user.closet = json["closetSpace"]

        user.scene_id = json["currentScene"]
        user.node_id =  json["currentNodeID"]

        user.total_affinity = json["totalAffinity"]

        save_affinities(user.id, json["affinities"])
        save_completed_scenes(user.id, json["completedScenes"])
        save_inventory(user.id, json["inventory"])
        save_books(user.id, json["books"])
        save_recipe(user.id, json["books"])

        user.unrecovered = False
    
    except KeyError as e:
        logger.error("login::handle_recover_player has KeyError: " + str(e))
    

def save_affinities(user_id, affinities_dict):
    # user_functions::create_user_routine already created entry
    user_character = UserCharacters.objects.get(user_id=user_id, delete_flag=False) # DoesNotExist

    user_character.affinities = affinities_dict;
    user_character.save()


def save_completed_scenes(user_id, completed_scenes):
    matched_scenes = UserCompletedScenes.objects.filter(user_id=user_id, delete_flag=False)
    existing_scenes = [scene.scene_id for scene in matched_scenes]

    for scene in completed_scenes:
        if scene not in existing_scenes:
            UserCompletedScenes.objects.create(user_id=user_id, scene_id=scene)


def save_inventory(user_id, inventory):
    matched_items = UserAvatarItemsInCloset.objects.filter(user_id=user_id, delete_flag=False)
    items_owned = [item.avatar_item_id for item in matched_items]

    for item_id, qty in inventory.iteritems():
        if item_id not in items_owned:
            UserAvatarItemsInCloset.objects.create(user_id=user_id, avatar_item_id=item_id, quantity=qty)


def save_books(user_id, books):
    # user_functions::create_user_routine already created entry
    user_books = UserBooks.objects.get(user_id=user_id, delete_flag=False)    # DoesNotExist

    for book in books:
        if book["Id"] not in user_books.book_list:
            user_books.book_list.append(book["Id"])

    user_books.save()
    

def save_recipe(user_id, books):
    matched_recipes = UserCompleteRecipes.objects.filter(user_id=user_id, delete_flag=False)

    for book in books:
        for recipe in book["Recipes"]:
            existing_recipe = matched_recipes.filter(recipe_id=recipe["recipe_id"])

            if len(existing_recipe) > 0:
                existing_recipe[0].level = recipe["stars"]
            else:
                UserCompleteRecipes.objects.create(user_id=user_id, recipe_id=recipe["recipe_id"], level=recipe["stars"])





### Also commented out as part of the DB recovery process. The above version is a better way of handling it, but these can be restored when we go back
# def update_login_date(phone_id, other, type_res, context):
#     try:
#         user = WUsers.objects.get(phone_id=phone_id, delete_flag=False)
#         user.login_date = get_now_datetime()
#         user.save()
#     except WUsers.DoesNotExist:
#         error = get_properties(err_type="Error", err_code="ERR0023")
#         res_dict = {'status': 'failed', 'function': other, 'Error': error}
#         if type_res == 0:
#             return throw_error(template="home.html", obj_dict=res_dict, context=context)
#         elif type_res == 1:
#             return throw_error_in_json(res_dict, phone_id)

# def add_user_device(phone_id, device, other, type_res, context):
#     try:
#         user = WUsers.objects.get(phone_id=phone_id, delete_flag=False)
#         user.device = device
#         user.save()
#     except WUsers.DoesNotExist:
#         error = get_properties(err_type="Error", err_code="ERR0023")
#         res_dict = {'status': 'failed', 'function': other, 'Error': error}
#         if type_res == 0:
#             return throw_error(template="home.html", obj_dict=res_dict, context=context)
#         elif type_res == 1:
#             return throw_error_in_json(res_dict, phone_id)

