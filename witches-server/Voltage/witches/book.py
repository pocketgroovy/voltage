__author__ = 'yoshi.miyamoto'

from bson import objectid, ObjectId
from witches.models import UserBooks, Books, UserCompleteRecipes
from witches.utils.util import get_properties, throw_error, throw_error_in_json
import logging


logger = logging.getLogger(__name__)


def add_new_book(book_id, user):
    other = 'activate_book_event'

    if objectid.ObjectId.is_valid(book_id):
        try:
            user_book = UserBooks.objects.get(user_id=user.id, delete_flag=False)
            user_book.book_list.append(book_id)
            user_book.save()
        except UserBooks.DoesNotExist:
            Error = get_properties(err_type='Error', err_code='ERR0041')
            res_dict = {'status': 'failed', 'function': other, 'Error': Error}
            return throw_error_in_json(res_dict, user.phone_id)
    else:
        Error = get_properties(err_type='Error', err_code='ERR0013')
        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
        return throw_error_in_json(res_dict, user.phone_id)

def update_current_user_book(book_id, user):
    user.current_book_id = book_id
    user.save()

def get_current_user_book(user):
    current_book = Books.objects.get(id=ObjectId(user.current_book_id), delete_flag=False)
    return current_book

def check_user_book_completeness(book, user):
    recipes_list = []
    try:
        recipes = Books.objects.get(id=book).recipes
        for recipe in recipes:
            try:
                user_recipe = UserCompleteRecipes.objects.get(user_id=user.id, recipe_id=recipe, delete_flag=False)
                dict_recipe = {'recipe_id': recipe, 'stars': user_recipe.level}
                recipes_list.append(dict_recipe)
            except UserCompleteRecipes.DoesNotExist:
                dict_recipe = {'recipe_id': recipe, 'stars': 0}
                recipes_list.append(dict_recipe)
                continue
        is_complete = is_book_complete(user_id=user.id, recipes_list=recipes)
        book_dic = {'id': book, 'is_complete': is_complete, 'recipes': recipes_list}
    except:
        raise Books.DoesNotExist

    # return user_book_array
    return book_dic

def is_book_complete(user_id, recipes_list):
    try:
        complete_list = UserCompleteRecipes.objects.filter(user_id=user_id, delete_flag=False).values_list('recipe_id', flat=True)
        for recipe in recipes_list:
            if recipe in complete_list:
                stars = UserCompleteRecipes.objects.get(user_id=user_id, recipe_id=recipe, delete_flag=False).level
                if stars == 3:
                    continue
                else:
                    return False
            else:
                return False
    except Exception as e:
        logger.error(str(e))
        return False
    return True
