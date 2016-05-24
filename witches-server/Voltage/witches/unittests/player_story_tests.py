import datetime
import json
from witches.utils.util import get_now_datetime
from django.utils import unittest
from pymongo import MongoClient
from django.test.client import Client
from witches.models import ShopItems, WUsers, UserMailBox, EmailTemplates, Characters, UserCharacters, SceneTable, \
    AvatarItems, Categories, GameProperties, ItemExchangeRate, UserBooks, Potions, BookPrizes, Recipes, Books, \
    Ingredients, UserCompletedScenes
from witches.unittests import const
from django.core.cache import cache
from copy import copy

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
const.product_id_stamina_potion_60 = 'com.voltage.ent.witch.104'


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        now = get_now_datetime()

        two_and_half_ago = now-datetime.timedelta(seconds=9000)
        more_than_eight_hours_ago = now-datetime.timedelta(seconds=28850)

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
        Categories.objects.create(name='avatar_category7', description='INTIMATES', type=1, color=00005)
        Categories.objects.create(name='avatar_category8', description='SHOES', type=1, color=00005)
        avatar_category1 = Categories.objects.filter(name='avatar_category1')[0]
        avatar_category2 = Categories.objects.filter(name='avatar_category2')[0]
        avatar_category7 = Categories.objects.filter(name='avatar_category7')[0]
        avatar_category8 = Categories.objects.filter(name='avatar_category8')[0]

        ingredient_category = Categories.objects.filter(name='ingredient_category')[0]
        ingredient_category2 = Categories.objects.filter(name='ingredient_category2')[0]
        ingredient_category3 = Categories.objects.filter(name='ingredient_category3')[0]
        ingredient_category4 = Categories.objects.filter(name='ingredient_category4')[0]

        # Ingredient
        Ingredients.objects.create(name='t_ingredient1', description=ingredient_category.description,
                                   category_id=ingredient_category.id, display_order=1, quality=1, isInfinite=False,
                                   coins_price=10, currency_flag=1)
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]

        # User
        cache.set('user1', WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                                                 email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='abcdefgh', closet=30))

        WUsers.objects.create(last_name='t_last3', first_name='t_user3', gender='Female', work=[],
                              email='t_user3@test.com', birthday='08/20/1999', free_currency=0,
                              premium_currency=0, ticket=2, delete_flag=0,
                              phone_id='a1b2c3d4', closet=3)

        WUsers.objects.create(last_name='t_last13', first_name='t_last13', gender='Female', work=[], scene_id='no_regen_scene',
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=2, delete_flag=0, stamina_potion=10,
                              phone_id='44444444', closet=60, 
                              ticket_last_update=more_than_eight_hours_ago)


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

        affinities_dict = {"A": 0, "M": 0, "N": 0, "R": 0, "T": 0}
        user1 = WUsers.objects.filter(phone_id='abcdefgh')[0]
        user3 = WUsers.objects.filter(phone_id='a1b2c3d4')[0]
        user4 = WUsers.objects.filter(phone_id='44444444')[0]

        UserCharacters.objects.create(user_id=user1.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user3.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user4.id, affinities=affinities_dict)

        UserBooks.objects.create(user_id=user1.id, book_list=[book1.id, book2.id])

        # Characters
        Characters.objects.create(first_name='Anastasia', last_name='Petrova', initial='A', romanceable=1)
        anastasia = Characters.objects.filter(first_name='Anastasia')[0]

        # mail
        mail_attachment = [{'id': avatar_item7.id, 'received_flag': False}, {'id': avatar_item8.id,
                                                                             'received_flag': False}]
        EmailTemplates.objects.create(premium_currency=1, sender_id=anastasia.id, free_currency=100,
                                      body_text='unittest', attach_list=mail_attachment, stamina_potion=5)
        mail = EmailTemplates.objects.get(body_text='unittest')

        # shop items
        ShopItems.objects.create(name='Stamina Potion Hoard', item_index=9, product_id='com.voltage.ent.witch.104',
                                 price=49.99, premium_qty=60)

        SceneTable.objects.create(scene_path='yes_deduct_yes_regen', mail_template_id=mail.id,
                                  regeneration_flag=True, stamina_deduction_flag=True)
        SceneTable.objects.create(scene_path='Prologue/Prologue/Divide by Thirteen', mail_template_id=mail.id,
                                  regeneration_flag=False, stamina_deduction_flag=True)
        SceneTable.objects.create(scene_path='Prologue/Prologue/Slow Day Swiftly Interrupted', mail_template_id=mail.id,
                                  regeneration_flag=False, stamina_deduction_flag=False)

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

        # price_type 0 = stamina potion, stone = 1
        # max = 0 is unlimited
        ItemExchangeRate.objects.create(ticket=const.stamina_ticket, ticket_quantity=1, ticket_price=1, max=5,
                                        exchange_type=1)  # stamina
        ItemExchangeRate.objects.create(ticket=const.closet_ticket, ticket_quantity=5, ticket_price=1, max=0,
                                        exchange_type=2)  # closet

    def test_start_scene(self):
        c = Client()
        param = {'phone_id': 'a1b2c3d4', 'scene_path': 'Prologue/Prologue/Divide by Thirteen'}
        r = c.post('/witches/start_scene/1', param)
        disc = json.loads(r.content)
        self.assertEqual(disc['status'], 'success', 'status should be success but got ' + disc['status'])
        user = WUsers.objects.get(phone_id='a1b2c3d4')
        self.assertEqual(user.scene_id, 'Prologue/Prologue/Divide by Thirteen', ' user scene id should be Prologue/Prologue/Divide by Thirteen but got ' + user.scene_id)

    def test_story_reset(self):
        c = Client()
        ios_receipt = const.ios_receipt
        param = {'phone_id': 'a1b2c3d4', 'premium_id': const.product_id_stamina_potion_60, 'receipt': ios_receipt, 'device_os': 'ios'}
        r = c.post('/witches/premium/buy_inapp')
        self.assertEqual(r.status_code, 200, 'buy stones html failed')
        r2 = c.post('/witches/buy_inapp/0', param)
        user = WUsers.objects.filter(phone_id='a1b2c3d4')[0]
        self.assertEqual(r2.status_code, 200, 'Accessing buy_inapp failed')
        self.assertEqual(user.stamina_potion, 60, 'total of premium currency should be 60 but got ' + str(user.stamina_potion))
        self.assertEqual(user.free_currency, 0, 'free currency should be 0 but got ' + str(user.free_currency))
        self.assertEqual(user.ticket, 2, 'user ticket should be 2 but got ' + str(user.ticket))

        affinities = '{"A": 10, "B": 10}'
        choices = '{"Prologue/Prologue/Divide by Thirteen": "A"}'
        param = {'phone_id': 'a1b2c3d4', 'affinities': affinities, 'stamina_potions': 58,
                 'scene_id': 'Prologue/Prologue/Divide by Thirteen', 'node_id': 'node1',
                 'choices': choices}

        c.post('/witches/update_playerstorystate/0', param)

        affinities = '{"A": 10, "B": 40}'
        choices = '{"Prologue/Prologue/Divide by Thirteen": "A"}'
        param = {'phone_id': 'a1b2c3d4', 'affinities': affinities, 'stamina_potions': 48,
                 'choices': choices}
        c.post('/witches/complete_scene/1', param)

        updated_user = WUsers.objects.filter(phone_id='a1b2c3d4')[0]
        characters = UserCharacters.objects.filter(user_id=user.id, delete_flag=False)

        self.assertEqual(updated_user.total_affinity, 50, 'total affinity should be 50 but got ' + str(updated_user.total_affinity))
        self.assertEqual(updated_user.stamina_potion, 48, 'stamina potion should be 48 but got ' + str(updated_user.stamina_potion))
        self.assertEqual(characters[0].affinities["A"], 10, 'A character affinity should be 10 but got ' +
                         str(characters[0].affinities["A"]))
        self.assertEqual(updated_user.ticket, 5, 'user ticket should be 5 but got ' + str(updated_user.ticket))

        param = {'phone_id': 'a1b2c3d4'}
        c.post('/witches/story_reset/1', param)
        user = WUsers.objects.filter(phone_id='a1b2c3d4')[0]
        completed_scenes = UserCompletedScenes.objects.filter(user_id=user.id, delete_flag=False)
        characters = UserCharacters.objects.filter(user_id=user.id, delete_flag=False)

        self.assertEqual(completed_scenes.__len__(), 0, 'should be no completed scene but got '+ str(completed_scenes.__len__()))
        self.assertEqual(characters[0].affinities["A"], 0, 'A character affinity should be 0 but got ' +
                         str(characters[0].affinities["A"]))
        self.assertEqual(user.total_affinity, 50, 'total affinity should be 50 but got ' + str(user.total_affinity))

    def test_complete_scene(self):
        c = Client()
        ios_receipt = const.ios_receipt
        param = {'phone_id': 'a1b2c3d4', 'premium_id': const.product_id_stamina_potion_60, 'receipt': ios_receipt, 'device_os': 'ios'}
        r = c.post('/witches/premium/buy_inapp')
        self.assertEqual(r.status_code, 200, 'buy stones html failed')
        r2 = c.post('/witches/buy_inapp/0', param)
        user = WUsers.objects.filter(phone_id='a1b2c3d4')[0]
        self.assertEqual(r2.status_code, 200, 'Accessing buy_inapp failed')
        self.assertEqual(user.stamina_potion, 60, 'total of premium currency should be 60 but got ' + str(user.stamina_potion))
        self.assertEqual(user.free_currency, 0, 'free currency should be  but got ' + str(user.free_currency))

        affinities = '{"A": 10, "B": 10}'
        choices = '{"Prologue/Prologue/Divide by Thirteen": "A"}'
        param = {'phone_id': 'a1b2c3d4', 'affinities': affinities, 'stamina_potions': 58,
                 'scene_id': 'Prologue/Prologue/Divide by Thirteen', 'node_id': 'node1',
                 'choices': choices}

        c.post('/witches/update_playerstorystate/0', param)

        affinities = '{"A": 10, "B": 40}'
        choices = '{"Prologue/Prologue/Divide by Thirteen": "A"}'
        param = {'phone_id': 'a1b2c3d4', 'affinities': affinities, 'stamina_potions': 48,
                 'choices': choices}
        c.post('/witches/complete_scene/1', param)

        updated_user = WUsers.objects.filter(phone_id='a1b2c3d4')[0]

        self.assertEqual(updated_user.total_affinity, 50, 'total affinity should be 50 but got ' + str(updated_user.total_affinity))
        self.assertEqual(updated_user.stamina_potion, 48, 'stamina potion should be 48 but got ' + str(updated_user.stamina_potion))

        usermail = UserMailBox.objects.filter(user_id=updated_user.id)
        mail = EmailTemplates.objects.get(body_text='unittest')
        anastasia = Characters.objects.get(first_name='Anastasia')
        self.assertEqual(usermail.count(), 1, 'user has one mail but got ' + str(usermail.count()))
        self.assertEqual(usermail[0].message_body, mail.body_text, 'message body should be unittest  but got ' + usermail[0].message_body)
        self.assertEqual(usermail[0].sender_id, anastasia.id, 'sender should be: ' + anastasia.id + ' but got ' + usermail[0].sender_id)

    def test_updateplayerstorystate_less_stamina(self):
        c = Client()
        ios_receipt = const.ios_receipt
        param = {'phone_id': 'a1b2c3d4', 'premium_id': const.product_id_stamina_potion_60, 'receipt': ios_receipt, 'device_os': 'ios'}
        r = c.post('/witches/premium/buy_inapp')
        self.assertEqual(r.status_code, 200, 'buy stones html failed')
        r2 = c.post('/witches/buy_inapp/0', param)

        user = WUsers.objects.filter(phone_id='a1b2c3d4')[0]
        self.assertEqual(r2.status_code, 200, 'Accessing buy_inapp failed')
        self.assertEqual(user.stamina_potion, 60, 'total of premium currency should be 60 but got ' + str(user.stamina_potion))
        self.assertEqual(user.free_currency, 0)

        affinities = '{"A": 10, "B": 10}'
        choices = '{"/Prologue/Prologue/Mending Luna": "A"}'
        param = {'phone_id': 'a1b2c3d4', 'affinities': affinities, 'stamina_potions': 58,
                 'scene_id': 'Prologue/Prologue/Slow Day Swiftly Interrupted', 'node_id': 'node1',
                 'choices': choices}

        r2 = c.post('/witches/update_playerstorystate/0', param)
        self.assertEqual(r2.status_code, 200, 'buy stamina failed')

        user = WUsers.objects.get(phone_id='a1b2c3d4')
        self.assertEqual(user.stamina_potion, 58, 'total of premium currency should be 58 but got ' + str(user.stamina_potion))
        self.assertEqual(user.ticket, 4, 'total of stamina should be 4 but got ' + str(user.ticket))
        self.assertEqual(user.total_affinity, 20, 'total of affinity should be 20 but got ' + str(user.total_affinity))

    def test_updateplayerstorystate(self):
        c = Client()
        ios_receipt = const.ios_receipt
        param = {'phone_id': 'abcdefgh', 'premium_id': const.product_id_stamina_potion_60, 'receipt': ios_receipt, 'device_os': 'ios'}
        r = c.post('/witches/premium/buy_inapp')
        self.assertEqual(r.status_code, 200, 'buy stamina potions html failed')
        r2 = c.post('/witches/buy_inapp/0', param)

        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        self.assertEqual(r2.status_code, 200, 'Accessing buy_inapp failed')
        self.assertEqual(user.stamina_potion, 60, 'total of premium currency should be 60 but got ' + str(user.stamina_potion))
        self.assertEqual(user.free_currency, 1000)

        affinities = '{"A": 30, "B": 10}'
        choices = '{"/Prologue/Prologue/Slow Day Swiftly Interrupted": "A"}'

        param = {'phone_id': 'abcdefgh', 'affinities': affinities, 'stamina_potions': 60,
                 'scene_id': 'Prologue/Prologue/Slow Day Swiftly Interrupted', 'node_id': 'node1',
                 'choices': choices}

        r = c.post('/witches/update_playerstorystate/0', param)
        self.assertEqual(r.status_code, 200, 'buy stamina failed')

        user = WUsers.objects.get(phone_id='abcdefgh')
        self.assertEqual(user.stamina_potion, 60, 'total of premium currency should be 60 but got ' + str(user.stamina_potion))
        self.assertEqual(user.ticket, 5, 'total of stamina should be 5 but got ' + str(user.ticket))
        self.assertEqual(user.total_affinity, 40, 'total of affinity should be 40 but got ' + str(user.total_affinity))

        affinities = '{"A": 10, "B": 10}'
        choices = '{"/Prologue/Prologue/Mending Luna": "A"}'
        param = {'phone_id': 'abcdefgh', 'affinities': affinities, 'stamina_potions': 59,
                 'scene_id': 'Prologue/Prologue/Slow Day Swiftly Interrupted', 'node_id': 'node1',
                 'choices': choices}

        r2 = c.post('/witches/update_playerstorystate/0', param)
        self.assertEqual(r2.status_code, 200, 'buy stamina failed')

        user = WUsers.objects.get(phone_id='abcdefgh')
        self.assertEqual(user.stamina_potion, 59, 'total of premium currency should be 59 but got ' + str(user.stamina_potion))
        self.assertEqual(user.ticket, 5, 'total of stamina should be 5 but got ' + str(user.ticket))
        self.assertEqual(user.total_affinity, 20, 'total of affinity should be 20 but got ' + str(user.total_affinity))

    def test_use_stamina_no_regeneration_no_deduction(self):
        c = Client()
        ios_receipt = const.ios_receipt
        user_updated_eight_hours_ago = WUsers.objects.get(phone_id='44444444')
        user_updated_eight_hours_ago_copy = copy(user_updated_eight_hours_ago.ticket_last_update)

        param = {'phone_id': '44444444', 'premium_id': const.product_id_stamina_potion_60, 'receipt': ios_receipt, 'device_os': 'ios'}
        r = c.post('/witches/premium/buy_inapp')
        self.assertEqual(r.status_code, 200, 'buy stamina potions html failed')
        r2 = c.post('/witches/buy_inapp/0', param)

        user = WUsers.objects.filter(phone_id='44444444')[0]
        self.assertEqual(r2.status_code, 200, 'Accessing buy_inapp failed')
        self.assertEqual(user.stamina_potion, 70, 'total of premium currency should be 70 but got ' + str(user.stamina_potion))

        affinities = '{"A": 10, "B": 10}'
        choices = '{"/Prologue/Prologue/Mending Luna": "A"}'
        param = {'phone_id': '44444444', 'affinities': affinities, 'stamina_potions': 70,
                 'scene_id': 'Prologue/Prologue/Slow Day Swiftly Interrupted', 'node_id': 'node1',
                 'choices': choices}

        r2 = c.post('/witches/update_playerstorystate/0', param)
        self.assertEqual(r2.status_code, 200, 'buy stamina failed')

        user = WUsers.objects.get(phone_id='44444444')
        self.assertEqual(user.stamina_potion, 70, 'total of stamina potion should be 70 but got ' + str(user.stamina_potion))
        self.assertEqual(user.ticket, 2, 'total of stamina should be 2 but got ' + str(user.ticket))
        self.assertEqual(user.ticket_last_update, user_updated_eight_hours_ago.ticket_last_update, 'ticket update time shouldn\'t be changed ' +
                         ' from original last update: ' + str(user_updated_eight_hours_ago_copy) +
                         ' but got ' + str(user.ticket_last_update))

    def test_use_stamina_no_regeneration_yes_deduction(self):
        c = Client()
        ios_receipt = const.ios_receipt
        param = {'phone_id': 'abcdefgh', 'premium_id': const.product_id_stamina_potion_60, 'receipt': ios_receipt, 'device_os': 'ios'}
        r = c.post('/witches/premium/buy_inapp')
        self.assertEqual(r.status_code, 200, 'buy stamina potions html failed')
        r2 = c.post('/witches/buy_inapp/0', param)

        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        self.assertEqual(r2.status_code, 200, 'Accessing buy_inapp failed')
        self.assertEqual(user.stamina_potion, 60, 'total of premium currency should be 60 but got ' + str(user.stamina_potion))
        self.assertEqual(user.free_currency, 1000)

        affinities = '{"A": 30, "B": 10}'
        choices = '{"Prologue/Prologue/Divide by Thirteen": "A"}'

        param = {'phone_id': 'abcdefgh', 'affinities': affinities, 'stamina_potions': 60,
                 'scene_id': 'Prologue/Prologue/Divide by Thirteen', 'node_id': 'node1',
                 'choices': choices}

        c.post('/witches/update_playerstorystate/0', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        self.assertEqual(user.stamina_potion, 60, 'total of premium currency should be 60 but got ' + str(user.stamina_potion))
        self.assertEqual(user.ticket, 4, 'total of stamina should be 4 but got ' + str(user.ticket))

        affinities = '{"A": 10, "B": 10}'
        choices = '{"/Prologue/Prologue/Mending Luna": "A"}'
        param = {'phone_id': 'abcdefgh', 'affinities': affinities, 'stamina_potions': 59,
                 'scene_id': 'Prologue/Prologue/Slow Day Swiftly Interrupted', 'node_id': 'node1',
                 'choices': choices}

        r2 = c.post('/witches/update_playerstorystate/0', param)
        self.assertEqual(r2.status_code, 200, 'buy stamina failed')

        user = WUsers.objects.get(phone_id='abcdefgh')
        self.assertEqual(user.stamina_potion, 59, 'total of premium currency should be 59 but got ' + str(user.stamina_potion))
        self.assertEqual(user.ticket, 5, 'total of stamina should be 5 but got ' + str(user.ticket))


    def test_use_stamina_yes_regeneration_yes_deduction(self):
            c = Client()
            ios_receipt = const.ios_receipt
            param = {'phone_id': '44444444', 'premium_id': const.product_id_stamina_potion_60, 'receipt': ios_receipt, 'device_os': 'ios'}
            r = c.post('/witches/premium/buy_inapp')
            self.assertEqual(r.status_code, 200, 'buy stamina potions html failed')
            r2 = c.post('/witches/buy_inapp/0', param)

            user = WUsers.objects.filter(phone_id='44444444')[0]
            self.assertEqual(r2.status_code, 200, 'Accessing buy_inapp failed')
            self.assertEqual(user.stamina_potion, 70, 'total of premium currency should be 70 but got ' + str(user.stamina_potion))
            self.assertEqual(user.free_currency, 1000)

            affinities = '{"A": 10, "B": 10}'
            choices = '{"/Prologue/Prologue/Mending Luna": "A"}'
            param = {'phone_id': '44444444', 'affinities': affinities, 'stamina_potions': 70,
                     'scene_id': 'yes_deduct_yes_regen', 'node_id': 'node1',
                     'choices': choices}

            r2 = c.post('/witches/update_playerstorystate/0', param)
            self.assertEqual(r2.status_code, 200, 'buy stamina failed')

            user = WUsers.objects.get(phone_id='44444444')
            self.assertEqual(user.stamina_potion, 70, 'total of premium currency should be 70 but got ' + str(user.stamina_potion))
            self.assertEqual(user.ticket, 3, 'total of stamina should be 3 but got ' + str(user.ticket))


    def test_error(self):
        c = Client()
        affinities = '{"A": 10, "B": 10}'
        choices = '{"/Prologue/Prologue/Mending Luna": "A"}'
        param = {'phone_id': 'a1b2c3d4', 'affinities': affinities, 'stamina_potions': 58,
                 'scene_id': '/Prologue/Prologue/Slow Day Swiftly Interrupted', 'node_id': 'node1',
                 'choices': choices}

        r2 = c.post('/witches/update_playerstorystate/1', param)
        self.assertTrue("failed" in r2.content, " didn't fail:" + str(r2.content))

    def tearDown(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()
