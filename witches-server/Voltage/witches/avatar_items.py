from pymongo.errors import ConnectionFailure

__author__ = 'yoshi.miyamoto'

from bson import objectid
from django.views.decorators.csrf import csrf_exempt
from witches.user import get_playerstate

from models import *
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from utils.util import throw_error, throw_error_in_json, get_properties
import json
import logging

logger = logging.getLogger(__name__)


def save_coordination_html(request):
    other = 'save_coordination_list'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'item_form': 'save_coordination_list', 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


def save_coordination_list(request):
    other = 'save_coordination'
    item1 = request.POST['item1']
    item2 = request.POST['item2']
    item3 = request.POST['item3']
    item4 = request.POST['item4']
    item5 = request.POST['item5']
    item6 = request.POST['item6']
    avatar_item_list = [item1, item2, item3, item4, item5, item6]

    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'item_form': 'save_coordination', 'action': other, 'type_res': 0,
                                       'json_obj': json.dumps(avatar_item_list)})
    return render_to_response('home.html', context_instance=context)

@csrf_exempt
def save_coordination(request, type_res):
    other = 'save_coordination'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    context = RequestContext(request, {request: request, 'user': request.user})

    try:
        phone_id = request.POST['phone_id']
        coordinate_list_json = request.POST['coordination_list']
        coordinate_list = json.loads(coordinate_list_json)

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    try:
        user = WUsers.objects.get(phone_id=phone_id, delete_flag=False)

    except WUsers.DoesNotExist:
        Error = get_properties(err_type='Error', err_code='ERR0023')
        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    if not objectid.ObjectId.is_valid(user.id):
        Error = get_properties(err_type='Error', err_code='ERR0008')
        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    # check if the user is correct
    if not user:
        error = get_properties(err_type="Error", err_code="ERR0023")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    try:
        coordinate = UserClothingCoordination.objects.create(user_id=user.id, coordinate_list=coordinate_list)
        saveEachAvatarItemInCoordinationToCloset(user, coordinate_list)
        UserAvatarItemsInCloset.objects.create(user_id=user.id, coordinate_item_id=coordinate.id, quantity=1)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    except Exception as e:
        # rollback
        try:
            wuser = WUsers.objects.get(id=user.id, delete_flag=False)
            if wuser:
                if wuser.free_currency != user.free_currency:
                    WUsers.objects.filter(id=user.id, delete_flag=False).update(premium_currency=user.premium_currency)
        except WUsers.DoesNotExist:
            error = get_properties(err_type='Error', err_code='ERR0023')
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        error = "Unexpected Error:", e.message
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    return get_playerstate(request=request, type_res=type_res)

def saveEachAvatarItemInCoordinationToCloset(user, coordinate_list):
    for item in coordinate_list:
        UserAvatarItemsInCloset.objects.create(user_id=user.id, avatar_item_id=item, quantity=1)


def remove_html(request):
    other = 'check_coord_for_removal'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'item_form': 'remove_item', 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def check_coord_for_removal(request, type_res):
    other = 'remove_avatar_item'
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        phone_id = request.POST['phone_id']
        avatar_item_id = request.POST['avatar_item_id']

        context = RequestContext(request, {request: request, 'user': request.user})
    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    try:
        try:
            user = WUsers.objects.get(phone_id=phone_id, delete_flag=False)

        except WUsers.DoesNotExist:
            Error = get_properties(err_type='Error', err_code='ERR0023')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        if not objectid.ObjectId.is_valid(user.id):
            Error = get_properties(err_type='Error', err_code='ERR0008')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        # check if the user ir correct
        if not user:
            error = get_properties(err_type="Error", err_code="ERR0023")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        if avatar_item_id:
            try:
                items_in_closet = UserAvatarItemsInCloset.objects.filter(user_id=user.id, delete_flag=False)
                templist = []
                if items_in_closet:
                    for item in items_in_closet:
                        if item.coordinate_item_id:
                            coordinate_contains_item = UserClothingCoordination.objects.filter(delete_flag=False,
                                                                                               pk=item.coordinate_item_id,
                                                                                               coordinate_list__icontains=avatar_item_id)
                            if coordinate_contains_item:
                                templist.append(coordinate_contains_item[0])

                    if templist:
                        context = RequestContext(request, {request: request, 'user': request.user,
                                                           'option': 'wuser_phone_id', 'action': other,
                                                           'item_form': 'remove_confirm'})
                        return render_to_response('home.html', {'phone_id': phone_id, 'avatar_item_id': avatar_item_id},
                                                  context_instance=context)
                    else:
                        return remove_avatar_item(request, other);

            except Exception as ex:
                logger.error(ex.message)
                res_dict = {'status': 'failed', 'function': other, 'Error': str(ex)}
                if type_res == 0:
                    return throw_error(template="home.html", obj_dict=res_dict, context=context)
                elif type_res == 1:
                    return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    return get_playerstate(request=request, type_res=type_res)


def remove_avatar_item_html(request):
    other = 'remove_avatar_item'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'item_form': 'remove_avatar_item', 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def remove_avatar_item(request, type_res):
    other = 'remove_avatar_item'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        phone_id = request.POST['phone_id']
        avatar_item_id = request.POST['avatar_item_id']

        context = RequestContext(request, {request: request, 'user': request.user})

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    try:
        try:
            user = WUsers.objects.get(phone_id=phone_id, delete_flag=False)

        except WUsers.DoesNotExist:
            Error = get_properties(err_type='Error', err_code='ERR0023')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        if not objectid.ObjectId.is_valid(user.id):
            Error = get_properties(err_type='Error', err_code='ERR0008')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        # check if the user is correct
        if not user:
            error = get_properties(err_type="Error", err_code="ERR0023")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        if avatar_item_id:  # how does it find out if this item is a part of coordination or just individual ??
            if not objectid.ObjectId.is_valid(avatar_item_id):
                Error = get_properties(err_type='Error', err_code='ERR0008')
                res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                if type_res == 0:
                    return throw_error(template="home.html", obj_dict=res_dict, context=context)
                elif type_res == 1:
                    return throw_error_in_json(res_dict, phone_id)

            try:
                coordinates_contains_item = UserClothingCoordination.objects.filter(delete_flag=False,
                    user_id=user.id, coordinate_list__icontains=avatar_item_id)
                if coordinates_contains_item:
                    for coord in coordinates_contains_item:
                        if not objectid.ObjectId.is_valid(coord.id):
                            Error = get_properties(err_type='Error', err_code='ERR0011')
                            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                            if type_res == 0:
                                return throw_error(template="home.html", obj_dict=res_dict, context=context)
                            elif type_res == 1:
                                return throw_error_in_json(res_dict, phone_id)
                        try:
                            UserClothingCoordination.objects.get(user_id=user.id, pk=coord.id, delete_flag=False).delete()  # 0:coordination removed 1:only items removed
                            coord_in_closet = UserAvatarItemsInCloset.objects.filter(user_id=user.id, delete_flag=False,
                                                                                     coordinate_item_id=coord.id)
                            if coord_in_closet:
                                coord_in_closet[0].delete()
                            UserAvatarItemsInCloset.objects.get(user_id=user.id, avatar_item_id=avatar_item_id, delete_flag=False).delete()
                            UserItemRemovalHistory.objects.create(user_id=user.id, coordinate_item_id=coord.id,
                                                                  avatar_item_id=avatar_item_id, removal_status=0)
                        except UserClothingCoordination.DoesNotExist:
                            Error = get_properties(err_type='Error', err_code='ERR0015')
                            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                            if type_res == 0:
                                return throw_error(template="home.html", obj_dict=res_dict, context=context)
                            elif type_res == 1:
                                return throw_error_in_json(res_dict, phone_id)

                else:
                    try:
                        UserAvatarItemsInCloset.objects.get(user_id=user.id, avatar_item_id=avatar_item_id, delete_flag=False).delete()
                        UserItemRemovalHistory.objects.create(user_id=user.id, avatar_item_id=avatar_item_id,
                                                             removal_status=1)
                    except UserAvatarItemsInCloset.DoesNotExist:
                        Error = get_properties(err_type='Error', err_code='ERR0016')
                        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                        if type_res == 0:
                            return throw_error(template="home.html", obj_dict=res_dict, context=context)
                        elif type_res == 1:
                            return throw_error_in_json(res_dict, phone_id)

            except Exception as ex:
                logger.error(ex.message)
                res_dict = {'status': 'failed', 'function': other, 'Error': str(ex)}
                if type_res == 0:
                    return throw_error(template="home.html", obj_dict=res_dict, context=context)
                elif type_res == 1:
                    return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    return get_playerstate(request=request, type_res=type_res)


def remove_coordination_html(request):
    other = 'remove_coordination'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'item_form': 'remove_coordination', 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def remove_coordination(request, type_res):
    other = 'remove_coordination'

    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        phone_id = request.POST['phone_id']
        coordinate_item_id = request.POST['coordinate_item_id']

        context = RequestContext(request, {request: request, 'user': request.user})

    except Exception as e:
        res_dict = {'status': 'failed', 'function': other, 'Error': str(e)}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    if not objectid.ObjectId.is_valid(coordinate_item_id):
        Error = get_properties(err_type='Error', err_code='ERR0008')
        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)

    try:
        user = WUsers.objects.filter(phone_id=phone_id, delete_flag=False)[0]

        if not objectid.ObjectId.is_valid(user.id):
            Error = get_properties(err_type='Error', err_code='ERR0008')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        # check if the user is correct
        if not user:
            error = get_properties(err_type="Error", err_code="ERR0023")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        if coordinate_item_id:
            try:
                coordinate_item = UserAvatarItemsInCloset.objects.get(user_id=user.id, delete_flag=False,
                                                                      coordinate_item_id=coordinate_item_id)
                if coordinate_item:
                    UserAvatarItemsInCloset.objects.get(user_id=user.id, coordinate_item_id=coordinate_item_id, delete_flag=False).delete()
                    try:
                        UserClothingCoordination.objects.get(user_id=user.id, id=coordinate_item_id, delete_flag=False).delete()

                    except UserClothingCoordination.DoesNotExist:
                        logger.debug("the coordination could not be found in user's coordination table")

                    UserItemRemovalHistory.objects.create(user_id=user.id, coordinate_item_id=coordinate_item_id,
                                                          removal_status=0)

            except UserAvatarItemsInCloset.DoesNotExist:
                error = get_properties(err_type="Error", err_code="ERR0032")
                res_dict = {'status': 'failed', 'function': other, 'Error': error}
                if type_res == 0:
                    return throw_error(template="home.html", obj_dict=res_dict, context=context)
                elif type_res == 1:
                    return throw_error_in_json(res_dict, phone_id)

    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    return get_playerstate(request=request, type_res=type_res)
