from django.test import Client
from pymongo import MongoClient
from witches import const
from witches.login import has_time_elapsed_for_next_bonus, update_bonus_items, create_login_bonus_list, \
    update_next_login_bonus_index_and_date, give_to_user_inventory, handle_inventory_items, give_user_bonus_item, \
    get_bonus_index_list

__author__ = 'yoshi.miyamoto'

from witches.models import WUsers, GameProperties, LogInBonusesMaster, Ingredients, Categories, Books, \
    UserBooks, UserCharacters, UserItemInventory, Potions
from django.utils import unittest
from django.core.cache import cache
from witches.utils.util import get_now_datetime
import datetime

now = get_now_datetime()

class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        more_than_eight_hours_ago = now-datetime.timedelta(seconds=28850)
        four_hours_ago = now-datetime.timedelta(seconds=14400)


        GameProperties.objects.create(name='login_bonus_interval', value=480)

        # Category
        Categories.objects.create(name='ingredient_category', description='Silver', type=0,
                                  color=000010)
        Categories.objects.create(name='ingredient_category2', description='Moonstone', type=0,
                                  color=000010)
        Categories.objects.create(name='avatar_category1', description='ACCESSORIES', type=1, color=00005)

        ingredient_category = Categories.objects.filter(name='ingredient_category')[0]
        ingredient_category2 = Categories.objects.filter(name='ingredient_category2')[0]

        # Ingredient
        Ingredients.objects.create(name='t_ingredient1', description=ingredient_category.description,
                                   category_id=ingredient_category.id, display_order=1, quality=1, isInfinite=False,
                                   coins_price=10, currency_flag=1)
        Ingredients.objects.create(name='t_ingredient2', description=ingredient_category2.description,
                                   category_id=ingredient_category2.id, display_order=4, quality=1, isInfinite=False,
                                   premium_price=5, currency_flag=3)

        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]
        ingredient2 = Ingredients.objects.filter(name='t_ingredient2')[0]

        # Potions
        Potions.objects.create(name='t_potion1', description='test potion 1', type=1, color='yellow',
                               effect_list=[{'character_id': 1, 'effect_id': 1},
                                            {'character_id': 4, 'effect_id': 2}])

        potion_item1 = Potions.objects.filter(name='t_potion1')[0]

        # Books
        Books.objects.create(name='book1', display_order=1, available=True)
        book1 = Books.objects.filter(name='book1')[0]

        WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                              email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                              premium_currency=20, ticket=5, delete_flag=0, stamina_potion=25,
                              phone_id='abcdefgh', closet=30, login_bonus_items=[{'id': potion_item1.id, 'qty': 1},
                                                                           {'id': 'stamina_potion', 'qty': 5},
                                                                           {'id': 'coin', 'qty': 100},
                                                                           {'id': 'starstone', 'qty': 32}],
                              next_login_bonus_index=1, last_login_bonus_date=more_than_eight_hours_ago)

        WUsers.objects.create(last_name='t_last2', first_name='t_user2', gender='Male', work=[],
                              email='t_user2@test.com', birthday='08/21/1999', free_currency=1000,
                              premium_currency=20, ticket=5, delete_flag=0,
                              phone_id='12345678', closet=30, login_bonus_items=[],
                              next_login_bonus_index=0)

        WUsers.objects.create(last_name='t_last3', first_name='t_user3', gender='Male', work=[],
                              email='t_user3@test.com', birthday='08/21/1999', free_currency=1000,
                              premium_currency=20, ticket=5, delete_flag=0,
                              phone_id='9876543', closet=30)

        WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                              email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                              premium_currency=20, ticket=5, delete_flag=0,
                              phone_id='11111111', closet=30, login_bonus_items=[{'id': ingredient2.id, 'qty': 2},
                                                                                {'id': potion_item1.id, 'qty': 1},
                                                                           {'id': 'stamina_potion', 'qty': 5},
                                                                           {'id': 'coin', 'qty': 100}],
                              next_login_bonus_index=1, last_login_bonus_date=more_than_eight_hours_ago)

        WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                              email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                              premium_currency=20, ticket=5, delete_flag=0, stamina_potion=25,
                              phone_id='22222222', closet=30, login_bonus_items=[{'id': potion_item1.id, 'qty': 1},
                                                                           {'id': 'stamina_potion', 'qty': 5},
                                                                           {'id': 'coin', 'qty': 100},
                                                                           {'id': 'starstone', 'qty': 32}],
                              next_login_bonus_index=1, last_login_bonus_date=four_hours_ago)

        affinities_dict = {"A": 0, "M": 0, "N": 0, "R": 0, "T": 0}
        user3 = WUsers.objects.filter(phone_id='9876543')[0]

        UserCharacters.objects.create(user_id=user3.id, affinities=affinities_dict)

        user3 = WUsers.objects.filter(phone_id='9876543')[0]
        UserBooks.objects.create(user_id=user3.id, book_list=[book1.id])

        LogInBonusesMaster.objects.create(bonus_index=0, bonus_id='stamina_potion', quantity=5,
                                          bonus_description='stamina potion bonus item')
        LogInBonusesMaster.objects.create(bonus_index=1, bonus_id='coin', quantity=100,
                                          bonus_description='coin bonus item')
        LogInBonusesMaster.objects.create(bonus_index=2, bonus_id='starstone', quantity=32,
                                          bonus_description='starstone bonus item')
        LogInBonusesMaster.objects.create(bonus_index=3, bonus_id=ingredient1.id, quantity=3,
                                          bonus_description='Silver(ingredient) bonus item')
        LogInBonusesMaster.objects.create(bonus_index=4, bonus_id=ingredient2.id, quantity=2,
                                          bonus_description='Moonstone(ingredient) bonus item')
        LogInBonusesMaster.objects.create(bonus_index=5, bonus_id=potion_item1.id, quantity=1,
                                          bonus_description='test potion 1 bonus item')

    def test_login_bonus_eligibility__true(self):
        cache.clear()
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        is_eligible = has_time_elapsed_for_next_bonus(user.phone_id, user.last_login_bonus_date, now)
        self.assertTrue(is_eligible)

    def test_get_bonus_index_list__new_user_list(self):
        cache.clear()
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        bonus_index_list = get_bonus_index_list(user.next_login_bonus_index)
        item_index = [0, 1, 2, 3]
        self.assertEqual(bonus_index_list, item_index, 'bonus_index_list should be ' + str(item_index) + ' but got ' + str(bonus_index_list))

    def test_get_bonus_index_list_index_0__first_item_is_end_of_master_list_item(self):
        cache.clear()
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        user.next_login_bonus_index = 0
        bonus_index_list = get_bonus_index_list(user.next_login_bonus_index)
        item_index = [5, 0, 1, 2]
        self.assertEqual(bonus_index_list, item_index, 'bonus_index_list should be ' + str(item_index) + ' but got ' + str(bonus_index_list))

    def test_get_bonus_index_list_index_larger_than_master_table__first_item_is_end_of_master_list_item(self):
        cache.clear()
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        user.next_login_bonus_index = 6
        bonus_index_list = get_bonus_index_list(user.next_login_bonus_index)
        item_index = [5, 0, 1, 2]
        self.assertEqual(bonus_index_list, item_index, 'bonus_index_list should be ' + str(item_index) + ' but got ' + str(bonus_index_list))

    def test_get_bonus_index_list_some_of_index_go_over_master_index__they_should_start_from_first_item_in_master(self):
        cache.clear()
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        user.next_login_bonus_index = 4
        bonus_index_list = get_bonus_index_list(user.next_login_bonus_index)
        item_index = [3, 4, 5, 0]
        self.assertEqual(bonus_index_list, item_index, 'bonus_index_list should be ' + str(item_index) + ' but got ' + str(bonus_index_list))
        user.next_login_bonus_index = 5
        bonus_index_list = get_bonus_index_list(user.next_login_bonus_index)
        item_index = [4, 5, 0, 1]
        self.assertEqual(bonus_index_list, item_index, 'bonus_index_list should be ' + str(item_index) + ' but got ' + str(bonus_index_list))

    def test_get_bonus_index_list_index_master_smaller_than_dialogue__should_repeat_the_master_item(self):
        cache.clear()
        LogInBonusesMaster.objects.get(bonus_index=3).delete()
        LogInBonusesMaster.objects.get(bonus_index=4).delete()
        LogInBonusesMaster.objects.get(bonus_index=5).delete()

        user = WUsers.objects.filter(phone_id='abcdefgh')[0]

        bonus_index_list = get_bonus_index_list(user.next_login_bonus_index)
        item_index = [0, 1, 2, 0]
        self.assertEqual(bonus_index_list, item_index, 'bonus_index_list should be ' + str(item_index) + ' but got ' + str(bonus_index_list))

    def test_get_bonus_index_list_index__no_master_table(self):
        cache.clear()
        LogInBonusesMaster.objects.all().delete()

        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        try:
            get_bonus_index_list(user.next_login_bonus_index)
        except Exception as e:
            self.assertEqual(str(e), 'No Bonus Items are listed in the master table')

    def test_update_login_bonus__updated_bonus_list_in_user_table(self):
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]

        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        new_bonus_index_list = get_bonus_index_list(user.next_login_bonus_index)
        update_bonus_items(user, new_bonus_index_list)
        new_login_bonus_items = [{'id': 'stamina_potion', 'qty': 5}, {'id': 'coin', 'qty': 100},
                                 {'id': 'starstone', 'qty': 32}, {'id': ingredient1.id, 'qty': 3}]
        self.assertEqual(user.login_bonus_items, new_login_bonus_items, 'login_bonus_items should be '
                         + str(new_login_bonus_items) + ' but got ' + str(user.login_bonus_items))

    def test_create_login_bonus_list__new_bonus_list_created(self):
        potion_item1 = Potions.objects.filter(name='t_potion1')[0]
        new_bonus_list = [5, 0, 1, 2]
        list =  create_login_bonus_list(new_bonus_list)
        new_login_bonus_items = [{'id': potion_item1.id, 'qty': 1},{'id': 'stamina_potion', 'qty': 5},
                                 {'id': 'coin', 'qty': 100},{'id': 'starstone', 'qty': 32}]
        self.assertEqual(list, new_login_bonus_items, 'login_bonus_items should be '
                         + str(new_login_bonus_items) + ' but got ' + str(list))

    def test_update_next_login_bonus_index__new_login_bonus_index(self):
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        new_bonus_index_list = [0, 1, 2, 3]
        update_next_login_bonus_index_and_date(user, now, new_bonus_index_list[2])
        self.assertEqual(user.next_login_bonus_index, 2, 'next_login_bonus_index should be 2 but got ' +
                         str(user.next_login_bonus_index))

    # def test_update_last_login_bonus_date__current_time(self):
    #     user = WUsers.objects.filter(phone_id='abcdefgh')[0]
    #     update_next_login_bonus_index_and_date(user, now)
    #     updated_user = WUsers.objects.filter(phone_id='abcdefgh')[0]
    #     self.assertEqual(updated_user.last_login_bonus_date, now, 'last_login_bonus_date should be ' + str(now) +
    #                      ' but got ' + str(updated_user.last_login_bonus_date))

    def test_give_user_bonus_item(self):
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        give_user_bonus_item(user)
        self.assertEqual(user.stamina_potion, 30, 'user stamina_potion should be 30 but got ' +
                         str(user.stamina_potion))

    def test_handle_inventory_items(self):
        potion_item1 = Potions.objects.filter(name='t_potion1')[0]
        user = WUsers.objects.filter(phone_id='11111111')[0]
        user.login_bonus_items[0]
        handle_inventory_items(user)
        item_set = UserItemInventory.objects.filter(user_id=user.id)[0]
        self.assertEqual(potion_item1.id, item_set.potion_id, 'potion id should be ' + item_set.potion_id + ' but got '
                         + potion_item1.id)

    def test_give_to_user_inventory(self):
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]
        give_to_user_inventory(user, ingredient1, 1, const.type_ingredient)
        item_set = UserItemInventory.objects.filter(user_id=user.id, ingredient_id=ingredient1.id, delete_flag=False)[0]
        self.assertEqual(item_set.quantity, 1, 'item quantity should be 1 but got ' + str(item_set.quantity))
        potion1 = Potions.objects.filter(name='t_potion1')[0]
        give_to_user_inventory(user, potion1, 2, const.type_potion)
        item_set = UserItemInventory.objects.filter(user_id=user.id, potion_id=potion1.id, delete_flag=False)[0]
        self.assertEqual(item_set.quantity, 2, 'item quantity should be 2 but got ' + str(item_set.quantity))
        item_set = UserItemInventory.objects.filter(user_id=user.id, delete_flag=False)
        self.assertEqual(len(item_set), 2, 'item should be 2 but got ' + str(len(item_set)))

#  integraton test
    def test_handle_login_bonus__index_2_new_login_bonus_items(self):
        c = Client()
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]

        c.post('/witches/login/0', {'phone_id': 'abcdefgh', 'device': 'Android', 'has_bonus': False})
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        new_login_bonus_items = [{'id': 'stamina_potion', 'qty': 5}, {'id': 'coin', 'qty': 100},
                                 {'id': 'starstone', 'qty': 32}, {'id': ingredient1.id, 'qty': 3}]

        self.assertEqual(user.next_login_bonus_index, 2, 'next_login_bonus_index should be 2 but got '
                         + str(user.next_login_bonus_index))
        self.assertEqual(user.login_bonus_items, new_login_bonus_items, 'login_bonus_items should be '
                         + str(new_login_bonus_items) + ' but got ' + str(user.login_bonus_items))

    def test_handle_login_bonus__updated_user_quantity(self):
        c = Client()
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]

        c.post('/witches/login/0', {'phone_id': 'abcdefgh', 'device': 'Android', 'has_bonus': False})
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        # new bonus
        [{'id': 'stamina_potion', 'qty': 5}, {'id': 'coin', 'qty': 100},
                                 {'id': 'starstone', 'qty': 32}, {'id': ingredient1.id, 'qty': 3}]

        self.assertEqual(user.free_currency, 1100, 'user coins should be 1100 but got ' +
                         str(user.free_currency))

    def test_handle_login_bonus_ineligible__no_updated_user_quantity(self):
        c = Client()
        ingredient1 = Ingredients.objects.filter(name='t_ingredient1')[0]

        c.post('/witches/login/0', {'phone_id': '22222222', 'device': 'Android', 'has_bonus': False})
        user = WUsers.objects.filter(phone_id='22222222')[0]
        # new bonus
        [{'id': 'stamina_potion', 'qty': 5}, {'id': 'coin', 'qty': 100},
                                 {'id': 'starstone', 'qty': 32}, {'id': ingredient1.id, 'qty': 3}]

        self.assertEqual(user.free_currency, 1000, 'user coins should be 100 but got ' +
                         str(user.free_currency))

    def test_handle_login_bonus__index_1_new_login_bonus_items(self):
        c = Client()
        potion1 = Potions.objects.filter(name='t_potion1')[0]
        c.post('/witches/login/0', {'phone_id': '12345678', 'device': 'Android', 'has_bonus': False})
        user = WUsers.objects.filter(phone_id='12345678')[0]
        new_login_bonus_items = [{'id': potion1.id, 'qty': 1},{'id': 'stamina_potion', 'qty': 5},
                                 {'id': 'coin', 'qty': 100},{'id': 'starstone', 'qty': 32}]

        self.assertEqual(user.next_login_bonus_index, 1, 'next_login_bonus_index should be 1 but got '
                         + str(user.next_login_bonus_index))
        self.assertEqual(user.login_bonus_items, new_login_bonus_items, 'login_bonus_items should be '
                         + str(new_login_bonus_items) + ' but got ' + str(user.login_bonus_items))

    def test_handle_login_bonus_flag_true__index_1_no_changes_in_login_bonus_items(self):
        c = Client()
        potion1 = Potions.objects.filter(name='t_potion1')[0]
        c.post('/witches/login/0', {'phone_id': 'abcdefgh', 'device': 'Android', 'has_bonus': True})
        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        owned_login_bonus_items = [{'id': potion1.id, 'qty': 1},{'id': 'stamina_potion', 'qty': 5},
                                   {'id': 'coin', 'qty': 100}, {'id': 'starstone', 'qty': 32}]

        self.assertEqual(user.next_login_bonus_index, 1, 'next_login_bonus_index should be 1 but got '
                         + str(user.next_login_bonus_index))
        self.assertEqual(user.login_bonus_items, owned_login_bonus_items, 'login_bonus_items should be '
                         + str(owned_login_bonus_items) + ' but got ' + str(user.login_bonus_items))

    def test_handle_login_bonus_old_user_no_bonus_fields__next_index_0_empty_list(self):
        c = Client()
        c.get('/witches/login/0', {'phone_id': '9876543', 'device': 'Android'})
        user = WUsers.objects.filter(phone_id='9876543')[0]
        self.assertEqual(user.next_login_bonus_index, 0, 'next_login_bonus_index should be 0 but got '
                         + str(user.next_login_bonus_index))
        self.assertEqual(len(user.login_bonus_items), 0, 'length of login bonus items should be 0 but got '
                         + str(len(user.login_bonus_items)))



    def tearDown(self):
            client = MongoClient('localhost', 27017)
            client.drop_database(name_or_database='UnitTest')
