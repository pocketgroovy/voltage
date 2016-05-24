__author__ = 'carlos.matsumoto', 'yoshi.miyamoto'


from pymongo.errors import ConnectionFailure
from witches import const
from witches.book import is_book_complete, get_current_user_book
from witches.mail import send_mail_to_user, get_mail_template, send_mini_game_potion
from witches.utils.user_util import get_user, get_id_from_phone_id
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from models import *
from utils.util import throw_error_in_json
from witches.utils.util import get_properties, throw_error
from django.views.decorators.csrf import csrf_exempt

import logging
from user import get_playerstate

logger = logging.getLogger(__name__)


def save_recipe_result_html(request):
    other = 'save_potion_result'
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'wuser_phone_id',
                                       'action': other, 'item_form': 'save_recipe', 'type_res': 0})
    return render_to_response('home.html', context_instance=context)


@csrf_exempt
def save_recipe_result(request, type_res):
    other = 'save_recipe_result'
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    context = RequestContext(request, {request: request, 'user': request.user})

    try:
        phone_id = request.POST['phone_id']
        recipe_id = request.POST['recipe_id']
        # potion_id = request.POST['potion_id']
        level = int(request.POST['stars'])

        if level > const.complete_level or level < 0:
            error = get_properties(err_type="Error", err_code="ERR0060")
            res_dict = {'status': 'failed', 'function': other, 'Error': error}
            if type_res == 0:
                return throw_error(template="home.html", obj_dict=res_dict, context=context)
            elif type_res == 1:
                return throw_error_in_json(res_dict, phone_id)

        user = get_user(phone_id)
        user_id = get_id_from_phone_id(phone_id)

        recipes = Books.objects.get(id=user.current_book_id, delete_flag=False).recipes

        # check completeness before current level to avoid giving away the complete bonus more than twice
        is_all_receipe_already_done = is_book_complete(user_id, recipes)
        # now set current level to user history
        set_user_complete_receipe_level(user_id, recipe_id, level, phone_id, other, context, type_res)

        if level == const.complete_level and not is_all_receipe_already_done:
            try:
                if is_prize_ready(user):
                    current_book = get_current_user_book(user)
                    temp_mail = get_mail_template(current_book.mail_id, other, context, type_res)
                    send_mail_to_user(temp_mail.id, user_id, context, other, type_res)  # mail attachment is the prize

            except Books.DoesNotExist:
                error = get_properties(err_type="Error", err_code="ERR0041")
                res_dict = {'status': 'failed', 'function': other, 'Error': error}
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


def set_user_complete_receipe_level(user_id, recipe_id, level, phone_id, other, context, type_res):
    user_potions = UserCompleteRecipes.objects.filter(user_id=user_id, recipe_id=recipe_id, delete_flag=False)
    if len(user_potions) == 1:
        if is_level_higher_than_before(user_potions[0], level):
            user_potions[0].level = level
        user_potions[0].save()
    elif len(user_potions) > 1:
        error = get_properties(err_type="Error", err_code="ERR0075")
        res_dict = {'status': 'failed', 'function': other, 'Error': error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, phone_id)
    else:
        UserCompleteRecipes.objects.create(user_id=user_id, recipe_id=recipe_id, level=level)


def is_level_higher_than_before(user_potion, level):
    if user_potion.level < level:
        return True
    else:
        return False

def is_prize_ready(user):
    try:
        recipes = Books.objects.get(id=user.current_book_id, delete_flag=False).recipes
        prize_ready = is_book_complete(user.id, recipes)
    except Books.DoesNotExist:
        raise Books.DoesNotExist

    return prize_ready

