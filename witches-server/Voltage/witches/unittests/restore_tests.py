__author__ = 'yoshi.miyamoto'
from django.test.client import Client
from witches.models import *
from pymongo import MongoClient
from django.utils import unittest


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        WUsers.objects.create(last_name='t_last2', first_name='t_user2', gender='Female', work=[],
                                                 email='t_user2@test.com', birthday='08/20/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='12345678', closet=2)

        # Category
        Categories.objects.create(name='ingredient_category', description='Silver', type=0,
                                  color=000010)
        Categories.objects.create(name='ingredient_category2', description='Moonstone', type=0,
                                  color=000010)
        Categories.objects.create(name='ingredient_category3', description='Artemisia', type=0,
                                  color=000010)
        Categories.objects.create(name='ingredient_category4', description='Rosemary', type=0,
                                  color=000010)

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
        GameProperties.objects.create(name='default_stamina_potions', value=25)

    def test_http_request_password(self):
        c = Client()
        c.get('/witches/create_user/1/')
        param = {'phone_id': 'none'}
        r = c.post('/witches/password/', param)
        self.assertEqual(r.status_code, 200, 'request password html failed')
        param2 = {'phone_id': '12345678'}
        r2 = c.post('/witches/get_password/0', param2)
        user = WUsers.objects.filter(phone_id='12345678')[0]
        self.assertEqual(r2.status_code, 200, 'request password failed')
        self.assertEqual(len(user.password), 4, 'Password was not right length')
        self.assertEqual(len(user.phone_id), 8, 'User ID was not right length')

    def test_http_restore(self):
        c = Client()
        param = {'phone_id': '12345678'}
        u1r = c.post('/witches/password/', param)
        self.assertEqual(u1r.status_code, 200, 'request password html failed')
        u1r2 = c.post('/witches/get_password/0', param)
        self.assertEqual(u1r2.status_code, 200, 'request get password failed')

        user = WUsers.objects.filter(phone_id='12345678')[0]
        self.assertEqual(len(user.password), 4, 'Password was not right length')

        u2r = c.post('/witches/restore/', param)
        self.assertEqual(u2r.status_code, 200, 'restore html failed')

        param3 = {'phone_id': user.phone_id, 'password': user.password}
        r3 = c.post('/witches/start_restore/0', param3)

        self.assertEqual(r3.status_code, 200, 'start restore failed')

    def tearDown(self):
            client = MongoClient('localhost', 27017)
            client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()