import datetime
import dateutil
from witches.utils.util import get_now_datetime

__author__ = 'yoshi.miyamoto'

from pymongo import MongoClient
from witches.models import *
from django.utils import unittest
from django.test.client import Client
from copy import copy
from django.core.cache import cache
import json

class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        now = get_now_datetime()
        # User
        cache.set('user1', WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                                                 email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0, scene_id='unittest_scene',
                                                 phone_id='abcdefgh', closet=30))

        cache.set('user2', WUsers.objects.create(last_name='t_last2', first_name='t_user2', gender='Female', work=[],
                                                 email='t_user2@test.com', birthday='08/20/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0, scene_id='unittest_scene',
                                                 phone_id='12345678', closet=2))

        WUsers.objects.create(last_name='t_last3', first_name='t_user3', gender='Female', work=[], scene_id='unittest_scene',
                              email='t_user3@test.com', birthday='08/20/1999', free_currency=0,
                              premium_currency=0, ticket=2, delete_flag=0,
                              phone_id='a1b2c3d4', closet=3)

        cache.set('user4', WUsers.objects.create(last_name='t_last4', first_name='t_user4', gender='Female', work=[],
                                                 email='t_user4@test.com', birthday='01/2/1996', free_currency=0, scene_id='unittest_scene',
                                                 premium_currency=0, ticket=5, delete_flag=0,
                                                 phone_id='9876qwer', closet=30))

        more_than_two_hours_ago = now-datetime.timedelta(seconds=7250)
        four_hours_ago = now-datetime.timedelta(seconds=14400)
        more_than_eight_hours_ago = now-datetime.timedelta(seconds=28850)
        six_hours_ago = now-datetime.timedelta(seconds=21600)
        twenty_four_hours_ago = now-datetime.timedelta(seconds=86400)
        future_time = now + datetime.timedelta(seconds=1)
        two_and_half_ago = now-datetime.timedelta(seconds=9000)


        WUsers.objects.create(last_name='t_last5', first_name='t_user5', gender='Female', work=[], scene_id='unittest_scene',
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=2, delete_flag=0, stamina_potion=10,
                              phone_id='zaq12wsx', closet=60, 
                              ticket_last_update=more_than_two_hours_ago)

        WUsers.objects.create(last_name='t_last6', first_name='t_user6', gender='Female', work=[], scene_id='unittest_scene',
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=4, delete_flag=0, stamina_potion=10,
                              phone_id='98765432', closet=60, 
                              ticket_last_update=more_than_eight_hours_ago)

        WUsers.objects.create(last_name='t_last7', first_name='t_user7', gender='Female', work=[], scene_id='unittest_scene',
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=1, delete_flag=0, stamina_potion=10,
                              phone_id='qwerasdf', closet=60, 
                              ticket_last_update=twenty_four_hours_ago)

        WUsers.objects.create(last_name='t_last9', first_name='t_user9', gender='Female', work=[], scene_id='unittest_scene',
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=1, delete_flag=0, stamina_potion=10,
                              phone_id='55555555', closet=60, 
                              ticket_last_update=more_than_two_hours_ago)

        WUsers.objects.create(last_name='t_last8', first_name='t_user8', gender='Female', work=[],
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000, stamina_potion=60,
                              premium_currency=20, ticket=5, delete_flag=0,
                              phone_id='zxcvasdf', closet=60, scene_id='Prologue/Prologue/Divide by Thirteen')

        WUsers.objects.create(last_name='t_last10', first_name='t_last10', gender='Female', work=[], scene_id='unittest_scene',
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=2, delete_flag=0, stamina_potion=10,
                              phone_id='11111111', closet=60, 
                              ticket_last_update=four_hours_ago)

        WUsers.objects.create(last_name='t_last11', first_name='t_last11', gender='Female', work=[], scene_id='unittest_scene',
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=2, delete_flag=0, stamina_potion=10,
                              phone_id='22222222', closet=60, 
                              ticket_last_update=future_time)

        WUsers.objects.create(last_name='t_last12', first_name='t_last12', gender='Female', work=[], scene_id='unittest_scene',
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=2, delete_flag=0, stamina_potion=10,
                              phone_id='33333333', closet=60, 
                              ticket_last_update=two_and_half_ago)

        WUsers.objects.create(last_name='t_last13', first_name='t_last13', gender='Female', work=[], scene_id='no_regen_scene',
                              email='t_user5@test.com', birthday='08/20/1979', free_currency=1000,
                              premium_currency=20, ticket=2, delete_flag=0, stamina_potion=10,
                              phone_id='44444444', closet=60, 
                              ticket_last_update=more_than_eight_hours_ago)

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


        avatar_category1 = Categories.objects.filter(name='avatar_category1')[0]

        # AvatarItems
        cache.set('avatar_item1', AvatarItems.objects.create(category_id=avatar_category1.id,
                                                             description=avatar_category1.description,
                                                             name='Baseball Cap', premium_price=1, currency_flag=2,
                                                             slots_layer=0,
                                                             display_order=2))

        ingredient_category = Categories.objects.filter(name='ingredient_category')[0]
        ingredient_category2 = Categories.objects.filter(name='ingredient_category2')[0]
        ingredient_category3 = Categories.objects.filter(name='ingredient_category3')[0]
        ingredient_category4 = Categories.objects.filter(name='ingredient_category4')[0]

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

        avatar_item1 = AvatarItems.objects.filter(name='Baseball Cap')[0]

        # Book Prizes
        BookPrizes.objects.create(name='t_bookprize1', type='avatar', reward_id=avatar_item1.id, quantity=1)
        bookprize1 = BookPrizes.objects.filter(name='t_bookprize1')[0]


        # Books
        Books.objects.create(name='book1', display_order=1, available=True,
                             book_prize_id=bookprize1.id, recipes=[{}])

        book1 = Books.objects.filter(name='book1')[0]

        user1 = WUsers.objects.filter(phone_id='zaq12wsx')[0]
        user2 = WUsers.objects.filter(phone_id='abcdefgh')[0]
        user3 = WUsers.objects.filter(phone_id='98765432')[0]
        user4 = WUsers.objects.filter(phone_id='qwerasdf')[0]
        user5 = WUsers.objects.filter(phone_id='55555555')[0]
        user10 = WUsers.objects.filter(phone_id='11111111')[0]
        user12 = WUsers.objects.filter(phone_id='33333333')[0]

        UserBooks.objects.create(user_id=user1.id, book_list=[book1.id])
        UserBooks.objects.create(user_id=user2.id, book_list=[book1.id])
        UserBooks.objects.create(user_id=user3.id, book_list=[book1.id])
        UserBooks.objects.create(user_id=user4.id, book_list=[book1.id])
        UserBooks.objects.create(user_id=user5.id, book_list=[book1.id])
        UserBooks.objects.create(user_id=user10.id, book_list=[book1.id])
        UserBooks.objects.create(user_id=user12.id, book_list=[book1.id])

        affinities_dict = {"A": 0, "M": 0, "N": 0, "R": 0, "T": 0}

        UserCharacters.objects.create(user_id=user1.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user2.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user3.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user4.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user5.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user10.id, affinities=affinities_dict)
        UserCharacters.objects.create(user_id=user12.id, affinities=affinities_dict)

        # item exchange rate
        ItemExchangeRate.objects.create(ticket_quantity=1, max=5, ticket=0, ticket_price=1, exchange_type=1)
        ItemExchangeRate.objects.create(ticket_quantity=1, max=5, ticket=1, ticket_price=1, exchange_type=2)
        ItemExchangeRate.objects.create(ticket_quantity=5, max=0, ticket=2, ticket_price=1, exchange_type=2)

        # Scene Table
        SceneTable.objects.create(scene_path='unittest_scene', regeneration_flag=True)
        SceneTable.objects.create(scene_path='no_regen_scene', regeneration_flag=False)

    def test_sync_resources_two_hours_passed(self):
        c = Client()
        param = {'phone_id': 'zaq12wsx', 'stamina': 4, 'stamina_potions': 8}
        r = c.post('/witches/sync_resources/1', param)
        dic = json.loads(r.content)
        stamina_count = dic['stamina']
        stamina_potion_count = dic['stamina_potion']
        self.assertEqual(stamina_count, 4, 'stamina should be 4 but got ' + str(stamina_count))
        self.assertEqual(stamina_potion_count, 8, 'stamina_potion should be 8 but got ' + str(stamina_potion_count))

    def test_sync_resources_two_hours_passed_wrong_phone_id(self):
        c = Client()
        param = {'phone_id': '55555552', 'stamina': 0,'stamina_potions': 4}
        r = c.post('/witches/sync_resources/1', param)
        dic = json.loads(r.content)
        status = dic['status']
        self.assertEqual(status, 'failed', 'status should be failed but got ' + str(status))

    def test_sync_resources_eight_hours_passed(self):
        c = Client()
        param = {'phone_id': '98765432', 'stamina': 4, 'stamina_potions': 8}
        r = c.post('/witches/sync_resources/1', param)
        dic = json.loads(r.content)
        stamina_count = dic['stamina']
        stamina_potion_count = dic['stamina_potion']
        self.assertEqual(stamina_count, 5, 'stamina should be 5 but got ' + str(stamina_count))
        self.assertEqual(stamina_potion_count, 8, 'stamina_potion should be 8 but got ' + str(stamina_potion_count))

    def test_sync_resources_two_hours_passed_wrong_count(self):
        c = Client()  # user with free_currency=1000, premium_currency=20, ticket=1, focus=0,stamina_potion=10,closet=60
        param = {'phone_id': '55555555', 'stamina': 4, 'stamina_potions': 10}
        r = c.post('/witches/sync_resources/1', param)
        dic = json.loads(r.content)
        status = dic['status']
        stamina = dic['stamina']
        self.assertEqual(status, 'success', 'status should be failed but got ' + str(status))
        self.assertEqual(stamina, 4, 'stamina should be 4 but got ' + str(stamina))



    def test_sync_resources_two_hours_passed_stamina_less_than_potion_used(self):
        c = Client()
        param = {'phone_id': '55555555', 'stamina': 0, 'stamina_potions': 9}
        r = c.post('/witches/sync_resources/1', param)
        dic = json.loads(r.content)
        stamina_count = dic['stamina']
        stamina_potion_count = dic['stamina_potion']
        self.assertEqual(stamina_count, 0, 'stamina should be 0 but got ' + str(stamina_count))
        self.assertEqual(stamina_potion_count, 9, 'status should be 9 but got ' + str(stamina_potion_count))

    def test_update_stamina_no_regeneration(self):
        c = Client()
        param = {'phone_id': '44444444'}
        user_updated_eight_hours_ago = WUsers.objects.get(phone_id='44444444')
        user_updated_eight_hours_ago_copy = copy(user_updated_eight_hours_ago.ticket_last_update)
        c.post('/witches/update_stamina/1', param)
        user = WUsers.objects.get(phone_id='44444444')

        self.assertEqual(user.ticket, 2, 'ticket should be 2 but got ' + str(user.ticket))
        self.assertEqual(user.ticket_last_update, user_updated_eight_hours_ago.ticket_last_update, 'ticket update time shouldn\'t be changed ' +
                         ' from original last update: ' + str(user_updated_eight_hours_ago_copy) +
                         ' but got ' + str(user.ticket_last_update))





    def test_update_stamina_2_hours_6hours_under_max(self):
        c = Client()
        param = {'phone_id': 'zaq12wsx'}
        user_updated_two_hours_ago = WUsers.objects.get(phone_id='zaq12wsx')
        user_updated_two_hours_ago_copy = copy(user_updated_two_hours_ago.ticket_last_update)
        c.post('/witches/update_stamina/1', param)
        user = WUsers.objects.get(phone_id='zaq12wsx')

        self.assertEqual(user.ticket, 2, 'ticket should be 2 and not be updated but got ' + str(user.ticket))
        self.assertEqual(user.ticket_last_update, user_updated_two_hours_ago.ticket_last_update,
                         'ticket update time shouldn\'t be changed but got ' + str(user.ticket_last_update)
                         + ' original last update:' + str(user_updated_two_hours_ago_copy))

        user.ticket_last_update -= datetime.timedelta(seconds=14400)
        user.save()
        user_updated_six_hours_ago_copy = copy(user.ticket_last_update)

        c.post('/witches/update_stamina/1', param)

        user_after_six_hours = WUsers.objects.get(phone_id='zaq12wsx')

        self.assertEqual(user_after_six_hours.ticket, 3, 'ticket should be updated to 3 but got ' + str(user.ticket))
        self.assertEqual(user_after_six_hours.ticket_last_update, user.ticket_last_update +
                                                                              datetime.timedelta(seconds=14400),
                         'ticket update time should be 4 hours later: ' + str(user.ticket_last_update +
                                                                              datetime.timedelta(seconds=14400)) +
                         ' from original: ' + str(user_updated_six_hours_ago_copy) + ' but got ' +
                         str(user_after_six_hours.ticket_last_update))

    def test_update_stamina_two_more_than_max_within_max_hours(self):
        c = Client()
        param = {'phone_id': '98765432'}
        user_updated_eight_hours_ago = WUsers.objects.get(phone_id='98765432')
        user_updated_eight_hours_ago_copy = copy(user_updated_eight_hours_ago.ticket_last_update)
        c.post('/witches/update_stamina/1', param)
        user = WUsers.objects.get(phone_id='98765432')

        self.assertEqual(user.ticket, 5, 'ticket should be 5 but got ' + str(user.ticket))
        self.assertEqual(user.ticket_last_update, user_updated_eight_hours_ago.ticket_last_update +
                         datetime.timedelta(seconds=28800), 'ticket update time should be 8 hours later: ' +
                         str(user_updated_eight_hours_ago.ticket_last_update + datetime.timedelta(seconds=28800)) +
                         ' from original last update: ' + str(user_updated_eight_hours_ago_copy) +
                         ' but got ' + str(user.ticket_last_update))


    def test_update_stamina_after_max_hours_add_four(self):
        c = Client()
        param = {'phone_id': 'qwerasdf'}
        user_updated_twentyfour_hours_ago = WUsers.objects.get(phone_id='qwerasdf')
        user_updated_twentyfour_hours_ago_copy = copy(user_updated_twentyfour_hours_ago.ticket_last_update)
        c.post('/witches/update_stamina/1', param)
        user = WUsers.objects.get(phone_id='qwerasdf')

        self.assertEqual(user.ticket, 5, 'ticket should be 5 but got ' + str(user.ticket))
        self.assertEqual(user.ticket_last_update, user_updated_twentyfour_hours_ago.ticket_last_update +
                         datetime.timedelta(seconds=86400), 'ticket update time should be 24 hours later: ' +
                         str(user_updated_twentyfour_hours_ago.ticket_last_update + datetime.timedelta(seconds=86400)) +
                         ' from original last update: ' + str(user_updated_twentyfour_hours_ago_copy) +
                         ' but got ' + str(user.ticket_last_update))

    def test_update_ticket_four_hours_later(self):
        c = Client()
        param = {'phone_id': '11111111'}
        user_updated_four_hours_ago = WUsers.objects.get(phone_id='11111111')
        user_updated_four_hours_ago_copy = copy(user_updated_four_hours_ago.ticket_last_update)
        c.post('/witches/update_stamina/1', param)
        user = WUsers.objects.get(phone_id='11111111')

        self.assertEqual(user.ticket, 3, 'ticket should be 3 but got ' + str(user.ticket))
        self.assertEqual(user.ticket_last_update, user_updated_four_hours_ago_copy +
                         datetime.timedelta(seconds=14400), 'ticket update time should be 4 hours later: ' +
                         str(user_updated_four_hours_ago_copy + datetime.timedelta(seconds=14400)) +
                         ' from original last update: ' + str(user_updated_four_hours_ago_copy) +
                         ' but got ' + str(user.ticket_last_update))


    def test_update_stamina_with_future_time(self):
        c = Client()
        param = {'phone_id': '22222222'}
        user_future_time = WUsers.objects.get(phone_id='22222222')
        user_future_time_copy = copy(user_future_time.ticket_last_update)
        c.post('/witches/update_stamina/1', param)
        user = WUsers.objects.get(phone_id='22222222')

        self.assertEqual(user.ticket, 2, 'ticket should be 2 but got ' + str(user.ticket))
        self.assertEqual(user.ticket_last_update, user_future_time_copy, 'ticket update time should be: ' +
                         str(user_future_time_copy) + ' but got ' + str(user.ticket_last_update))

    def test_update_stamina_gifts(self):
        c = Client()
        param = {'phone_id': '44444444'}
        c.post('/witches/refill_stamina/1', param)
        user = WUsers.objects.get(phone_id='44444444')

        self.assertEqual(user.ticket, 5, 'ticket should be 5 but got ' + str(user.ticket))


    def tearDown(self):
            client = MongoClient('localhost', 27017)
            client.drop_database(name_or_database='UnitTest')


if __name__ == '__main__':
    unittest.main()