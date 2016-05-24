__author__ = 'yoshi.miyamoto'


from django.utils import unittest
from pymongo import MongoClient
from django.test.client import Client
from witches.models import  WUsers, UserMailBox, EmailTemplates, Characters, UserCharacters, \
    AvatarItems, Categories, UserBooks, Potions, BookPrizes, Recipes, Books, \
    UserCompleteRecipes
from witches.unittests import const
from django.core.cache import cache

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



class ModelsTestCase(unittest.TestCase):
    def setUp(self):

        Categories.objects.create(name='avatar_category1', description='ACCESSORIES', type=1, color=00005)
        Categories.objects.create(name='avatar_category2', description='SKIN', type=1,color=00005)

        avatar_category1 = Categories.objects.filter(name='avatar_category1')[0]
        avatar_category2 = Categories.objects.filter(name='avatar_category2')[0]

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

        # Category
        Categories.objects.create(name='ingredient_category', description='Silver', type=0,
                                  color=000010)
        Categories.objects.create(name='ingredient_category2', description='Moonstone', type=0,
                                  color=000010)
        ingredient_category = Categories.objects.filter(name='ingredient_category')[0]
        ingredient_category2 = Categories.objects.filter(name='ingredient_category2')[0]

        avatar_item1 = AvatarItems.objects.filter(name='Baseball Cap')[0]
        avatar_item2 = AvatarItems.objects.filter(name='Shirt')[0]

        # Characters
        Characters.objects.create(first_name='K&C', romanceable=1)
        Characters.objects.create(first_name='Anastasia', last_name='Petrova', initial='A', romanceable=1)
        anastasia = Characters.objects.filter(first_name='Anastasia')[0]

        # mail
        mail_attachment = [{'id': avatar_item1.id, 'received_flag': False}, {'id': avatar_item2.id,
                                                                             'received_flag': False}]
        EmailTemplates.objects.create(premium_currency='1', sender_id=anastasia.id, free_currency='100',
                                      body_text='unittest', attach_list=mail_attachment, stamina_potion='None')
        mail = EmailTemplates.objects.get(body_text='unittest')


        # Book Prizes
        BookPrizes.objects.create(name='t_bookprize1', type='avatar', reward_id=avatar_item1.id, quantity=1)
        bookprize1 = BookPrizes.objects.filter(name='t_bookprize1')[0]

        # Potion
        Potions.objects.create(name='t_potion1', description='test potion 1', type=1, color='yellow',
                               effect_list=[{'A': 80}, {'N':80}])
        Potions.objects.create(name='t_potion2', description='test potion 2', type=2, color='red',
                               effect_list=[{'A': 20}, {'T':110}])
        Potions.objects.create(name='t_potion3', description='test potion 3', type=2, color='blue',
                               effect_list=[{'R': 60}, {'M':10}])

        potion1 = Potions.objects.filter(name='t_potion1')[0]
        potion2 = Potions.objects.filter(name='t_potion2')[0]
        potion3 = Potions.objects.filter(name='t_potion3')[0]

        # Recipes
        Recipes.objects.create(name='t_recipe1', display_order=1, hint='t_hint1',
                               ingredient_list=[{'category': ingredient_category.id, 'quantity': 10},
                                                {'category': ingredient_category2.id, 'quantity': 10}], replay_flag=False,
                               potion_list={'master': potion1.id, 'superior': potion2.id, 'basic': potion3.id},
                               score_list={'low': 0.25, 'mid': 0.5, 'high': 0.75},
                               game_duration=30, continue_duration=10)

        Recipes.objects.create(name='t_recipe2', display_order=2, hint='t_hint2',
                               ingredient_list=[{'category': ingredient_category.id, 'quantity': 20},
                                                {'category': ingredient_category2.id, 'quantity': 50}], replay_flag=False,
                               potion_list={'master': potion3.id, 'superior': potion1.id, 'basic': potion2.id},
                               score_list={'low': 0.25, 'mid': 0.5, 'high': 0.75},
                               game_duration=10, continue_duration=30)

        recipe1 = Recipes.objects.get(name='t_recipe1')
        recipe2 = Recipes.objects.get(name='t_recipe2')


        # Books
        Books.objects.create(name='book1', display_order=1, available=True, mail_id=mail.id,
                             book_prize_id=bookprize1.id, recipes=[recipe1.id, recipe2.id])

        book = Books.objects.get(name='book1')


        # User
        cache.set('user1', WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                                                 email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='abcdefgh', closet=30, current_book_id=book.id))


        user1 = WUsers.objects.filter(phone_id='abcdefgh')[0]

        book_list = []
        book_list.append(book.id)


        UserBooks.objects.create(user_id=user1.id, book_list=book_list)

        # User Characters
        affinities_dict = {"A": 0, "M": 0, "N": 0, "R": 0, "T": 0}
        UserCharacters.objects.create(user_id=user1.id, affinities=affinities_dict)

        UserCompleteRecipes.objects.create(user_id=user1.id, recipe_id=recipe1.id, level=3)

    def test_complete_book(self):
        c = Client()
        recipe2 = Recipes.objects.get(name='t_recipe2')
        potion3 = Potions.objects.filter(name='t_potion3')[0]

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'potion_id': potion3.id, 'stars': 3}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 2, 'User mail count should be 2 but got ' + str(user_mail.count()))

        for mail in user_mail:
            if mail.title != 'Minigame Potion': #  Character mail
                prize = mail.gifts[0]['id']
                bookprize1 = BookPrizes.objects.filter(name='t_bookprize1')[0]
                self.assertEqual(prize, bookprize1.reward_id, 'book prize has wrong id, it should be ' + str(bookprize1.reward_id))
            else:
                potion_id = mail.gifts[0]['id']
                self.assertEqual(potion_id, potion3.id, 'potion has wrong id, it should be ' + str(potion3.id) +
                                 ' but got ' + str(potion_id))

    def test_not_compelete_book(self):
        c = Client()
        recipe2 = Recipes.objects.get(name='t_recipe2')
        potion1 = Potions.objects.filter(name='t_potion1')[0]

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'potion_id': potion1.id, 'stars': 2}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 1, 'User mail count should be 1 but got ' + str(user_mail.count()))

        for mail in user_mail:
            if mail.title != 'Minigame Potion': #  Character mail
                prize = mail.gifts[0]['id']
                bookprize1 = BookPrizes.objects.filter(name='t_bookprize1')[0]
                self.assertEqual(prize, bookprize1.reward_id, 'book prize has wrong id, it should be ' + str(bookprize1.reward_id))
            else:
                potion_id = mail.gifts[0]['id']
                self.assertEqual(potion_id, potion1.id, 'potion has wrong id, it should be ' + str(potion_id))

    def test_not_compelete_book_then_complete(self):
        c = Client()
        recipe2 = Recipes.objects.get(name='t_recipe2')
        potion1 = Potions.objects.filter(name='t_potion1')[0]
        potion3 = Potions.objects.filter(name='t_potion3')[0]

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'potion_id': potion1.id, 'stars': 2}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 1, 'User mail count should be 1 but got ' + str(user_mail.count()))

        for mail in user_mail:
            if mail.title != 'Minigame Potion': #  Character mail
                prize = mail.gifts[0]['id']
                bookprize1 = BookPrizes.objects.filter(name='t_bookprize1')[0]
                self.assertEqual(prize, bookprize1.reward_id, 'book prize has wrong id, it should be ' +
                                 str(bookprize1.reward_id) + ' but got ' + str(prize))
            else:
                potion_id = mail.gifts[0]['id']
                self.assertEqual(potion_id, potion1.id, 'potion has wrong id, it should be ' + str(potion1.id) +
                                 ' bit got '+ str(potion_id))

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'potion_id': potion3.id, 'stars': 3}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)

        self.assertEqual(user_mail.count(), 3, 'User mail count should be 3 but got ' + str(user_mail.count()))

    def test_complete_and_redo_recipe(self):
        c = Client()
        recipe2 = Recipes.objects.get(name='t_recipe2')
        potion3 = Potions.objects.filter(name='t_potion3')[0]
        potion1 = Potions.objects.filter(name='t_potion1')[0]

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'potion_id': potion3.id, 'stars': 3}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 2, 'User mail count should be 2 but got ' + str(user_mail.count()))

        for mail in user_mail:
            if mail.title != 'Minigame Potion': #  Character mail
                prize = mail.gifts[0]['id']
                bookprize1 = BookPrizes.objects.filter(name='t_bookprize1')[0]
                self.assertEqual(prize, bookprize1.reward_id, 'book prize has wrong id, it should be ' + str(bookprize1.reward_id) +
                                 ' but got ' + str(prize))
            else:
                potion_id = mail.gifts[0]['id']
                self.assertEqual(potion_id, potion3.id, 'potion has wrong id, it should be ' + str(potion3.id) +
                                 ' but got ' + str(potion_id))

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'potion_id': potion1.id, 'stars': 2}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 3, 'User mail count should be 3 but got ' + str(user_mail.count()))

        minigame_potion = UserMailBox.objects.filter(user_id=user.id, title='Minigame Potion')
        self.assertEqual(minigame_potion.count(), 2, 'User mail for minigame count should be 2 but got ' + str(minigame_potion.count()))
        prize_potion = UserMailBox.objects.filter(user_id=user.id, message_body='unittest')
        self.assertEqual(prize_potion.count(), 1, 'User mail for prize count should be 1 but got ' + str(prize_potion.count()))
        completed_recipes = UserCompleteRecipes.objects.filter(user_id=user.id, recipe_id=recipe2.id)[0]
        self.assertEqual(completed_recipes.level, 3, 'completed highest recipe level should be 3 but got ' + str(completed_recipes.level))

    def test_complete_twice(self):
        c = Client()
        recipe2 = Recipes.objects.get(name='t_recipe2')
        potion3 = Potions.objects.filter(name='t_potion3')[0]

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'potion_id': potion3.id, 'stars': 3}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 2, 'User mail count should be 2 but got ' + str(user_mail.count()))

        for mail in user_mail:
            if mail.title != 'Minigame Potion': #  Character mail
                prize = mail.gifts[0]['id']
                bookprize1 = BookPrizes.objects.filter(name='t_bookprize1')[0]
                self.assertEqual(prize, bookprize1.reward_id, 'book prize has wrong id, it should be ' + str(bookprize1.reward_id))
            else:
                potion_id = mail.gifts[0]['id']
                self.assertEqual(potion_id, potion3.id, 'potion has wrong id, it should be ' + str(potion3.id) +
                                 ' but got ' + str(potion_id))

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'potion_id': potion3.id, 'stars': 3}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 3, 'User mail count should be 3 but got ' + str(user_mail.count()))

        minigame_potion = UserMailBox.objects.filter(user_id=user.id, title='Minigame Potion')
        self.assertEqual(minigame_potion.count(), 2, 'User mail for minigame count should be 2 but got ' + str(minigame_potion.count()))
        prize_potion = UserMailBox.objects.filter(user_id=user.id, message_body='unittest')
        self.assertEqual(prize_potion.count(), 1, 'User mail for prize count should be 1 but got ' + str(prize_potion.count()))
        completed_recipes = UserCompleteRecipes.objects.filter(user_id=user.id, recipe_id=recipe2.id)[0]
        self.assertEqual(completed_recipes.level, 3, 'completed highest recipe level should be 3 but got ' + str(completed_recipes.level))

    def test_wrong_level(self):
        c = Client()
        recipe2 = Recipes.objects.get(name='t_recipe2')
        potion1 = Potions.objects.filter(name='t_potion1')[0]

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'potion_id': potion1.id, 'stars': -1}
        r = c.post('/witches/save_potion_result/1', param)
        self.assertIn('failed', r.content, 'this should failed but status didn\'t say failed' )

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 0, 'User mail count should be 0 but got ' + str(user_mail.count()))

    def test_save_recipe_result_zero_star(self):
        c = Client()
        recipe2 = Recipes.objects.get(name='t_recipe2')

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'stars': 0}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 0, 'User mail count should be 0 but got ' + str(user_mail.count()))

    def test_save_recipe_result_complete_book_no_potion_id_in_api(self):
        c = Client()
        recipe2 = Recipes.objects.get(name='t_recipe2')
        potion3 = Potions.objects.filter(name='t_potion3')[0]

        param = {'phone_id': 'abcdefgh', 'recipe_id': recipe2.id, 'stars': 3}
        c.post('/witches/save_potion_result/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        user_mail = UserMailBox.objects.filter(user_id=user.id)
        self.assertEqual(user_mail.count(), 2, 'User mail count should be 2 but got ' + str(user_mail.count()))

        for mail in user_mail:
            if mail.title != 'Minigame Potion': #  Character mail
                prize = mail.gifts[0]['id']
                bookprize1 = BookPrizes.objects.filter(name='t_bookprize1')[0]
                self.assertEqual(prize, bookprize1.reward_id, 'book prize has wrong id, it should be ' + str(bookprize1.reward_id))
            else:
                potion_id = mail.gifts[0]['id']
                self.assertEqual(potion_id, potion3.id, 'potion has wrong id, it should be ' + str(potion3.id) +
                                 ' but got ' + str(potion_id))

    def tearDown(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()
