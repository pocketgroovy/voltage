__author__ = 'yoshi.miyamoto'

from witches.utils.util import get_properties
from witches.models import GameProperties
from witches.utils.custom_exceptions import NoValueFoundError


def get_default_outfit():
    return [
        'basic_jeans_darkblue',
        'basic_canvas_shoes_navy',
        'monochrome_blouse_pink',
        'flannel_plaid_shirt_red'
    ]

def get_default_free_currency():
    try:
        default_free_currency = GameProperties.objects.get(name='default_free_currency', delete_flag=False)
    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0043")
        raise NoValueFoundError(error)

    return default_free_currency

def get_default_premium_currency():
    try:
        default_premium_currency = GameProperties.objects.get(name='default_premium_currency', delete_flag=False)
    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0044")
        raise NoValueFoundError(error)

    return default_premium_currency

def get_default_ticket():
    try:
        default_ticket = GameProperties.objects.get(name='default_ticket', delete_flag=False)
    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0045")
        raise NoValueFoundError(error)

    return default_ticket


def get_default_user_book():
    try:
        default_user_book = GameProperties.objects.get(name='default_user_book', delete_flag=False)
    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0047")
        raise NoValueFoundError(error)

    return default_user_book

def get_default_closet():
    try:
        default_closet = GameProperties.objects.get(name='default_closet', delete_flag=False)
    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0048")
        raise NoValueFoundError(error)

    return default_closet

def get_default_affinity():
    try:
        default_affinity = GameProperties.objects.get(name='default_affinity', delete_flag=False)
    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0049")
        raise NoValueFoundError(error)

    return default_affinity

def get_default_ingredients():
    try:
        default_ingredients = GameProperties.objects.get(name='default_ingredients', delete_flag=False)

    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0051")
        raise NoValueFoundError(error)

    return default_ingredients

def get_default_stamina_potions():
    try:
        default_stamina_potions = GameProperties.objects.get(name='default_stamina_potions', delete_flag=False)
    except GameProperties.DoesNotExist:
        error = get_properties(err_type="Error", err_code="ERR0080")
        raise NoValueFoundError(error)

    return default_stamina_potions

def get_default_closet_pieces():
    return ['starry_night_pjs_darkblue']
