import json
from witches import const
from witches.models import *
from witches.utils.custom_exceptions import TooManyValueFoundError, NoValueFoundError
from witches.utils.util import throw_error, throw_error_in_json, get_properties, log_error_without_response, error_log

__author__ = 'yoshi.miyamoto'

def get_howtos_progress(request, other, type_res, context):
    try:
        howtos_progess = request.POST['howtos_progress']

    except Exception as e:
        phone_id = const.system_phone_id
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            throw_error_in_json(res_dict, phone_id)

    return howtos_progess


def get_parameter_for_sync_resources(request, other, type_res, context):
    try:
        phone_id = request.POST['phone_id']
        stamina = request.POST['stamina']
        stamina_potions = int(request.POST['stamina_potions'])
        pending_sp = request.POST.get('pendingStaminaPotions')
        if not pending_sp:
            pending_stamina_potions = 0
        else:
            pending_stamina_potions = int(pending_sp)

    except Exception as e:
        phone_id = const.system_phone_id
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            throw_error_in_json(res_dict, phone_id)

    return phone_id, stamina, stamina_potions, pending_stamina_potions


def get_parameter_for_update_playerstorystate(request):
    phone_id = request.POST['phone_id']
    node_id = request.POST['node_id']
    scene_id = request.POST['scene_id']
    stamina_potions = int(request.POST['stamina_potions'])
    pending_sp = request.POST.get('pendingStaminaPotions')
    if not pending_sp:
        pending_stamina_potions = 0
    else:
        pending_stamina_potions = int(pending_sp)

    return phone_id, node_id, scene_id, stamina_potions, pending_stamina_potions,


def get_parameter_for_complete_scene(request):
    affinities_json = request.POST["affinities"]
    affinities_dict = json.loads(affinities_json)
    phone_id = request.POST['phone_id']
    stamina_potion = int(request.POST["stamina_potions"])
    pending_sp = request.POST.get('pendingStaminaPotions')
    if not pending_sp:
        pending_stamina_potions = 0
    else:
        pending_stamina_potions = int(pending_sp)

    scene_id = request.POST.get("scene_path")

    return phone_id, affinities_dict, stamina_potion, pending_stamina_potions, scene_id



def get_user(phone_id, db='default'):

    try:
        user = WUsers.objects.using(db).get(phone_id=phone_id, delete_flag=False)
        return user

    except WUsers.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0023")
        raise Exception(error)


def get_id_from_phone_id(user_id):
    return WUsers.objects.get(phone_id=user_id, delete_flag=False).id


def get_phone_id_from_request(request, other, context, type_res):
    try:
        phone_id = request.POST['phone_id']

    except Exception as e:
        phone_id = const.system_phone_id
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            throw_error_in_json(res_dict, phone_id)

    return phone_id


def get_first_last_name_from_request(request):
    if 'first_name' not in request.POST:
        error = get_properties(err_type="Error", err_code="ERR0076")
        raise Exception(error)
    if 'last_name' not in request.POST:
        error = get_properties(err_type="Error", err_code="ERR0077")
        raise Exception(error)

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    return first_name, last_name


def get_current_tutorial_progress_from_request(request, other, context, type_res):
    tutorial_name = request.POST.get('tutorial_name')
    tutorial_progress = request.POST.get('tutorial_progress')
    if not tutorial_name:
        phone_id = get_phone_id_from_request(request, other, context, type_res)
        error = get_properties(err_type="Error", err_code="ERR0078")
        res_dict = {'status': 'missing', 'function': other, 'Error': error}
        log_error_without_response(res_dict, phone_id)

    if not tutorial_progress:
        phone_id = get_phone_id_from_request(request, other, context, type_res)
        error = get_properties(err_type="Error", err_code="ERR0079")
        res_dict = {'status': 'missing', 'function': other, 'Error': error}
        log_error_without_response(res_dict, phone_id)

    return tutorial_name, tutorial_progress


def get_scene_path_from_request(request, other, context, type_res):
    try:
        scene_path = request.POST['scene_path']

    except Exception as e:
        phone_id = get_phone_id_from_request(request, other, context, type_res)
        if not phone_id:
            phone_id = const.system_phone_id
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            throw_error_in_json(res_dict, phone_id)

    return scene_path


def get_user_playerjson_collection(user):
    player_json = UserPlayerJson.objects.filter(phone_id=user.phone_id)
    player_json_count = len(player_json)
    if player_json_count == 1:
        user_player_json = player_json[0]
    elif player_json_count == 0:
        user_player_json = UserPlayerJson.objects.create(phone_id=user.phone_id)
    else:
        error_log('Multiple Player Json Found', user.phone_id, 'get_user_playerjson_collection')
        user_player_json = player_json[0]
    return user_player_json


def get_user_client_update_json_collection(phone_id):
    update_json_doc = UserClientUpdateJson.objects.filter(phone_id=phone_id)
    update_json_count = len(update_json_doc)
    if update_json_count == 1:
        user_update_json_doc = update_json_doc[0]
    elif update_json_count == 0:
        user_update_json_doc = UserClientUpdateJson.objects.create(phone_id=phone_id)
    else:
        error_log('Multiple Player Json Found', phone_id, 'get_user_client_update_json_collection')
        user_update_json_doc = update_json_count[0]
    return user_update_json_doc


def get_playerjson_from_request(request, phone_id):
    player_json = request.POST.get('player_json')
    if player_json:
        return player_json
    else:
        error_log('No Player Json Found', phone_id, 'get_playerjson_from_request')
