from default_items import get_default_affinity, get_default_closet, \
    get_default_free_currency, get_default_premium_currency, get_default_ticket, get_default_user_book, \
    get_default_ingredients, get_default_outfit, get_default_stamina_potions, get_default_closet_pieces

from models import WUsers, UserCharacters, UserBooks, UserAvatarItemsInCloset, UserItemInventory, AvatarItems
import ast
import random
import string

OLD_USER_ID_LENGTH=8
NEW_USER_ID_LENGTH=9

def is_new_style_user_id(player_id):
    return len(player_id) == NEW_USER_ID_LENGTH

def generate_user_id(length):
    key = ''
    for i in range(length):
        key += random.choice(string.digits)
    return key


def generate_unique_user_id():
    player_id = generate_user_id(NEW_USER_ID_LENGTH)

    is_not_unique_id = True

    while is_not_unique_id:
        try:
            WUsers.objects.get(phone_id=player_id, delete_flag=False)  # if the random number was used before. create new one
            player_id = generate_user_id(NEW_USER_ID_LENGTH)
        except WUsers.DoesNotExist:
            is_not_unique_id = False

    return player_id

def item_list_to_store_in_closet(default_outfit_pieces, default_closet_pieces):
    # convert the default outfit items to item ids
    default_clothing_in_closet = default_outfit_pieces + default_closet_pieces
    clothing_db_entries = AvatarItems.objects.filter(layer_name__in=default_clothing_in_closet)
    closet_clothing_ids = [ x.id for x in clothing_db_entries ]
    return closet_clothing_ids

def create_user_routine(existing_id=""):

    unrecovered = False
    if existing_id:
        unrecovered = True

    default_free_currency = get_default_free_currency()
    default_premium_currency = get_default_premium_currency()
    default_ticket = get_default_ticket()
    default_user_book = get_default_user_book()
    default_closet = get_default_closet()
    default_affinity = get_default_affinity()
    default_ingredients = get_default_ingredients()
    default_outfit_pieces = get_default_outfit()
    default_stamina_potions = get_default_stamina_potions()
    default_closet_pieces = get_default_closet_pieces()

    default_clothing_in_closet = item_list_to_store_in_closet(default_outfit_pieces, default_closet_pieces)

    clothing_db_entries = AvatarItems.objects.filter(layer_name__in=default_outfit_pieces)
    clothing_ids = [ x.id for x in clothing_db_entries ]

    player_id = existing_id if existing_id else generate_unique_user_id()

    user = WUsers.objects.create(phone_id=player_id, free_currency=int(default_free_currency.value),
                                     premium_currency=int(default_premium_currency.value),
                                     total_affinity=int(default_affinity.value), current_book_id=default_user_book.value,
                                     ticket=int(default_ticket.value),
                                     facebook_flag=False, delete_flag=False, closet=int(default_closet.value),
                                     current_outfit=clothing_ids, stamina_potion=int(default_stamina_potions.value),
                                     scene_id="", howtos_scene_id="", last_name='', first_name='',
                                     unrecovered=unrecovered)

    affinities_dict = {"A": 0, "M": 0, "N": 0, "R": 0, "T": 0}
    UserCharacters.objects.create(user_id=user.id, affinities=affinities_dict)
    UserBooks.objects.create(user_id=user.id, book_list=[default_user_book.value])

    for clothing_id in default_clothing_in_closet:
        UserAvatarItemsInCloset.objects.create(user_id=user.id, avatar_item_id=clothing_id, quantity=1)
        
    ingredients_dict = ast.literal_eval(default_ingredients.value)
    if ingredients_dict:
        for ingredient_id in ingredients_dict.keys():
            quantity = ingredients_dict[ingredient_id]
            UserItemInventory.objects.create(user_id=user.id, ingredient_id=ingredient_id, quantity=quantity)

    return user
