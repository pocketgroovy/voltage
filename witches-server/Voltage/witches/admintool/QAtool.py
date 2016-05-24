
__author__ = 'yoshi.miyamoto'

import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from witches.models import WUsers, Ingredients, UserItemInventory, Potions, UserAvatarItemsInCloset, AvatarItems
from witches.utils.util import get_properties, throw_error, throw_error_in_json, date_handler


def add_ingredients_inputs(request, type_res):
    other = 'add_all_ingredients'

    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'QA',
                                       'action': other, 'type_res': 0,  'item_form': 'add_all_ingredients'})
    return render_to_response('home.html', context_instance=context)


def add_all_ingredients(request, type_res):
    other = 'add_all_ingredients'
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    res_dict = {}
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id'})

    phone_id = request.POST['phone_id']
    user = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)[0]

    all_ingredients = Ingredients.objects.all()

    if all_ingredients.count() <= 0:
        Error = get_properties(err_type='Error', err_code='ERR0069')
        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
    else:
        for ingredient in all_ingredients:
            UserItemInventory.objects.create(user_id=user.id, ingredient_id=ingredient.id, quantity=1)

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_dict, 'function': other}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')


def add_potions_inputs(request, type_res):
    other = 'add_all_potions'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'QA',
                                       'action': other, 'type_res': 0,  'item_form': 'add_all_potions'})
    return render_to_response('home.html', context_instance=context)


def add_all_potions(request, type_res):
    other = 'add_all_potions'
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    res_dict = {}
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id'})

    phone_id = request.POST['phone_id']
    user = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)[0]

    all_potions = Potions.objects.all()

    if all_potions.count() <= 0:
        Error = get_properties(err_type='Error', err_code='ERR0070')
        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
    else:
        for potion in all_potions:
            UserItemInventory.objects.create(user_id=user.id, potion_id=potion.id, quantity=1)

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_dict, 'function': other}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')


def add_avatar_inputs(request, type_res):
    other = 'add_all_avatars'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'QA',
                                       'action': other, 'type_res': 0,  'item_form': 'add_all_avatars'})
    return render_to_response('home.html', context_instance=context)


def add_all_avatars(request, type_res):
    other = 'add_all_avatars'
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    res_dict = {}
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id'})

    phone_id = request.POST['phone_id']
    user = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)[0]

    all_avatars = AvatarItems.objects.all()

    if all_avatars.count() <= 0:
        Error = get_properties(err_type='Error', err_code='ERR0071')
        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
    else:
        for avatar in all_avatars:
            UserAvatarItemsInCloset.objects.create(user_id=user.id, avatar_item_id=avatar.id, quantity=1)

    if type_res == 0:
        return render_to_response("home.html", {'res_obj': res_dict, 'function': other}, context_instance=context)
    elif type_res == 1:
        return HttpResponse(json.dumps(res_dict, default=date_handler), content_type='application/json')