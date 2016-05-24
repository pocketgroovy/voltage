import json
from witches.mail import send_mail_to_user, give_user_howtos_mail_attachment, check_if_scene_has_mail
from witches.utils.custom_exceptions import NoValueFoundError

__author__ = 'yoshi.miyamoto'


from django.utils import unittest
from django.test.client import Client
from django.core.cache import cache
from pymongo import MongoClient
from witches.models import *
import datetime
from django.utils.timezone import utc

import const


def get_db(db_name=None):
    client = MongoClient('localhost', 27017)
    return client[db_name]


const.pw_length = 4
const.stamina_ticket = 0
const.closet_ticket = 2

const.system = 0
const.chara = 1
const.system_name = 'K&C'

const.type_ingredient = 0
const.type_avatar = 1
const.type_coordinate = 2
const.type_closet = 3

const.ios_receipt = 'ewoJInNpZ25hdHVyZSIgPSAiQW5TR0t0WDZiQUhVOGdBcEI3L2NsMWoyQ3NVM2t2VUUyTWl1MVIzaUVtMXE5MUZzeDJxTUdPaS9ka3M1UVZDVWZvdHBsaXFlRWl2ejZVWUREc3VKR3RjTmdsQWluZk9JTHNNZ2kwNGZWQmU3V1hLS3VBSWVGck1FQ1dYWGRYemVUWkR3ZmZVamo4OERYSGxPT0V4YTV5OE5yT1NBUUZmVUtCdERqYVlNWmd2Q0FBQURWekNDQTFNd2dnSTdvQU1DQVFJQ0NCdXA0K1BBaG0vTE1BMEdDU3FHU0liM0RRRUJCUVVBTUg4eEN6QUpCZ05WQkFZVEFsVlRNUk13RVFZRFZRUUtEQXBCY0hCc1pTQkpibU11TVNZd0pBWURWUVFMREIxQmNIQnNaU0JEWlhKMGFXWnBZMkYwYVc5dUlFRjFkR2h2Y21sMGVURXpNREVHQTFVRUF3d3FRWEJ3YkdVZ2FWUjFibVZ6SUZOMGIzSmxJRU5sY25ScFptbGpZWFJwYjI0Z1FYVjBhRzl5YVhSNU1CNFhEVEUwTURZd056QXdNREl5TVZvWERURTJNRFV4T0RFNE16RXpNRm93WkRFak1DRUdBMVVFQXd3YVVIVnlZMmhoYzJWU1pXTmxhWEIwUTJWeWRHbG1hV05oZEdVeEd6QVpCZ05WQkFzTUVrRndjR3hsSUdsVWRXNWxjeUJUZEc5eVpURVRNQkVHQTFVRUNnd0tRWEJ3YkdVZ1NXNWpMakVMTUFrR0ExVUVCaE1DVlZNd2daOHdEUVlKS29aSWh2Y05BUUVCQlFBRGdZMEFNSUdKQW9HQkFNbVRFdUxnamltTHdSSnh5MW9FZjBlc1VORFZFSWU2d0Rzbm5hbDE0aE5CdDF2MTk1WDZuOTNZTzdnaTNvclBTdXg5RDU1NFNrTXArU2F5Zzg0bFRjMzYyVXRtWUxwV25iMzRucXlHeDlLQlZUeTVPR1Y0bGpFMU93QytvVG5STStRTFJDbWVOeE1iUFpoUzQ3VCtlWnRERWhWQjl1c2szK0pNMkNvZ2Z3bzdBZ01CQUFHamNqQndNQjBHQTFVZERnUVdCQlNKYUVlTnVxOURmNlpmTjY4RmUrSTJ1MjJzc0RBTUJnTlZIUk1CQWY4RUFqQUFNQjhHQTFVZEl3UVlNQmFBRkRZZDZPS2RndElCR0xVeWF3N1hRd3VSV0VNNk1BNEdBMVVkRHdFQi93UUVBd0lIZ0RBUUJnb3Foa2lHOTJOa0JnVUJCQUlGQURBTkJna3Foa2lHOXcwQkFRVUZBQU9DQVFFQWVhSlYyVTUxcnhmY3FBQWU1QzIvZkVXOEtVbDRpTzRsTXV0YTdONlh6UDFwWkl6MU5ra0N0SUl3ZXlOajVVUllISytIalJLU1U5UkxndU5sMG5rZnhxT2JpTWNrd1J1ZEtTcTY5Tkluclp5Q0Q2NlI0Szc3bmI5bE1UQUJTU1lsc0t0OG9OdGxoZ1IvMWtqU1NSUWNIa3RzRGNTaVFHS01ka1NscDRBeVhmN3ZuSFBCZTR5Q3dZVjJQcFNOMDRrYm9pSjNwQmx4c0d3Vi9abEwyNk0ydWVZSEtZQ3VYaGRxRnd4VmdtNTJoM29lSk9PdC92WTRFY1FxN2VxSG02bTAzWjliN1BSellNMktHWEhEbU9Nazd2RHBlTVZsTERQU0dZejErVTNzRHhKemViU3BiYUptVDdpbXpVS2ZnZ0VZN3h4ZjRjemZIMHlqNXdOelNHVE92UT09IjsKCSJwdXJjaGFzZS1pbmZvIiA9ICJld29KSW05eWFXZHBibUZzTFhCMWNtTm9ZWE5sTFdSaGRHVXRjSE4wSWlBOUlDSXlNREUwTFRBM0xUSXlJREUyT2pFMU9qTXlJRUZ0WlhKcFkyRXZURzl6WDBGdVoyVnNaWE1pT3dvSkluVnVhWEYxWlMxcFpHVnVkR2xtYVdWeUlpQTlJQ0l3TkRka1pETTJNalJrWWpobVlUVTVNREUyWkRnNE56VTRPV0UzTURJd1lqUXdObUV6Wm1RNUlqc0tDU0p2Y21sbmFXNWhiQzEwY21GdWMyRmpkR2x2YmkxcFpDSWdQU0FpTVRBd01EQXdNREV4TnpZMk5qa3lNU0k3Q2draVluWnljeUlnUFNBaU1TNHdJanNLQ1NKMGNtRnVjMkZqZEdsdmJpMXBaQ0lnUFNBaU1UQXdNREF3TURFeU5ETTRPVFV6TVNJN0Nna2ljWFZoYm5ScGRIa2lJRDBnSWpFaU93b0pJbTl5YVdkcGJtRnNMWEIxY21Ob1lYTmxMV1JoZEdVdGJYTWlJRDBnSWpFME1EWXdOekE1TXpJd01EQWlPd29KSW5WdWFYRjFaUzEyWlc1a2IzSXRhV1JsYm5ScFptbGxjaUlnUFNBaU1VTTJPRFEyUkVVdE9VUkdOUzAwTURRMUxVRkVRekV0TmpsR1JVUTNOVVkxUVRReElqc0tDU0p3Y205a2RXTjBMV2xrSWlBOUlDSnpjSGw2WDJWdGJXVjBkRjlsTURFd01TSTdDZ2tpYVhSbGJTMXBaQ0lnUFNBaU9EWTNPREU1TXpBNUlqc0tDU0ppYVdRaUlEMGdJbU52YlM1MmIyeDBZV2RsTG1WdWRDNXpjSGw2TG1WdUlqc0tDU0p3ZFhKamFHRnpaUzFrWVhSbExXMXpJaUE5SUNJeE5ERXhNRGMwTnpjeU1EQXdJanNLQ1NKd2RYSmphR0Z6WlMxa1lYUmxJaUE5SUNJeU1ERTBMVEE1TFRFNElESXhPakV5T2pVeUlFVjBZeTlIVFZRaU93b0pJbkIxY21Ob1lYTmxMV1JoZEdVdGNITjBJaUE5SUNJeU1ERTBMVEE1TFRFNElERTBPakV5T2pVeUlFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW05eWFXZHBibUZzTFhCMWNtTm9ZWE5sTFdSaGRHVWlJRDBnSWpJd01UUXRNRGN0TWpJZ01qTTZNVFU2TXpJZ1JYUmpMMGROVkNJN0NuMD0iOwoJImVudmlyb25tZW50IiA9ICJTYW5kYm94IjsKCSJwb2QiID0gIjEwMCI7Cgkic2lnbmluZy1zdGF0dXMiID0gIjAiOwp9'

now = datetime.datetime.utcnow().replace(tzinfo=utc)

class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        # Category
        Categories.objects.create(name='ingredient_category', description='Silver', type=0,
                                  color=000010)
        Categories.objects.create(name='ingredient_category2', description='Moonstone', type=0,
                                  color=000010)
        Categories.objects.create(name='ingredient_category3', description='Artemisia', type=0,
                                  color=000010)
        Categories.objects.create(name='ingredient_category4', description='Rosemary', type=0,
                                  color=000010)

        Categories.objects.create(name='avatar_category1', description='ACCESSORIES', type=1, color=00005)
        Categories.objects.create(name='avatar_category2', description='SKIN', type=1,color=00005)
        Categories.objects.create(name='avatar_category3', description='BOTTOMS', type=1, color=00005)
        Categories.objects.create(name='avatar_category4', description='DRESSES', type=1, color=00005)
        Categories.objects.create(name='avatar_category5', description='HAIRSTYLES', type=1, color=00005)
        Categories.objects.create(name='avatar_category6', description='HATS', type=1, color=00005)
        Categories.objects.create(name='avatar_category7', description='INTIMATES', type=1, color=00005)
        Categories.objects.create(name='avatar_category8', description='SHOES', type=1, color=00005)

        Categories.objects.create(name='glossary_category', description='Spells', type=2, color=00005)
        ingredient_category = Categories.objects.filter(name='ingredient_category')[0]
        ingredient_category2 = Categories.objects.filter(name='ingredient_category2')[0]
        ingredient_category3 = Categories.objects.filter(name='ingredient_category3')[0]
        ingredient_category4 = Categories.objects.filter(name='ingredient_category4')[0]

        avatar_category1 = Categories.objects.filter(name='avatar_category1')[0]
        avatar_category2 = Categories.objects.filter(name='avatar_category2')[0]
        avatar_category3 = Categories.objects.filter(name='avatar_category3')[0]
        avatar_category4 = Categories.objects.filter(name='avatar_category4')[0]
        avatar_category5 = Categories.objects.filter(name='avatar_category5')[0]
        avatar_category6 = Categories.objects.filter(name='avatar_category6')[0]
        avatar_category7 = Categories.objects.filter(name='avatar_category7')[0]
        avatar_category8 = Categories.objects.filter(name='avatar_category8')[0]

        # Ingredient
        Ingredients.objects.create(name='t_ingredient1', description=ingredient_category.description,
                                   category_id=ingredient_category.id, display_order=1, quality=1, isInfinite=False,
                                   coins_price=10, currency_flag=1)
        Ingredients.objects.create(name='t_ingredient2', description=ingredient_category2.description,
                                   category_id=ingredient_category2.id, display_order=4, quality=1, isInfinite=False,
                                   premium_price=5, currency_flag=3)
        Ingredients.objects.create(name='t_ingredient3', description=ingredient_category3.description,
                                   category_id=ingredient_category3.id, display_order=6, quality=1, isInfinite=False,
                                   coins_price=1, currency_flag=1)
        Ingredients.objects.create(name='t_ingredient4', description=ingredient_category4.description,
                                   category_id=ingredient_category4.id, display_order=6, quality=1, isInfinite=False,
                                   premium_price=3, currency_flag=3)
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]
        ingredient2 = Ingredients.objects.filter(name='t_ingredient2')[0]
        ingredient3 = Ingredients.objects.filter(name='t_ingredient3')[0]
        ingredient4 = Ingredients.objects.filter(name='t_ingredient4')[0]

        # AvatarItems
        cache.set('avatar_item1', AvatarItems.objects.create(category_id=avatar_category1.id,
                                                             description=avatar_category1.description,
                                                             name='Baseball Cap', premium_price=1, currency_flag=2,
                                                             slots_layer=0,
                                                             display_order=2))
        cache.set('avatar_item2', AvatarItems.objects.create(category_id=avatar_category2.id,
                                                             description=avatar_category2.description,
                                                             name='Shirt', slots_layer=0,
                                                             coins_price=2, currency_flag=3, display_order=4))
        cache.set('avatar_item3', AvatarItems.objects.create(category_id=avatar_category3.id,
                                                             description=avatar_category3.description, slots_layer=0,
                                                             name='Boots', coins_price=3, currency_flag=3,
                                                             display_order=3))
        cache.set('avatar_item4', AvatarItems.objects.create(category_id=avatar_category4.id,
                                                             description=avatar_category4.description, slots_layer=0,
                                                             name='Fedora', premium_price=5, currency_flag=2,
                                                             display_order=5))
        cache.set('avatar_item5', AvatarItems.objects.create(category_id=avatar_category5.id,
                                                             description=avatar_category5.description, slots_layer=0,
                                                             name='T-shirt', premium_price=1, currency_flag=2,
                                                             display_order=7))
        cache.set('avatar_item6', AvatarItems.objects.create(category_id=avatar_category6.id,
                                                             description=avatar_category6.description, slots_layer=0,
                                                             name='Jeans', coins_price=2, currency_flag=3,
                                                             display_order=10))
        cache.set('avatar_item7', AvatarItems.objects.create(category_id=avatar_category7.id,
                                                             description=avatar_category7.description, slots_layer=0,
                                                             name='short cardigan', premium_price=2, currency_flag=2,
                                                             display_order=12))
        cache.set('avatar_item8', AvatarItems.objects.create(category_id=avatar_category8.id,
                                                             description=avatar_category8.description, slots_layer=0,
                                                             name='black hair', coins_price=3, currency_flag=3,
                                                             display_order=24))

        avatar_item1 = AvatarItems.objects.filter(name='Baseball Cap')[0]
        avatar_item2 = AvatarItems.objects.filter(name='Shirt')[0]
        avatar_item3 = AvatarItems.objects.filter(name='Boots')[0]
        avatar_item4 = AvatarItems.objects.filter(name='Fedora')[0]
        avatar_item5 = AvatarItems.objects.filter(name='T-shirt')[0]
        avatar_item6 = AvatarItems.objects.filter(name='Jeans')[0]
        avatar_item7 = AvatarItems.objects.filter(name='short cardigan')[0]
        avatar_item8 = AvatarItems.objects.filter(name='black hair')[0]

        # Potion
        Potions.objects.create(name='t_potion1', description='test potion 1', type=1, color='yellow',
                               effect_list=[{'character_id': 1, 'effect_id': 1},
                                            {'character_id': 4, 'effect_id': 2}])
        Potions.objects.create(name='t_potion2', description='test potion 2', type=2, color='red',
                               effect_list=[{'character_id': 2, 'effect_id': 3},
                                            {'character_id': 5, 'effect_id': 4}])
        Potions.objects.create(name='t_potion3', description='test potion 3', type=3, color='blue',
                               effect_list=[{'character_id': 3, 'effect_id': 5},
                                            {'character_id': 6, 'effect_id': 6}])

        potion1 = Potions.objects.filter(name='t_potion1')[0]
        potion2 = Potions.objects.filter(name='t_potion2')[0]
        potion3 = Potions.objects.filter(name='t_potion3')[0]

        # Book Prizes
        BookPrizes.objects.create(name='t_bookprize1', type='avatar', reward_id=avatar_item1.id, quantity=1)
        BookPrizes.objects.create(name='t_bookprize2', type='ingredient', reward_id=ingredient1.id, quantity=3)
        BookPrizes.objects.create(name='t_bookprize3', type='avatar', reward_id=avatar_item2.id, quantity=5)
        bookprize1 = BookPrizes.objects.filter(name='t_bookprize1')[0]
        bookprize2 = BookPrizes.objects.filter(name='t_bookprize2')[0]
        bookprize3 = BookPrizes.objects.filter(name='t_bookprize3')[0]

        # Recipes
        Recipes.objects.create(name='t_recipe1', display_order=1, hint='t_hint1',
                               ingredient_list=[{'category': ingredient_category.id}, {'category': ingredient_category2.id}], replay_flag=False,
                               potion_list={'superior': potion1.id, 'master': potion2.id, 'basic': potion3.id},
                               score_list={'low': 0.25, 'mid': 0.5, 'high': 0.75},
                               prize_list={'low': bookprize1.id, 'mid': bookprize2.id, 'high': bookprize3.id},
                               game_duration=30, continue_duration=10)
        Recipes.objects.create(name='t_recipe2', display_order=2, hint='t_hint2',
                               ingredient_list=[{'category': ingredient_category3.id}, {'category': ingredient_category4.id}], replay_flag=False,
                               potion_list={'superior': potion3.id, 'master': potion1.id, 'basic': potion2.id},
                               score_list={'low': 0.25, 'mid': 0.5, 'high': 0.75},
                               prize_list={'low': bookprize3.id, 'mid': bookprize1.id, 'high': bookprize2.id},
                               game_duration=10, continue_duration=30)

        recipe1 = Recipes.objects.filter(name='t_recipe1')[0]
        recipe2 = Recipes.objects.filter(name='t_recipe2')[0]

        # Books
        Books.objects.create(name='book1', display_order=1, available=True,
                             book_prize_id=bookprize1.id, recipes=[{'recipe_id': recipe1.id, 'success_threshold': 20},
                                                                   {'recipe_id': recipe2.id, 'success_threshold': 100}])
        Books.objects.create(name='book2', display_order=1, available=True,
                             book_prize_id=bookprize1.id, recipes=[{'recipe_id': recipe1.id, 'success_threshold': 50},
                                                                   {'recipe_id': recipe2.id, 'success_threshold': 10}])
        book1 = Books.objects.filter(name='book1')[0]
        book2 = Books.objects.filter(name='book2')[0]

        # User
        cache.set('user1', WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                                                 email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='abcdefgh', closet=30, stamina_potion=1))

        cache.set('user2', WUsers.objects.create(last_name='t_last2', first_name='t_user2', gender='Female', work=[],
                                                 email='t_user2@test.com', birthday='08/20/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='12345678', closet=2, stamina_potion=0))

        WUsers.objects.create(last_name='t_last3', first_name='t_user3', gender='Female', work=[], stamina_potion=0,
                              email='t_user3@test.com', birthday='08/20/1999', free_currency=0,
                              premium_currency=0, ticket=2, delete_flag=0,
                              phone_id='a1b2c3d4', closet=3)

        cache.set('user4', WUsers.objects.create(last_name='t_last4', first_name='t_user4', gender='Female', work=[],
                                                 email='t_user4@test.com', birthday='01/2/1996', free_currency=0,
                                                 premium_currency=0, ticket=5, delete_flag=0, stamina_potion=0,
                                                 phone_id='9876qwer', closet=30))

        WUsers.objects.create(last_name='t_last5', first_name='t_user5', gender='Female', work=[],
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=2, delete_flag=0,
                              phone_id='zaq12wsx', closet=60, 
                              ticket_last_update=now-datetime.timedelta(seconds=7250))

        WUsers.objects.create(last_name='t_last6', first_name='t_user6', gender='Female', work=[],
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=4, delete_flag=0,
                              phone_id='98765432', closet=60, 
                              ticket_last_update=now-datetime.timedelta(seconds=28850))

        WUsers.objects.create(last_name='t_last7', first_name='t_user7', gender='Female', work=[],
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=1,
                              phone_id='qwerasdf', closet=60, 
                              ticket_last_update=now-datetime.timedelta(seconds=86400))

        WUsers.objects.create(last_name='t_last8', first_name='t_user8', gender='Female', work=[],
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000, stamina_potion=60,
                              premium_currency=20, ticket=5, delete_flag=0,
                              phone_id='zxcvasdf', closet=60, scene_id='Prologue/Prologue/Divide by Thirteen')

        cache.set('user9', WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                                                 email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='77777777', closet=30, stamina_potion=1))

        cache.set('user10', WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                                                 email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='55555555', closet=30, stamina_potion=1))

        user1 = WUsers.objects.filter(phone_id='abcdefgh')[0]
        user2 = WUsers.objects.filter(phone_id='12345678')[0]
        user3 = WUsers.objects.filter(phone_id='a1b2c3d4')[0]
        user4 = WUsers.objects.filter(phone_id='9876qwer')[0]
        user8 = WUsers.objects.filter(phone_id='zxcvasdf')[0]
        user9 = WUsers.objects.filter(phone_id='77777777')[0]
        user10 = WUsers.objects.filter(phone_id='55555555')[0]

        # User Characters
        affinities_dict = {"A": 0, "M": 0, "N": 0, "R": 0, "T": 0}
        UserCharacters.objects.create(user_id=user1.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user2.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user3.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user4.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user8.id, affinities=affinities_dict)

        # User Books
        UserBooks.objects.create(user_id=user1.id, book_list=[book1.id, book2.id])

        # User Item inventory
        UserItemInventory.objects.create(ingredient_id=ingredient1.id, user_id=user1.id, quantity=1)  # coin ingredient item
        UserItemInventory.objects.create(ingredient_id=ingredient2.id, user_id=user1.id, quantity=1)  # stone ingredient item
        UserItemInventory.objects.create(potion_id=potion1.id, user_id=user1.id, quantity=30)
        UserItemInventory.objects.create(potion_id=potion2.id, user_id=user1.id, quantity=11)
        UserItemInventory.objects.create(potion_id=potion2.id, user_id=user2.id, quantity=0)
        UserItemInventory.objects.create(potion_id=potion2.id, user_id=user3.id, quantity=1)

        # ClothingCoordination
        ClothingCoordinates.objects.create(item_list=[avatar_item1.id, avatar_item2.id, avatar_item3.id],
                                           name='Night Owl', description='Club Goer', premium_price=5, currency_flag=2)

        ClothingCoordinates.objects.create(item_list=[avatar_item4.id, avatar_item5.id, avatar_item6.id],
                                           name='Morning Sun', description='Sunday Brunch', coins_price=8,
                                           currency_flag=3)

        ClothingCoordinates.objects.create(item_list=[avatar_item4.id, avatar_item2.id, avatar_item6.id],
                                           name='Party', description='Evening Dress', premium_price=1, currency_flag=2)

        # UserClothingCoordination
        UserClothingCoordination.objects.create(user_id=user1.id, coordinate_list=[avatar_item4.id, avatar_item5.id,
                                                                                   avatar_item6.id])

        # UserAvatarItemsInCloset
        usercoordination_item = UserClothingCoordination.objects.filter(user_id=user1.id)[0]
        storecoordination_item = ClothingCoordinates.objects.filter(name='Night Owl')[0]
        storecoordination_coin_item = ClothingCoordinates.objects.filter(name='Morning Sun')[0]

        UserAvatarItemsInCloset.objects.create(user_id=user1.id, avatar_item_id=avatar_item1.id, quantity=1)
        UserAvatarItemsInCloset.objects.create(user_id=user1.id, avatar_item_id=avatar_item7.id, quantity=1)
        UserAvatarItemsInCloset.objects.create(user_id=user1.id, coordinate_item_id=usercoordination_item.id,
                                               quantity=1)
        UserAvatarItemsInCloset.objects.create(user_id=user1.id, coordinate_item_id=storecoordination_item.id,
                                               quantity=1)
        UserAvatarItemsInCloset.objects.create(user_id=user2.id, avatar_item_id=avatar_item8.id, quantity=1)
        UserAvatarItemsInCloset.objects.create(user_id=user2.id, coordinate_item_id=storecoordination_coin_item.id, quantity=1)
        UserAvatarItemsInCloset.objects.create(user_id=user10.id, avatar_item_id=avatar_item1.id, quantity=1)

        # GameProperties
        GameProperties.objects.create(name='default_free_currency', value=100)
        GameProperties.objects.create(name='default_premium_currency', value=1)
        GameProperties.objects.create(name='default_ticket', value=1000)
        GameProperties.objects.create(name='default_user_book', value='63720jdur9j2nf')
        GameProperties.objects.create(name='default_ticket_Refresh_Rate', value=240)
        GameProperties.objects.create(name='default_closet', value=30)
        GameProperties.objects.create(name='default_preppy', value=0)
        GameProperties.objects.create(name='default_funky', value=0)
        GameProperties.objects.create(name='default_rebel', value=0)
        GameProperties.objects.create(name='default_affinity', value=30)
        GameProperties.objects.create(name='version', value=1)
        GameProperties.objects.create(name='cumulative_max', value=30)
        GameProperties.objects.create(name='max_tickets', value=5)
        GameProperties.objects.create(name='default_ingredients', value={ingredient1.id: 1, ingredient2.id: 1, ingredient3.id: 1, ingredient4.id: 1})

        # EI Table
        EI.objects.create(name='chapter1')
        EI.objects.create(name='chapter2')

        chapter_image1 = EI.objects.filter(name='chapter1')[0]
        chapter_image2 = EI.objects.filter(name='chapter2')[0]

        # Characters
        Characters.objects.create(first_name='K&C', romanceable=1)
        Characters.objects.create(first_name='Anastasia', last_name='Petrova', initial='A', romanceable=1)
        Characters.objects.create(first_name='Rhys', last_name='Ceridwen', initial='R', romanceable=1)

        system_char = Characters.objects.filter(first_name='K&C')[0]
        anastasia = Characters.objects.filter(first_name='Anastasia')[0]
        rhys = Characters.objects.filter(first_name='Rhys')[0]

        # UserMailBox
        UserMailBox.objects.create(user_id=user1.id, title='Gifts for you!',
                                   message_body='you will enjoy all the great gifts attached to this mail',
                                   read_flag=False, sender_id=system_char.id, EI=chapter_image1.id, sender_flag=False,
                                   gifts=[{'id': avatar_item1.id, 'received_flag': False},
                                          {'id': potion1.id, 'received_flag': False}], premium_currency=2, free_currency=2,
                                   premium_received_flag=False, free_currency_received_flag=False, stamina_potion=5,
                                   stamina_potion_received_flag=False)

        UserMailBox.objects.create(user_id=user1.id, title='Gifts for you 2!',
                                   message_body='test message 2', sender_flag=False, premium_received_flag=False,
                                   read_flag=False, sender_id=anastasia.id, EI=chapter_image1.id,
                                   gifts=[{'id': avatar_item1.id, 'received_flag': False},
                                          {'id': potion1.id, 'received_flag': False}], premium_currency=12,
                                   free_currency=1, free_currency_received_flag=False, stamina_potion=0,
                                   stamina_potion_received_flag=False)

        UserMailBox.objects.create(user_id=user2.id, title="test message", message_body="this is the test message",
                                   read_flag=False, sender_id=user1.id, EI=chapter_image2.id,
                                   sender_flag=True, gifts=[{'id': ingredient1.id, 'received_flag': False},
                                                            {'id': storecoordination_item.id, 'received_flag': False}],
                                   premium_currency=10, free_currency=5, premium_received_flag=False,
                                   free_currency_received_flag=False, stamina_potion=3,
                                   stamina_potion_received_flag=False)

        UserMailBox.objects.create(user_id=user9.id, title='Gifts for you!',
                                   message_body='you will enjoy all the great gifts attached to this mail',
                                   read_flag=False, sender_id=system_char.id, EI=chapter_image1.id, sender_flag=False,
                                   gifts=[{'id': avatar_item1.id, 'received_flag': False},
                                          {'id': ingredient1.id, 'received_flag': False}], premium_currency=2, free_currency=2,
                                   premium_received_flag=False, free_currency_received_flag=False, stamina_potion=5,
                                   stamina_potion_received_flag=False)

        UserMailBox.objects.create(user_id=user10.id, title='Gifts for you!',
                                   message_body='you will enjoy all the great gifts attached to this mail',
                                   read_flag=False, sender_id=system_char.id, EI=chapter_image1.id, sender_flag=False,
                                   gifts=[{'id': avatar_item1.id, 'received_flag': True},
                                          {'id': ingredient1.id, 'received_flag': False}], stamina_potion_received_flag=False,
                                   free_currency_received_flag=False, premium_received_flag=False)
        # LogInBonusesMaster
        LogInBonusesMaster.objects.create(bonus_id=avatar_item1.id, quantity=1,
                                          bonus_description='BaseBall Cap')
        LogInBonusesMaster.objects.create(bonus_id=potion1.id,  quantity=1,
                                          bonus_description='potion')
        LogInBonusesMaster.objects.create(bonus_id=ingredient1.id,  quantity=1,
                                          bonus_description='ingredients')
        LogInBonusesMaster.objects.create(bonus_id=avatar_item2.id,quantity=1,
                                          bonus_description='Shirt')
        LogInBonusesMaster.objects.create(bonus_id='', quantity=10,
                                          bonus_description='Bonus Currency!')
        LogInBonusesMaster.objects.create(bonus_id=avatar_item1.id,  quantity=1,
                                          bonus_description='eyes')
        LogInBonusesMaster.objects.create(bonus_id=avatar_item1.id, quantity=1,
                                          bonus_description='Bonus Potion!')
        LogInBonusesMaster.objects.create(bonus_id='', quantity=1,
                                          bonus_description='Bonus Stone!')

        # VariableLogInBonuses
        VariableLogInBonuses.objects.create(login_cycle=2, cumulative=3, reward_id=potion1.id, type='Potion',
                                            quantity=1, bonus_description='potion')

        # price_type 0 = stamina potion, stone = 1
        # max = 0 is unlimited
        ItemExchangeRate.objects.create(ticket=const.stamina_ticket, ticket_quantity=1, ticket_price=1, max=5,
                                        exchange_type=1)  # stamina
        ItemExchangeRate.objects.create(ticket=const.closet_ticket, ticket_quantity=5, ticket_price=1, max=0,
                                        exchange_type=2)  # closet

        # mail
        mail_attachment = [{'id': avatar_item7.id, 'received_flag': False}, {'id': avatar_item8.id,
                                                                             'received_flag': False}]
        EmailTemplates.objects.create(premium_currency='1', sender_id=anastasia.id, free_currency='100',
                                      body_text='unittest', attach_list=mail_attachment, stamina_potion='None')
        mail = EmailTemplates.objects.get(body_text='unittest')

        EmailTemplates.objects.create(premium_currency='10', sender_id=rhys.id, free_currency='100',
                                      body_text='howtos_mail', stamina_potion='5', attach_list=mail_attachment)
        howtos_mail = EmailTemplates.objects.get(body_text='howtos_mail')

        GameProperties.objects.create(name='default_howtos_mail', value=howtos_mail.id)

        # shop items
        ShopItems.objects.create(name='Stamina Potion Hoard', item_index=9, product_id='com.voltage.ent.witch.104',
                                 price=49.99, premium_qty=60)

        # scene table
        SceneTable.objects.create(scene_path='Prologue/Prologue/Divide by Thirteen', mail_template_id=mail.id)
        SceneTable.objects.create(scene_path='Prologue/Prologue/Bewitching Meeting', mail_template_id='')
        SceneTable.objects.create(scene_path='Prologue/Prologue/Mending Luna', mail_template_id='')
        SceneTable.objects.create(scene_path='Prologue/Prologue/Mending Luna', mail_template_id='')


    def test_http_get_all_mails(self):
        user = WUsers.objects.filter(phone_id='abcdefgh')
        mail = UserMailBox.objects.filter(user_id=user[0].id)

        c = Client()

        # invalid mail id
        param = {'phone_id': 'abcdefgh', 'mail_id': mail}
        r = c.post('/witches/open_mail/0', param)
        self.assertEqual(r.status_code, 200, 'open mail failed')
        self.assertEqual(UserMailBox.objects.filter(user_id=user[0].id, read_flag=False).count(), 2)

        # open a mail
        param = {'phone_id': 'abcdefgh', 'mail_id': mail[0].id}
        r = c.post('/witches/open_mail/0', param)
        self.assertEqual(r.status_code, 200, 'open mail failed')
        self.assertEqual(UserMailBox.objects.filter(user_id=user[0].id, read_flag=False).count(), 1)


    def test_mail_gift_by_complete_scene(self):
        c = Client()
        affinities = '{"A": 10, "B": 40}'
        choices = '{"Prologue/Prologue/Divide by Thirteen": "A"}'
        param = {'phone_id': 'zxcvasdf', 'affinities': affinities, 'stamina_potions': 48,
                 'choices': choices}
        c.post('/witches/complete_scene/1', param)

        updated_user = WUsers.objects.filter(phone_id='zxcvasdf')[0]

        avatar_item7 = AvatarItems.objects.filter(name='short cardigan')[0]
        avatar_item8 = AvatarItems.objects.filter(name='black hair')[0]

        usermail = UserMailBox.objects.filter(user_id=updated_user.id)
        anastasia = Characters.objects.get(first_name='Anastasia')
        self.assertEqual(usermail.count(), 1, 'user has one mail but got ' + str(usermail.count()))
        self.assertTrue(avatar_item7.id in usermail[0].gifts[0].values(), str(avatar_item7.id) + ' item is not in the gifts')
        self.assertTrue(avatar_item8.id in usermail[0].gifts[1].values(), str(avatar_item8.id) + ' item is not in the gifts')
        self.assertEqual(usermail[0].sender_id, anastasia.id, 'sender should be: ' + anastasia.id + ' but got ' + usermail[0].sender_id)

    def test_send_howtos_mail(self):
        c = Client()
        howtos_ID = '/tutorial/prologue/FIRST_MAIL_PICKEDUP'
        param = {'phone_id': 'zxcvasdf', 'howtos_progress': howtos_ID}
        c.post('/witches/howtos_progress/1', param)

        updated_user = WUsers.objects.filter(phone_id='zxcvasdf')[0]

        usermail = UserMailBox.objects.filter(user_id=updated_user.id)
        rhys = Characters.objects.get(first_name='Rhys')
        self.assertEqual(usermail.count(), 1, 'user has one mail but got ' + str(usermail.count()))
        self.assertEqual(usermail[0].sender_id, rhys.id, 'sender should be: ' + rhys.id + ' but got ' + str(usermail[0].sender_id))
        self.assertEqual(usermail[0].premium_currency, 10, 'premium should be 10 but got ' + str(usermail[0].premium_currency))
        self.assertTrue(usermail[0].premium_received_flag)
        self.assertTrue(usermail[0].free_currency_received_flag)
        self.assertEqual(updated_user.premium_currency, 30, ' user premium currency should be 30 but got ' + str(updated_user.premium_currency))
        self.assertEqual(updated_user.free_currency, 1100, ' user free currency should be 1100 but got ' + str(updated_user.free_currency))
        self.assertEqual(updated_user.stamina_potion, 65, ' user free currency should be 65 but got ' + str(updated_user.stamina_potion))

        avatar_item7 = AvatarItems.objects.filter(name='short cardigan')[0]
        avatar_item8 = AvatarItems.objects.filter(name='black hair')[0]
        user_avatars = list(UserAvatarItemsInCloset.objects.filter(user_id=updated_user.id).values('avatar_item_id'))
        if len(user_avatars) > 0:
            for user_avatar in user_avatars:
                if avatar_item7.id == user_avatar['avatar_item_id']:
                    self.assertTrue(user_avatar['avatar_item_id'], avatar_item7.id)
                elif avatar_item8.id == user_avatar['avatar_item_id']:
                    self.assertTrue(user_avatar['avatar_item_id'], avatar_item8.id)

    def test_send_mail_to_user(self):
        context = ''
        type_res = 1
        user = WUsers.objects.filter(phone_id='zxcvasdf')[0]
        mail = EmailTemplates.objects.get(body_text='unittest')
        send_mail_to_user(mail.id, user.id, context, 'test_send_mail_to_user', type_res)

        usermail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(usermail.count(), 1, 'user has one mail but got ' + str(usermail.count()))
        self.assertEqual(usermail[0].premium_currency, 1, 'user should have 1 premium_currency in  mail but got ' + str(usermail[0].premium_currency))
        self.assertEqual(usermail[0].free_currency, 100, 'user should have 100 free_currency in mail but got ' + str(usermail[0].free_currency))
        self.assertEqual(usermail[0].stamina_potion, None, 'user should have none stamina_potion in mail but got ' + str(usermail[0].stamina_potion))
        self.assertEqual(usermail[0].sender_type_for_metrics, 'Character', 'mail sender type for metrics should be Character but got ' + str(usermail[0].sender_type_for_metrics))

    def test_give_user_howtos_mail_attachment(self):
        user = WUsers.objects.filter(phone_id='zxcvasdf')[0]
        context = ''
        type_res = 1
        other = ''
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]
        storecoordination_item = ClothingCoordinates.objects.filter(name='Night Owl')[0]
        UserMailBox.objects.create(user_id=user.id, title="HOWTOS MAIL", message_body="this is the test message",
                                   read_flag=False, sender_flag=True,
                                   gifts=[{'id': ingredient1.id, 'received_flag': False}, {'id': storecoordination_item.id,
                                                                                           'received_flag': False}],
                                   premium_currency=10, free_currency=5, premium_received_flag=False,
                                   free_currency_received_flag=False, stamina_potion=3,
                                   stamina_potion_received_flag=False)

        usermail = UserMailBox.objects.filter(user_id=user.id)
        give_user_howtos_mail_attachment(user, usermail[0].id, other, context, type_res)
        updated_user = WUsers.objects.filter(phone_id='zxcvasdf')[0]
        received_usermail = UserMailBox.objects.filter(user_id=user.id)

        self.assertEqual(received_usermail.count(), 1, 'user has one mail but got ' + str(usermail.count()))
        self.assertEqual(received_usermail[0].premium_currency, 10, 'premium should be 10 but got ' + str(usermail[0].premium_currency))
        self.assertTrue(received_usermail[0].premium_received_flag)
        self.assertTrue(received_usermail[0].free_currency_received_flag)
        self.assertEqual(updated_user.premium_currency, 30, ' user premium currency should be 30 but got ' + str(updated_user.premium_currency))
        self.assertEqual(updated_user.free_currency, 1005, ' user free currency should be 1005 but got ' + str(updated_user.free_currency))
        self.assertEqual(updated_user.stamina_potion, 63, ' user free currency should be 63 but got ' + str(updated_user.stamina_potion))

    def test_receive_items(self):
        user = WUsers.objects.filter(phone_id='77777777')
        mail = UserMailBox.objects.filter(user_id=user[0].id)

        c = Client()
        param = {'phone_id': '77777777', 'mail_id': mail[0].id}
        r = c.post('/witches/open_mail/0', param)
        user = WUsers.objects.get(phone_id='77777777')

        avatar_item1 = AvatarItems.objects.filter(name='Baseball Cap')[0]
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]
        update_mail = UserMailBox.objects.filter(user_id=user.id)

        self.assertEqual(r.status_code, 200, 'open mail failed')
        self.assertEqual(UserMailBox.objects.filter(user_id=user.id, read_flag=False).count(), 0)
        self.assertEqual(user.premium_currency, 22, ' user premium currency should be 22 but got ' + str(user.premium_currency))
        self.assertEqual(user.free_currency, 1002, ' user free_currency should be 1002 but got ' + str(user.free_currency))
        self.assertEqual(user.stamina_potion, 6, ' user stamina_potion should be 6 but got ' + str(user.stamina_potion))
        user_avatar = UserAvatarItemsInCloset.objects.get(user_id=user.id)
        self.assertEqual(user_avatar.avatar_item_id, avatar_item1.id, ' user avatar should be ' + avatar_item1.id + ' but got ' + user_avatar.avatar_item_id)
        ingredient = UserItemInventory.objects.get(user_id=user.id)
        self.assertEqual(ingredient.ingredient_id, ingredient1.id, ' user ingredient should be ' + ingredient1.id + ' but got ' + ingredient.ingredient_id)
        self.assertTrue(update_mail[0].premium_received_flag)
        self.assertTrue(update_mail[0].free_currency_received_flag)
        self.assertTrue(update_mail[0].stamina_potion_received_flag)

    def test_receive_items_no_currencies(self):
        user = WUsers.objects.filter(phone_id='55555555')
        mail = UserMailBox.objects.filter(user_id=user[0].id)

        c = Client()
        param = {'phone_id': '55555555', 'mail_id': mail[0].id}
        r = c.post('/witches/open_mail/0', param)
        user = WUsers.objects.get(phone_id='55555555')

        avatar_item1 = AvatarItems.objects.filter(name='Baseball Cap')[0]
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]
        mail = UserMailBox.objects.filter(user_id=user.id)

        self.assertEqual(r.status_code, 200, 'open mail failed')
        self.assertEqual(UserMailBox.objects.filter(user_id=user.id, read_flag=False).count(), 0)
        self.assertEqual(user.premium_currency, 20, ' user premium currency should be 20 but got ' + str(user.premium_currency))
        self.assertEqual(user.free_currency, 1000, ' user free_currency should be 1000 but got ' + str(user.free_currency))
        self.assertEqual(user.stamina_potion, 1, ' user stamina_potion should be 1 but got ' + str(user.stamina_potion))
        user_avatar = UserAvatarItemsInCloset.objects.filter(user_id=user.id, avatar_item_id=avatar_item1.id)
        self.assertEqual(user_avatar.count(), 1, ' user avatar should had been recevied so count should be 1 but got ' + str(user_avatar.count()))
        ingredient = UserItemInventory.objects.get(user_id=user.id)
        self.assertEqual(ingredient.ingredient_id, ingredient1.id, ' user ingredient should be ' + ingredient1.id + ' but got ' + ingredient.ingredient_id)
        self.assertFalse(mail[0].premium_received_flag)
        self.assertFalse(mail[0].free_currency_received_flag)
        self.assertFalse(mail[0].stamina_potion_received_flag)

    def test_scene_mail(self):
        scene_id = 'Prologue/Prologue/Divide by Thirteen'
        c = Client()
        param = {'phone_id': '55555555', 'scene_path': scene_id}
        r = c.post('/witches/check_scene_mail/1', param)
        self.assertEqual(r.status_code, 200, 'open mail failed')
        response = json.loads(r.content)
        self.assertTrue(response['scene_mail'])

    def test_check_scene_mail(self):
        scene_id = 'Prologue/Prologue/Divide by Thirteen'
        has_mail = check_if_scene_has_mail(scene_id)
        self.assertTrue(has_mail)
        scene_id = 'Prologue/Prologue/Bewitching Meeting'
        has_mail = check_if_scene_has_mail(scene_id)
        self.assertFalse(has_mail)

    def test_check_scene_mail_exception(self):
        scene_id = 'Prologue/Prologue/Divide by Thirtee'
        try:
            check_if_scene_has_mail(scene_id)
        except NoValueFoundError as e:
            self.assertEqual(str(e), 'Scene ID couldn\'t be found', "Scene ID ''Prologue/Prologue/Divide by Thirtee' was not found")

    def test_check_scene_mail_exception2(self):
        scene_id = 'Prologue/Prologue/Mending Luna'
        try:
            check_if_scene_has_mail(scene_id)
        except NoValueFoundError as e:
            self.assertEqual(str(e), 'More than 2 scene IDs with the same name are found', "Scene ID 'Prologue/Prologue/Mending Luna' was found more than 2")


    def tearDown(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()