__author__ = 'yoshi.miyamoto'

import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from pymongo.errors import ConnectionFailure
from witches import const
from witches.master import get_type_res
from django.views.decorators.csrf import csrf_exempt
from witches.utils.user_util import get_current_tutorial_progress_from_request, get_phone_id_from_request, get_user
from witches.utils.util import throw_error_in_json, date_handler, throw_error


@csrf_exempt
def progress(request, type_res):
    other = 'tutorial progress'
    type_res = get_type_res(type_res)
    context = RequestContext(request, {request: request, 'user': request.user})

    try:
        phone_id = get_phone_id_from_request(request, other, context, type_res)
        tutorial_name, tutorial_progress = get_current_tutorial_progress_from_request(request, other, context, type_res)
        user = get_user(phone_id)
        user.tutorial_progress = tutorial_progress
        user.save()
        res_dict = {'status': 'success', 'function': other}

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

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

@csrf_exempt
def finish(request, type_res):
    other = 'finish tutorial'
    type_res = get_type_res(type_res)
    context = RequestContext(request, {request: request, 'user': request.user})
    try:
        phone_id = get_phone_id_from_request(request, other, context, type_res)
        user = get_user(phone_id)
        user.tutorial_flag = False
        user.save()
        res_dict = {'status': 'success', 'function': other}
    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenence')

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