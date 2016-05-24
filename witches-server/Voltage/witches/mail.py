from witches.utils.custom_exceptions import NoValueFoundError

__author__ = 'yoshi.miyamoto'

from pymongo.errors import ConnectionFailure
from witches.mail_gifts import pick_up_items
from witches.master import get_howtos_mail, get_type_res
from witches.utils.user_util import get_id_from_phone_id, get_user, get_phone_id_from_request, \
    get_scene_path_from_request
import json
import logging
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from witches import const
from witches.utils.util import get_properties, throw_error, throw_error_in_json, date_handler
from models import *
from bson import ObjectId, objectid

logger = logging.getLogger(__name__)


def check_if_scene_has_mail(scene_id):
    scene = SceneTable.objects.filter(scene_path=scene_id)
    if len(scene) == 1:
        if scene[0].mail_template_id:
            return True
        else:
            return False
    elif len(scene) > 1:
        error = get_properties(err_type="Error", err_code="ERR0082")
    else:
        error = get_properties(err_type="Error", err_code="ERR0039")

    raise NoValueFoundError(error)

@csrf_exempt
def check_scene_mail(request, type_res):
    other = 'check_scene_mail'

    type_res = get_type_res(type_res)

    context = RequestContext(request, {request: request, 'user': request.user})

    phone_id = get_phone_id_from_request(request, other, context, type_res)
    scene_id = get_scene_path_from_request(request, other, context, type_res)

    try:
        get_user(phone_id)

        if scene_id:
            has_scene_mail = check_if_scene_has_mail(scene_id)
            res_dict = {'status': 'success', 'scene_mail': has_scene_mail}

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


def get_all_mails_html(request):
    other = 'get_all_mails'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def get_all_mails(request, type_res):
    other = 'open_mail'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        context = RequestContext(request, {request: request, 'user': request.user})
        phone_id = request.POST['phone_id']
        wuser = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)[0]
        if objectid.ObjectId.is_valid(wuser.id):
            mail_list = list(UserMailBox.objects.filter(user_id=wuser.id, delete_flag=False).values())
        else:
            Error = get_properties(err_type='Error', err_code='ERR0008')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                           'action': other, 'item_form': 'open_mail', 'phone_id': phone_id,
                                           'all_mail_ids': mail_list, 'type_res': type_res})
    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    res_dict = {'mail_box': mail_list, 'status': 'success'}

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_dict, 'function': 'get_all_mails'}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')

@csrf_exempt
def open_mail(request, type_res):
    other = 'pick_up_gifts'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        context = RequestContext(request, {request: request, 'user': request.user})
        phone_id = request.POST['phone_id']
        mail_id = request.POST['mail_id']

        if not objectid.ObjectId.is_valid(mail_id):
            Error = get_properties(err_type='Error', err_code='ERR0012')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        try:
            received_mail = UserMailBox.objects.get(id=ObjectId(mail_id))
            user = get_user(phone_id)
            if not received_mail.read_flag:
                receive_items(received_mail, user, type_res, other, context)

            context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                               'action': other, 'item_form': 'mail_pickup', 'phone_id': phone_id,
                                               'mail_content': received_mail, 'type_res': type_res})
        except UserMailBox.DoesNotExist:
            Error = get_properties(err_type='Error', err_code='ERR0017')
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

    res_dict = {'mail_box': mail_id, 'status': 'success'}

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_dict, 'function': 'open_mail'}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')


def receive_items(received_mail, user, type_res, other, context):
    if received_mail.premium_currency and not received_mail.premium_received_flag:
        new_currency = int(user.premium_currency) + int(received_mail.premium_currency)
        user.premium_currency = new_currency
        received_mail.premium_received_flag = True
    if received_mail.free_currency and not received_mail.free_currency_received_flag:
        new_currency = int(user.free_currency) + int(received_mail.free_currency)
        user.free_currency = new_currency
        received_mail.free_currency_received_flag = True
    if received_mail.stamina_potion and not received_mail.stamina_potion_received_flag:
        new_currency = int(user.stamina_potion) + int(received_mail.stamina_potion)
        user.stamina_potion = new_currency
        received_mail.stamina_potion_received_flag =True
    if received_mail.gifts:
        for item_id in received_mail.gifts:
            pick_up_items(user, item_id['id'], received_mail, type_res, other, context)

    received_mail.read_flag = True
    received_mail.save()
    user.save()


def send_mail_to_user(temp_mail_id, user_id, context, other, type_res):
    mail = get_mail_template(temp_mail_id, other, context, type_res)
    phone_id = const.system_phone_id
    try:
        character = Characters.objects.get(id=ObjectId(mail.sender_id), delete_flag=False)
    except Characters.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0042")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    sender_flag = is_sender_character(temp_mail_id, context, type_res)
    sender_type_for_metrics = get_sender_info_for_metrics(sender_flag)

    prem_num = convert_str_nullable_int(mail.premium_currency)
    free_num = convert_str_nullable_int(mail.free_currency)
    stamina_num = convert_str_nullable_int(mail.stamina_potion)

    UserMailBox.objects.create(user_id=user_id, gifts=mail.attach_list, title="", sender_flag=sender_flag,
                               message_body=mail.body_text, sender_id=character.id, read_flag=False,
                               premium_currency=prem_num, free_currency=free_num, login_bonus_id='',
                               stamina_potion=stamina_num, stamina_potion_received_flag=False,
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


def send_howtos_mail_to_user(temp_mail_id, user_id, context, other, type_res):
    mail = get_mail_template(temp_mail_id, other, context, type_res)
    phone_id = const.system_phone_id
    try:
        character = Characters.objects.get(id=ObjectId(mail.sender_id), delete_flag=False)
    except Characters.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0042")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    sender_flag = is_sender_character(temp_mail_id, context, type_res)
    sender_type_for_metrics = get_sender_info_for_metrics(sender_flag)

    prem_num = convert_str_nullable_int(mail.premium_currency)
    free_num = convert_str_nullable_int(mail.free_currency)
    stamina_num = convert_str_nullable_int(mail.stamina_potion)

    UserMailBox.objects.create(user_id=user_id, gifts=mail.attach_list, title="", sender_flag=sender_flag,
                               message_body=mail.body_text, sender_id=character.id, stamina_potion=stamina_num,
                               premium_currency=prem_num, free_currency=free_num,
                               stamina_potion_received_flag=False,
                               premium_received_flag=False, free_currency_received_flag=False, read_flag=False,
                               login_bonus_id='', multiply_bonus_flag=False, sender_type_for_metrics=sender_type_for_metrics)

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

def activate_mail_event(mail_template_id, user, context, type_res):
    other = 'activate_mail_event'
    if objectid.ObjectId.is_valid(mail_template_id):
        send_mail_to_user(mail_template_id, user.id, context, other, type_res)
    else:
        Error = get_properties(err_type='Error', err_code='ERR0012')
        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, user.phone_id)

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


def mail_badge_html(request):
    other = 'get_mail_badge'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'type_res': 0})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def get_mail_badge(request, type_res):
    other = 'get_mail_badge'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        phone_id = request.POST['phone_id']

        context = RequestContext(request, {request: request, 'user': request.user})
    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    try:
        try:
            WUsers.objects.get(phone_id=phone_id, delete_flag=False)
            user_id = get_id_from_phone_id(phone_id)

        except WUsers.DoesNotExist:
            error = get_properties(err_type="Error", err_code="ERR0023")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        mails = UserMailBox.objects.filter(user_id=user_id, read_flag=False, delete_flag=False)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    res_dict = {'mail_badge': mails.count(), 'status': 'success'}

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_dict, 'function': other}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')

def send_mini_game_potion(recipe_id, user, level, phone_id, other, context, type_res):
    try:
        system = Characters.objects.get(first_name='K&C', delete_flag=False)  # get system ID as sender
    except Characters.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0058")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
        return throw_error(template="home.html", obj_dict=res_dict, context=context)

    user_receipe = Recipes.objects.filter(pk=recipe_id)
    potion_id = get_potion_id_for_level(user_receipe[0], level)
    if potion_id != '' and potion_id != 0:
        gift_list = [{'id': potion_id, 'received_flag': False}]
        UserMailBox.objects.create(user_id=user.id, gifts=gift_list, title="Minigame Potion", sender_flag=True,
                                   message_body='Minigame Result Potion', sender_id=system.id,
                                   read_flag=False, login_bonus_id='', multiply_bonus_flag=False)
    elif potion_id == 0:
        logger.debug('User Star was 0. This should have been already handled. Concern that this is seen here')
    else:
        error = get_properties(err_type="Error", err_code="ERR0060")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
        return throw_error(template="home.html", obj_dict=res_dict, context=context)


def get_potion_id_for_level(user_receipe, level):
    if user_receipe:
        potion_list = user_receipe.potion_list
        if level == 1:
            potion_id = potion_list['basic']
        elif level == 2:
            potion_id = potion_list['superior']
        elif level == 3:
            potion_id = potion_list['master']
        elif level == 0:
            return 0
        else:
            return ''

        return potion_id


def give_user_howtos_mail_attachment(user, user_mail_id, other, context, type_res):
    user_mail = UserMailBox.objects.get(id=ObjectId(user_mail_id), delete_flag=False)
    user_mail.read_flag = True
    if user_mail.premium_currency:
        user.premium_currency += user_mail.premium_currency
        user_mail.premium_received_flag = True
    if user_mail.free_currency:
        user.free_currency += user_mail.free_currency
        user_mail.free_currency_received_flag = True
    if user_mail.stamina_potion:
        user.stamina_potion += user_mail.stamina_potion
        user_mail.stamina_potion_received_flag = True
    if len(user_mail.gifts) > 0:
        for item_id in user_mail.gifts:
            pick_up_items(user, item_id['id'], user_mail, type_res, other, context)
    user_mail.save()
    user.save()

def send_first_mail(user, context, type_res):
    other = 'send_first_mail'
    howtos_mail = get_howtos_mail(other, context, type_res)
    send_howtos_mail_to_user(howtos_mail.value, user.id, other, context, type_res)

def has_howtos_mail_sent_already(user):
    howtos_mail_sent = False
    user_mails = UserMailBox.objects.filter(user_id=user.id)
    if user_mails.__len__() > 0:
        howtos_mail_sent = True
    return howtos_mail_sent
