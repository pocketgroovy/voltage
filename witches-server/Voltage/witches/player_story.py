__author__ = 'yoshi.miyamoto'

from witches.master import get_type_res
from pymongo.errors import ConnectionFailure
from witches import const
from witches.utils.user_util import get_id_from_phone_id, get_user, get_phone_id_from_request, \
    get_scene_path_from_request, get_parameter_for_complete_scene
from django.http import HttpResponse
from utils.util import date_handler
from django.views.decorators.csrf import csrf_exempt
from witches.book import add_new_book, update_current_user_book
from witches.mail import activate_mail_event
from witches.user import get_playerstate, is_stamina_potion_count_valid, handle_stamina_regeneration, \
    reflect_stamina_potion_count_to_stamina_count
from django.shortcuts import render_to_response
from django.template import RequestContext
from witches.models import UserCharacters, SceneTable, UserCompletedScenes
from witches.utils.util import get_properties, throw_error, throw_error_in_json

import json

def start_scene_entry(request):
    other = 'start_scene'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'start_scene', 'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def start_scene(request, type_res):
    other = 'start_scene'

    type_res = get_type_res(type_res)

    context = RequestContext(request, {request: request, 'user': request.user})

    phone_id = get_phone_id_from_request(request, other, context, type_res)
    scene_id = get_scene_path_from_request(request, other, context, type_res)

    try:
        handle_stamina_regeneration(request, type_res)
        user = get_user(phone_id)

        if scene_id:
            user.scene_id = scene_id
            user.save()
            res_dict = {'status': 'success', 'function': other}

        else:
            error = get_properties(err_type="Error", err_code="ERR0053")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        if not phone_id:
            phone_id = const.system_phone_id
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_dict, 'function': other}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')


def story_reset_inputs(request):
    other = 'story_reset'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def story_reset(request, type_res):
    other = 'story_reset'
    phone_id = request.POST['phone_id']
    try:
        user_id = get_id_from_phone_id(phone_id)
        UserCompletedScenes.objects.filter(user_id=user_id, delete_flag=False).update(delete_flag=True)
        UserCharacters.objects.filter(user_id=user_id, delete_flag=False).update(delete_flag=True)
        affinities_dict = {"A": 0, "M": 0, "N": 0, "R": 0, "T": 0}
        UserCharacters.objects.create(user_id=user_id, delete_flag=False, affinities=affinities_dict)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    request.POST = request.POST.copy()
    request.POST['story_reset'] = True
    return get_playerstate(request, type_res)


def complete_scene_html(request):
    other = 'complete_scene_affinities'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'complete_scene_affinities', 'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

def complete_scene_affinities(request):
    other = 'complete_scene_choices'
    char1 = request.POST['char_init1']
    char2 = request.POST['char_init2']
    char3 = request.POST['char_init3']
    affinity1 = request.POST['affinity1']
    affinity2 = request.POST['affinity2']
    affinity3 = request.POST['affinity3']
    affinities = {char1: affinity1, char2: affinity2, char3: affinity3}

    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'complete_scene_choices', 'action': other, 'type_res': 0,
                                       'json_obj': json.dumps(affinities)})
    return render_to_response('home.html', context_instance=context)

def complete_scene_choices(request):
    other = 'complete_scene'

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
                                       'item_form': 'complete_scene', 'action': other, 'type_res': 0,
                                       'json_choice': json.dumps(choices), 'json_aff': affinities_json})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def complete_scene(request, type_res):
    other = 'complete_scene'
    context = RequestContext(request, {request: request, 'user': request.user})

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        phone_id, affinities_dict, stamina_potion, pending_stamina_potions, scene_id = \
            get_parameter_for_complete_scene(request)

        user = get_user(phone_id)

        if is_stamina_potion_count_valid(user, stamina_potion):  # validate the user's stamina porion count is not more than the one in DB
            reflect_stamina_potion_count_to_stamina_count(user, stamina_potion, int(user.ticket), request, type_res)
            user.stamina_potion = stamina_potion + pending_stamina_potions

        try:
            user_character = UserCharacters.objects.get(user_id=user.id, delete_flag=False)
            for key in affinities_dict.keys():
                if key in user_character.affinities:
                    try:
                        affinity_value = int(affinities_dict[key])
                        user_character.affinities[key] = affinity_value
                        user_character.save()
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

        if not scene_id:
            scene_id = user.scene_id
            
        if scene_id:
            if not has_scene_completed_already(scene_id, user.id):
                UserCompletedScenes.objects.create(user_id=user.id, scene_id=scene_id, delete_flag=False)

            activate_event(scene_id, context, user, type_res)  # unlocking mail and book if needed

        user.save()

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        if not phone_id:
            phone_id = const.system_phone_id
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    return get_playerstate(request, type_res)


def activate_event(scene_id, context, user, type_res):
    other = 'activate_event'
    try:
        scene_event = SceneTable.objects.get(scene_path=scene_id, delete_flag=False)
        if scene_event.mail_template_id:
            activate_mail_event(scene_event.mail_template_id, user, context, type_res)
        if scene_event.book_id:
            if not has_scene_completed_already(scene_id, user.id):
                add_new_book(scene_event.book_id, user)
                update_current_user_book(scene_event.book_id, user)

    except SceneTable.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0039")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, user.phone_id)

def has_scene_completed_already(scene_id, user_id):
    try:
        UserCompletedScenes.objects.get(user_id=user_id, scene_id=scene_id, delete_flag=False)
        return True
    except UserCompletedScenes.DoesNotExist:
        return False

