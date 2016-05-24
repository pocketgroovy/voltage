__author__ = 'yoshi.miyamoto'

from django.http import HttpResponse
from django.core.cache import cache

from witches.models import *
from witches.utils.util import writeToSheet,get_sanitized_int, get_sanitized_string_int, \
    sanitize_scene_path
from datetime import datetime
import ast
import xlwt
import xlrd
from django.views.decorators.csrf import csrf_exempt

from witches.utils.user_util import get_user
from django.core.exceptions import ObjectDoesNotExist
from witches.utils.util import get_now_datetime

# from django.views.decorators.cache import never_cache
import json

import logging
logger = logging.getLogger(__name__)

import traceback

from collections import OrderedDict


@csrf_exempt
def pull_master_data(fileName):

    book = xlwt.Workbook(encoding='UTF-8', style_compression=2)

    ##### BOOKS #####
    bookSheet = book.add_sheet('Books')
    bookFields = Books._meta.fields
    booksValues = Books.objects.order_by('id').values()
    bookSheet = writeToSheet(bookSheet, bookFields, booksValues)


    ##### BOOKPRIZES #####
    bookprizesSheet = book.add_sheet('BookPrizes')
    bookprizesFields = BookPrizes._meta.fields
    bookprizesValues = BookPrizes.objects.order_by('id').values()
    bookprizesSheet = writeToSheet(bookprizesSheet, bookprizesFields, bookprizesValues)

    ##### RECIPIES #####
    recipesSheet = book.add_sheet('Recipes')
    recpesFields = Recipes._meta.fields
    recipeValues = Recipes.objects.order_by('id').values()
    recipesSheet = writeToSheet(recipesSheet, recpesFields, recipeValues)

    ##### INGREDIENTS #####
    ingredientsSheet = book.add_sheet('Ingredients')
    ingredientsFields = Ingredients._meta.fields
    ingredientsValues = Ingredients.objects.order_by('id').values()
    ingredientsSheet = writeToSheet(ingredientsSheet, ingredientsFields, ingredientsValues)

    ##### POTIONS #####
    potionsSheet = book.add_sheet('Potions')
    potionsFields = Potions._meta.fields
    potionsValues = Potions.objects.order_by('id').values()
    potionsSheet = writeToSheet(potionsSheet, potionsFields, potionsValues)

    ##### CATEGORIES #####
    categoriesSheet = book.add_sheet('Categories')
    categoriesFields = Categories._meta.fields
    categoriesValues = Categories.objects.order_by('id').values()
    categoriesSheet = writeToSheet(categoriesSheet, categoriesFields, categoriesValues)

    ##### AVATARITEMS #####
    avataritemsSheet = book.add_sheet('AvatarItems')
    avataritemsFields = AvatarItems._meta.fields
    avataritemsValues = AvatarItems.objects.order_by('id').values()
    avataritemsSheet = writeToSheet(avataritemsSheet, avataritemsFields, avataritemsValues)

    ##### EMAILTEMPLATES #####
    emailtemplatesSheet = book.add_sheet('EmailTemplates')
    emailtemplatesFields = EmailTemplates._meta.fields
    emailtemplatesValues = EmailTemplates.objects.order_by('id').values()
    emailtemplatesSheet = writeToSheet(emailtemplatesSheet, emailtemplatesFields, emailtemplatesValues)

    ##### CHARACTERS #####
    charactersSheet = book.add_sheet('Characters')
    charactersFields = Characters._meta.fields
    charactersValues = Characters.objects.order_by('id').values()
    charactersSheet = writeToSheet(charactersSheet, charactersFields, charactersValues)

    ##### CLOTHINGCOORDINATES #####
    clothingcoordinateSheet = book.add_sheet('ClothingCoordinates')
    clothingcoordinateFields = ClothingCoordinates._meta.fields
    clothingcoordinateValues = ClothingCoordinates.objects.order_by('id').values()
    clothingcoordinateSheet = writeToSheet(clothingcoordinateSheet, clothingcoordinateFields, clothingcoordinateValues)

    ##### AFFINITIES #####
    affinitySheet = book.add_sheet('Affinities')
    affinityFields = Affinities._meta.fields
    affinityValues = Affinities.objects.order_by('id').values()
    affinitySheet = writeToSheet(affinitySheet, affinityFields, affinityValues)

    ##### EI #####
    eiSheet = book.add_sheet('EI')
    eiFields = EI._meta.fields
    eiValues = EI.objects.filter(delete_flag=False).values()
    chaptertableSheet = writeToSheet(eiSheet, eiFields, eiValues)

    ##### GAMEPROPERTIES #####
    gamepropertiesSheet = book.add_sheet('GameProperties')
    gamepropertiesFields = GameProperties._meta.fields
    gamepropertiesValues = GameProperties.objects.order_by('id').values()
    gamepropertiesSheet = writeToSheet(gamepropertiesSheet, gamepropertiesFields, gamepropertiesValues)

    ##### SHOPITEMS #####
    shopitemsSheet = book.add_sheet('ShopItems')
    shopitemsFields = ShopItems._meta.fields
    shopitemsValues = ShopItems.objects.order_by('item_index').values()
    shopitemsSheet = writeToSheet(shopitemsSheet, shopitemsFields, shopitemsValues)

    ##### GLOSSARY #####
    glossarySheet = book.add_sheet('Glossary')
    glossaryFields = Glossary._meta.fields
    glossaryValues = Glossary.objects.order_by('id').values()
    glossarySheet = writeToSheet(glossarySheet, glossaryFields, glossaryValues)

    ##### SCENES #####
    scenesSheet = book.add_sheet('Scenes')
    scenesFields = SceneTable._meta.fields
    scenesValues = SceneTable.objects.order_by('id').values()
    scenesSheet = writeToSheet(scenesSheet, scenesFields, scenesValues)


    ##### LOGINBONUS #####
    loginBonusSheet = book.add_sheet('LogInBonusesMaster')
    loginBonusFields = LogInBonusesMaster._meta.fields
    loginBonusValues = LogInBonusesMaster.objects.order_by('bonus_index').values()
    writeToSheet(loginBonusSheet, loginBonusFields, loginBonusValues)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + fileName
    book.save(response)

    return response


# def hide_field(fields, hidden_field):
#     for field in fields:
#         if field.name == hidden_field:
#             fields.remove(field)
#
#     return fields


# @never_cache
def fetch_json_response(phone_id, env):
    try:
        db = "admin_{0}".format(env)

        player = UserPlayerJson.objects.using(db).get(phone_id=phone_id) 
        player_json = json.loads(player.playerjson, object_pairs_hook=OrderedDict)

        # append additional information for support
        wuser = get_user(phone_id, db)
        player_json['SUPPORT'] = {}
        player_json['SUPPORT']['MONGO_ID'] = wuser.id
        player_json['SUPPORT']['DEVICE'] = wuser.device

        # convert to standard json
        json_dump = json.dumps(player_json, indent=4, separators=(',', ': '))

        response = HttpResponse(json_dump, content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename="voltage_kisses_and_curses_player.json"'

        return response, None

    except Exception as e:              # can be django.core.exceptions.DoesNotExist or MultipleObjectsReturned or ConnectionFailure: timed out (VPN)
        trace = traceback.format_exc()
        logger.error("admin_tools::fetch_json_response({0}, {1}) > {2}\n{3}".format(phone_id, env, str(e), trace))
        return HttpResponse(''), e

# alternatively we could store the file (FileField) itself instead of the string of the JSON (TextField)
def upload_json_file(json_file, env):
    try:
        db = "admin_{0}".format(env)

        new_json = json.load(json_file)             # file to python json object
        phone_id = new_json['userID']
        datetime_now = get_now_datetime()

        # get_user raises an exception if does not exist, needs to be called before (new) entry is created
        user = get_user(phone_id, db) 

        valid, err = validate_json(new_json, user)
        if valid:
            user.update_client = True

            del new_json['SUPPORT']
            standardized_json = json.dumps(new_json)    # need to convert python json object to standard JSON string
            entry = get_client_update_entry(phone_id, db)
            if entry:
                entry.playerjson = standardized_json
            else:
                # creates new document in the database by default
                entry = UserClientUpdateJson.objects.using(db).create(  phone_id=phone_id, playerjson=standardized_json, 
                                                                        creation_date=datetime_now, last_updated=datetime_now)  # optional
            # save documents
            entry.save()
            user.save()

            return phone_id, None

        else:
            return None, err

    except Exception as e:              # can raise ValueError if not json
        trace = traceback.format_exc()
        logger.error("admin_tools::upload_json_file(file, {0}) > {1}\n{2}".format(env, str(e), trace))
        return None, e

def get_client_update_entry(phone_id, db):
    try:
        return UserClientUpdateJson.objects.using(db).get(phone_id=phone_id)

    except ObjectDoesNotExist:
        return None

def validate_json(json_data, wuser):
    
    if 'SUPPORT' not in json_data:
        return False, "JSON doesn't have 'SUPPORT' field!"

    if json_data['SUPPORT']['MONGO_ID'] != wuser.id:
        return False, "MongoID doesn't match!"

    if json_data['userID'] != wuser.phone_id:
        return False, "Phone ID doesn't match!"

    return True, ''
            
        








def insert_update_data(data, context):

    book = xlrd.open_workbook(data.masterload.name)

    # BOOKS
    sheet = book.sheet_by_name('Books')

    for books in range(1, sheet.nrows):
        id = sheet.cell(books, 0).value
        name = sheet.cell(books, 1).value
        display_order = sheet.cell(books, 2).value
        available = sheet.cell(books, 3).value
        book_prize_id = sheet.cell(books, 4).value
        recipes = sheet.cell(books, 5).value
        mail_id = sheet.cell(books, 6).value
        delete_flag = sheet.cell(books, 7).value

        display_order = get_sanitized_int(display_order, 'Books', 'display_order')

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            Books.objects.create(name=name, display_order=display_order, available=available,
                                 book_prize_id=book_prize_id, reward_list=ast.literal_eval(recipes),
                                 recipes=ast.literal_eval(recipes), mail_id=mail_id, delete_flag=delete_flag)
        else:
            db_book = Books.objects.get(id=id)
            if db_book:
                db_book.name = name
                db_book.display_order = display_order
                db_book.available = available
                db_book.book_prize_id = book_prize_id
                db_book.recipes = ast.literal_eval(recipes)
                db_book.mail_id = mail_id
                db_book.delete_flag = delete_flag
                db_book.save()

    # BOOKPRIZES
    sheet = book.sheet_by_name('BookPrizes')

    for bookprize in range(1, sheet.nrows):
        id = sheet.cell(bookprize, 0).value
        name = sheet.cell(bookprize, 1).value
        type = sheet.cell(bookprize, 2).value
        reward_id = sheet.cell(bookprize, 3).value
        quantity = sheet.cell(bookprize, 4).value
        delete_flag = sheet.cell(bookprize, 5).value

        quantity = get_sanitized_int(quantity, 'BookPrizes', 'quantity')
        reward_id = get_sanitized_string_int(reward_id)

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            BookPrizes.objects.create(name=name, type=type, reward_id=reward_id, quantity=quantity,
                                      delete_flag=delete_flag)
        else:
            db_bookprizes = BookPrizes.objects.get(id=id)
            if db_bookprizes:
                db_bookprizes.name = name
                db_bookprizes.type = type
                db_bookprizes.reward_id = reward_id
                db_bookprizes.quantity = quantity
                db_bookprizes.delete_flag = delete_flag
                db_bookprizes.save()

    # RECIPES
    sheet = book.sheet_by_name('Recipes')

    for recipe in range(1, sheet.nrows):
        id = sheet.cell(recipe, 0).value
        name = sheet.cell(recipe, 1).value
        hint = sheet.cell(recipe, 2).value
        display_order = sheet.cell(recipe, 3).value
        replay_flag = sheet.cell(recipe, 4).value
        ingredient_list = sheet.cell(recipe, 5).value
        score_list = sheet.cell(recipe, 6).value
        prize_list = sheet.cell(recipe, 7).value
        potion_list = sheet.cell(recipe, 8).value
        game_duration = sheet.cell(recipe, 9).value
        continue_duration = sheet.cell(recipe, 10).value
        delete_flag = sheet.cell(recipe, 11).value

        display_order = get_sanitized_int(display_order, 'Recipes', 'display_order')

        if int(replay_flag) == 0 or replay_flag is False:
            replay_flag = False
        elif int(replay_flag) == 1 or replay_flag is True:
            replay_flag = True

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            Recipes.objects.create(name=name, hint=hint, display_order=display_order, replay_flag=replay_flag,
                                   ingredient_list=ast.literal_eval(ingredient_list), 
                                   score_list=ast.literal_eval(score_list), prize_list=ast.literal_eval(prize_list),
                                   potion_list=ast.literal_eval(potion_list), game_duration=game_duration,
                                   continue_duration=continue_duration, delete_flag=delete_flag)
        else:
            db_recipe = Recipes.objects.get(id=id)
            if db_recipe:
                db_recipe.name = name
                db_recipe.hint = hint
                db_recipe.display_order = display_order
                db_recipe.reply_flag = replay_flag
                db_recipe.ingredient_list = ast.literal_eval(ingredient_list)
                db_recipe.score_list = ast.literal_eval(score_list)
                db_recipe.prize_list = ast.literal_eval(prize_list)
                db_recipe.potion_list = ast.literal_eval(potion_list)
                db_recipe.game_duration = game_duration
                db_recipe.continue_duration = continue_duration
                db_recipe.delete_flag = delete_flag
                db_recipe.save()

    # INGREDIENTS
    sheet = book.sheet_by_name('Ingredients')

    for ingredients in range(1, sheet.nrows):
        id = sheet.cell(ingredients, 0).value
        name = sheet.cell(ingredients, 1).value
        description = sheet.cell(ingredients, 2).value
        category_id = sheet.cell(ingredients, 3).value
        display_order = sheet.cell(ingredients, 4).value
        quality = sheet.cell(ingredients, 5).value
        effect_list = sheet.cell(ingredients, 6).value
        isInfinite = sheet.cell(ingredients, 7).value
        bottle_bg = sheet.cell(ingredients, 8).value
        color = sheet.cell(ingredients, 9).value
        coins_price = sheet.cell(ingredients, 10).value
        premium_price = sheet.cell(ingredients, 11).value
        currency_flag = sheet.cell(ingredients, 12).value
        delete_flag = sheet.cell(ingredients, 13).value

        display_order = get_sanitized_int(display_order, 'Ingredients', 'display_order')
        quality = get_sanitized_int(quality, 'Ingredients', 'quality')
        bottle_bg = get_sanitized_int(bottle_bg, 'Ingredients', 'bottle_bg')
        coins_price = get_sanitized_int(coins_price, 'Ingredients', 'coins_price')
        premium_price = get_sanitized_int(premium_price, 'Ingredients', 'premium_price')
        currency_flag = get_sanitized_int(currency_flag, 'Ingredients', 'currency_flag')

        if int(isInfinite) == 0 or isInfinite is False:
            isInfinite = False
        elif int(isInfinite) == 1 or isInfinite is True:
            isInfinite = True

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            Ingredients.objects.create(name=name, description=description, category_id=category_id,
                                       display_order=display_order, quality=quality, 
                                       effect_list=ast.literal_eval(effect_list),
                                       isInfinite=isInfinite,
                                       bottle_bg=bottle_bg, color=color, coins_price=coins_price,
                                       premium_price=premium_price,
                                       currency_flag=currency_flag,
                                       delete_flag=delete_flag)
        else:
            db_ingredients = Ingredients.objects.get(id=id)
            if db_ingredients:
                db_ingredients.name = name
                db_ingredients.description = description
                db_ingredients.category_id = category_id
                db_ingredients.display_order = display_order
                db_ingredients.quality = quality
                db_ingredients.effect_list = ast.literal_eval(effect_list)
                db_ingredients.isInfinite = isInfinite
                db_ingredients.bottle_bg = bottle_bg
                db_ingredients.color = color
                db_ingredients.coins_price = coins_price
                db_ingredients.premium_price = premium_price
                db_ingredients.currency_flag = currency_flag
                db_ingredients.delete_flag = delete_flag
                db_ingredients.save()

    # POTIONS
    sheet = book.sheet_by_name('Potions')

    for potion in range(1, sheet.nrows):
        id = sheet.cell(potion, 0).value
        name = sheet.cell(potion, 1).value
        description = sheet.cell(potion, 2).value
        type = sheet.cell(potion, 3).value
        display_order = sheet.cell(potion, 4).value
        color = sheet.cell(potion, 5).value             # To Be Deprecated
        icon = sheet.cell(potion, 6).value
        effect_list = sheet.cell(potion, 7).value
        delete_flag = sheet.cell(potion, 8).value

        type = get_sanitized_int(type, 'Potions', 'type')
        display_order = get_sanitized_int(display_order, 'Potions', 'display_order')
        color = get_sanitized_string_int(color)

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            Potions.objects.create(name=name, description=description, type=type, display_order=display_order,
                                   color=color, effect_list=effect_list, delete_flag=delete_flag, icon_name=icon)
        else:
            db_potion = Potions.objects.get(id=id)
            if db_potion:
                db_potion.name = name
                db_potion.description = description
                db_potion.type = type
                db_potion.display_order = display_order
                db_potion.color = color
                db_potion.icon_name = icon
                db_potion.effect_list = ast.literal_eval(effect_list)
                db_potion.delete_flag = delete_flag
                db_potion.save()

    # CATEGORIES
    sheet = book.sheet_by_name('Categories')

    for category in range(1, sheet.nrows):
        id = sheet.cell(category, 0).value
        name = sheet.cell(category, 1).value
        description = sheet.cell(category, 2).value
        type = sheet.cell(category, 3).value
        color = sheet.cell(category, 4).value
        delete_flag = sheet.cell(category, 5).value

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            Categories.objects.create(name=name, description=description, type=type, color=color,
                                      delete_flag=delete_flag)
        else:
            db_category = Categories.objects.get(id=id)
            if db_category:
                db_category.name = name
                db_category.description = description
                db_category.type = type
                db_category.color = color
                db_category.delete_flag = delete_flag
                db_category.save()

    # AVATAR ITEMS
    sheet = book.sheet_by_name('AvatarItems')

    for avataritem in range(1, sheet.nrows):
        id = sheet.cell(avataritem, 0).value
        name = sheet.cell(avataritem, 1).value
        layer_name = sheet.cell(avataritem, 2).value
        description = sheet.cell(avataritem, 3).value
        category_id = sheet.cell(avataritem, 4).value
        display_order = sheet.cell(avataritem, 5).value
        slots_layer = sheet.cell(avataritem, 6).value
        coins_price = sheet.cell(avataritem, 7).value
        premium_price = sheet.cell(avataritem, 8).value
        currency_flag = sheet.cell(avataritem, 9).value
        delete_flag = sheet.cell(avataritem, 10).value

        display_order = get_sanitized_int(display_order, 'AvatarItems', 'display_order')
        slots_layer = get_sanitized_int(slots_layer, 'AvatarItems', 'slots_layer')
        coins_price = get_sanitized_int(coins_price, 'AvatarItems', 'coins_price')
        premium_price = get_sanitized_int(premium_price, 'AvatarItems', 'premium_price')
        currency_flag = get_sanitized_int(currency_flag, 'AvatarItems', 'currency_flag')

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            AvatarItems.objects.create(name=name, layer_name=layer_name, description=description, category_id=category_id,
                                       display_order=display_order, slots_layer=slots_layer, coins_price=coins_price,
                                       premium_price=premium_price, currency_flag=currency_flag, delete_flag=delete_flag)
        else:
            db_avatar = AvatarItems.objects.get(id=id)
            if db_avatar:
                db_avatar.name = name
                db_avatar.layer_name = layer_name
                db_avatar.description = description
                db_avatar.category_id = category_id
                db_avatar.display_order = display_order
                db_avatar.slots_layer = slots_layer
                db_avatar.coins_price = coins_price
                db_avatar.premium_price = premium_price
                db_avatar.currency_flag = currency_flag
                db_avatar.delete_flag = delete_flag
                db_avatar.save()

    # EMAILTEMPLATES
    sheet = book.sheet_by_name('EmailTemplates')

    for template in range(1, sheet.nrows):
        id = sheet.cell(template, 0).value
        sender_id = sheet.cell(template, 1).value
        attach_list = sheet.cell(template, 2).value
        premium_currency = sheet.cell(template, 3).value
        free_currency = sheet.cell(template, 4).value
        stamina_potion = sheet.cell(template, 5).value
        body_text = sheet.cell(template, 6).value
        delete_flag = sheet.cell(template, 7).value

        premium_currency = get_sanitized_string_int(premium_currency)
        free_currency = get_sanitized_string_int(free_currency)
        stamina_potion = get_sanitized_string_int(stamina_potion)

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            EmailTemplates.objects.create(sender_id=sender_id, attach_list=ast.literal_eval(attach_list), premium_currency=premium_currency,
                                          free_currency=free_currency, stamina_potion=stamina_potion, body_text=body_text,
                                          delete_flag=delete_flag)
        else:
            db_template = EmailTemplates.objects.get(id=id)
            if db_template:
                db_template.sender_id = sender_id
                db_template.attach_list = ast.literal_eval(attach_list)
                db_template.premium_currency = premium_currency
                db_template.free_currency = free_currency
                db_template.stamina_potion = stamina_potion
                db_template.body_text = body_text
                db_template.delete_flag = delete_flag
                db_template.save()

    # CHARACTERS
    sheet = book.sheet_by_name('Characters')

    for character in range(1, sheet.nrows):
        id = sheet.cell(character, 0).value
        first_name = sheet.cell(character, 1).value
        last_name = sheet.cell(character, 2).value
        shorter = sheet.cell(character, 3).value
        initial = sheet.cell(character, 4).value
        romanceable = sheet.cell(character, 5).value
        delete_flag = sheet.cell(character, 6).value

        if int(romanceable) == 0 or romanceable is False:
            romanceable = False
        elif int(romanceable) == 1 or romanceable is True:
            romanceable = True

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            Characters.objects.create(first_name=first_name, last_name=last_name, shorter=shorter, initial=initial,
                                      romanceable=romanceable, delete_flag=delete_flag)
        else:
            db_character = Characters.objects.get(id=id)
            if db_character:
                db_character.first_name = first_name
                db_character.last_name = last_name
                db_character.shorter = shorter
                db_character.initial = initial
                db_character.romanceable = romanceable
                db_character.delete_flag = delete_flag
                db_character.save()

    # CLOTHINGCOORDINATES
    sheet = book.sheet_by_name('ClothingCoordinates')

    for coordinates in range(1, sheet.nrows):
        id = sheet.cell(coordinates, 0).value
        name = sheet.cell(coordinates, 1).value
        description = sheet.cell(coordinates, 2).value
        item_list = sheet.cell(coordinates, 3).value
        coins_price = sheet.cell(coordinates, 4).value
        premium_price = sheet.cell(coordinates, 5).value
        currency_flag = sheet.cell(coordinates, 6).value
        delete_flag = sheet.cell(coordinates, 7).value

        coins_price = get_sanitized_int(coins_price, 'ClothingCoordinates', 'coins_price')
        premium_price = get_sanitized_int(premium_price, 'ClothingCoordinates', 'premium_price')
        currency_flag = get_sanitized_int(currency_flag, 'ClothingCoordinates', 'currency_flag')

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            ClothingCoordinates.objects.create(name=name, description=description, item_list=ast.literal_eval(item_list),
                                               coins_price=coins_price, premium_price=premium_price,
                                               currency_flag=currency_flag, delete_flag=delete_flag)
        else:
            db_clooting = ClothingCoordinates.objects.get(id=id)
            if db_clooting:
                db_clooting.name = name
                db_clooting.description = description
                db_clooting.item_list = ast.literal_eval(item_list)
                db_clooting.coins_price = coins_price
                db_clooting.premium_price = premium_price
                db_clooting.currency_flag = currency_flag
                db_clooting.delete_flag = delete_flag
                db_clooting.save()

    # AFFINITIES
    sheet = book.sheet_by_name('Affinities')

    for affinities in range(1, sheet.nrows):
        id = sheet.cell(affinities, 0).value
        name = sheet.cell(affinities, 1).value
        grade = sheet.cell(affinities, 2).value
        total_affinity = sheet.cell(affinities, 3).value
        delete_flag = sheet.cell(affinities, 4).value

        total_affinity = get_sanitized_int(total_affinity, 'Affinities', 'total_affinity')

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            Affinities.objects.create(name=name, grade=grade, total_affinity=total_affinity, delete_flag=delete_flag)
        else:
            db_affinities = Affinities.objects.get(id=id)
            if db_affinities:
                db_affinities.name = name
                db_affinities.grade = grade
                db_affinities.total_affinity = total_affinity
                db_affinities.delete_flag = delete_flag
                db_affinities.save()

    # GAMEPROPERTIES
    sheet = book.sheet_by_name('GameProperties')

    for game in range(1, sheet.nrows):
        id = sheet.cell(game, 0).value
        name = sheet.cell(game, 1).value
        value = sheet.cell(game, 2).value
        event_flag = sheet.cell(game, 3).value
        start_date = sheet.cell(game, 4).value
        end_date = sheet.cell(game, 5).value
        delete_flag = sheet.cell(game, 6).value

        value = get_sanitized_string_int(value)

        if int(event_flag) == 0 or event_flag is False:
            event_flag = False
        elif int(event_flag) == 1 or event_flag is True:
            event_flag = True

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if not start_date or start_date == 'None':
            start_date = None
        if not end_date or end_date == 'None':
            end_date = None

        if id == 0:
            GameProperties.objects.create(name=name, value=value, event_flag=event_flag, start_date=start_date,
                                          end_date=end_date, delete_flag=delete_flag)
        else:
            db_game = GameProperties.objects.get(id=id)
            if db_game:
                db_game.name = name
                db_game.value = value
                db_game.event_flag = event_flag
                if start_date:
                    db_game.start_date = datetime(*xlrd.xldate_as_tuple(start_date, book.datemode))
                else:
                    db_game.start_date = None
                if end_date:
                    db_game.end_date = datetime(*xlrd.xldate_as_tuple(end_date, book.datemode))
                else:
                    db_game.end_date = None
                db_game.delete_flag = delete_flag
                db_game.save()

    # SHOPITEMS
    sheet = book.sheet_by_name('ShopItems')

    for shop in range(1, sheet.nrows):
        id = sheet.cell(shop, 0).value
        name = sheet.cell(shop, 1).value
        price = sheet.cell(shop, 2).value
        item_index = sheet.cell(shop, 3).value
        product_id = sheet.cell(shop, 4).value
        premium_qty = sheet.cell(shop, 5).value
        bundle_items = sheet.cell(shop, 6).value
        delete_flag = sheet.cell(shop, 7).value

        item_index = get_sanitized_int(item_index, 'ShopItems', 'item_index')
        premium_qty = get_sanitized_int(premium_qty, 'ShopItems', 'premium_qty')

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            ShopItems.objects.create(name=name, price=price, item_index=item_index, product_id=product_id,
                                     premium_qty=premium_qty, bundle_items=ast.literal_eval(bundle_items),
                                     delete_flag=delete_flag)
        else:
            db_shop = ShopItems.objects.get(id=id)
            if db_shop:
                db_shop.name = name
                db_shop.price = price
                db_shop.item_index = item_index
                db_shop.product_id = product_id
                db_shop.premium_qty = premium_qty
                db_shop.bundle_items = ast.literal_eval(bundle_items)
                db_shop.delete_flag = delete_flag
                db_shop.save()

   # GLOSSARY
    sheet = book.sheet_by_name('Glossary')

    for glossary in range(1, sheet.nrows):
        id = sheet.cell(glossary, 0).value
        name = sheet.cell(glossary, 1).value
        category_id = sheet.cell(glossary, 2).value
        display_order = sheet.cell(glossary, 3).value
        body_text = sheet.cell(glossary, 4).value
        delete_flag = sheet.cell(glossary, 5).value

        display_order = get_sanitized_int(display_order, 'Glossary', 'display_order')

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            Glossary.objects.create(name=name, category_id=category_id, display_order=display_order,
                                    body_text=body_text, delete_flag=delete_flag)
        else:
            db_glossary = Glossary.objects.get(id=id)
            if db_glossary:
                db_glossary.name = name
                db_glossary.category_id = category_id
                db_glossary.display_order = display_order
                db_glossary.body_text = body_text
                db_glossary.delete_flag = delete_flag
                db_glossary.save()

    # SCENE TABLES
    scenes = book.sheet_by_name('Scenes')

    for scene in range(1, scenes.nrows):
        id = scenes.cell(scene, 0).value
        scene_path = scenes.cell(scene, 1).value
        EI_id = scenes.cell(scene, 2).value
        mail_template_id = scenes.cell(scene, 3).value
        book_id = scenes.cell(scene, 4).value
        stamina_deduction_flag = scenes.cell(scene, 5).value
        regeneration_flag = scenes.cell(scene, 6).value
        delete_flag = scenes.cell(scene, 7).value

        scene_path = sanitize_scene_path(scene_path)

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if int(stamina_deduction_flag) == 0 or stamina_deduction_flag is False:
            stamina_deduction_flag = False
        elif int(stamina_deduction_flag) == 1 or stamina_deduction_flag is True:
            stamina_deduction_flag = True

        if int(regeneration_flag) == 0 or regeneration_flag is False:
            regeneration_flag = False
        elif int(regeneration_flag) == 1 or regeneration_flag is True:
            regeneration_flag = True

        if id == 0:
            SceneTable.objects.create(scene_path=scene_path, EI_id=EI_id, mail_template_id=mail_template_id,
                                      stamina_deduction_flag=False, regeneration_flag=False, book_id=book_id,
                                      delete_flag=delete_flag)
        else:
            db_scenes = SceneTable.objects.get(id=id)
            if db_scenes:
                db_scenes.scene_path = scene_path
                db_scenes.EI_id = EI_id
                db_scenes.mail_template_id = mail_template_id
                db_scenes.book_id = book_id
                db_scenes.stamina_deduction_flag = stamina_deduction_flag
                db_scenes.regeneration_flag = regeneration_flag
                db_scenes.save()

    # EI TABLES
    eis = book.sheet_by_name('EI')

    for ei in range(1, eis.nrows):
        id = eis.cell(ei, 0).value
        name = eis.cell(ei, 1).value

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            EI.objects.create(name=name)
        else:
            db_ei = EI.objects.get(id=id)
            if db_scenes:
                db_ei.name=name
                db_ei.save()

    # LogIn Bonus Master
    sheet = book.sheet_by_name('LogInBonusesMaster')

    bonus_index = 0
    for bonus in range(1, sheet.nrows):
        id = sheet.cell(bonus, 0).value
        bonus_id = sheet.cell(bonus, 2).value
        quantity = sheet.cell(bonus, 3).value
        bonus_description = sheet.cell(bonus, 4).value
        delete_flag = sheet.cell(bonus, 5).value

        if int(delete_flag) == 0 or delete_flag is False:
            delete_flag = False
        elif int(delete_flag) == 1 or delete_flag is True:
            delete_flag = True

        if id == 0:
            LogInBonusesMaster.objects.create(bonus_index=bonus_index, bonus_id=bonus_id, quantity=quantity,
                                              bonus_description=bonus_description, delete_flag=delete_flag)
        else:
            bonus_items = LogInBonusesMaster.objects.get(id=id)
            if bonus_items:
                bonus_items.bonus_index = bonus_index
                bonus_items.bonus_id = bonus_id
                bonus_items.quantity = quantity
                bonus_items.bonus_description = bonus_description
                bonus_items.delete_flag = delete_flag
                bonus_items.save()

        bonus_index += 1

    cache.delete('mst_dict')
    cache.clear()

    context['message'] = 'Master data uploaded Successfully !!'
