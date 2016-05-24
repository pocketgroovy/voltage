import json
from django.test import Client
from django.utils import unittest
from pymongo import MongoClient
from witches.models import *
from django.core.cache import cache

__author__ = 'yoshi.miyamoto'

class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        cache.set('user1', WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                                                 email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='abcdefgh', closet=30))

        WUsers.objects.create(last_name='t_last2', first_name='t_user2', gender='Male', work=[],
                                                 email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='12345678', closet=30)

        user1 = WUsers.objects.filter(phone_id='abcdefgh')[0]

        Categories.objects.create(name='avatar_category1', description='ACCESSORIES', type=1, color=00005)
        Categories.objects.create(name='avatar_category2', description='SKIN', type=1,color=00005)
        Categories.objects.create(name='avatar_category3', description='BOTTOMS', type=1, color=00005)
        Categories.objects.create(name='avatar_category4', description='DRESSES', type=1, color=00005)
        Categories.objects.create(name='avatar_category5', description='HAIRSTYLES', type=1, color=00005)
        Categories.objects.create(name='avatar_category6', description='HATS', type=1, color=00005)

        avatar_category1 = Categories.objects.filter(name='avatar_category1')[0]
        avatar_category2 = Categories.objects.filter(name='avatar_category2')[0]
        avatar_category3 = Categories.objects.filter(name='avatar_category3')[0]
        avatar_category4 = Categories.objects.filter(name='avatar_category4')[0]
        avatar_category5 = Categories.objects.filter(name='avatar_category5')[0]
        avatar_category6 = Categories.objects.filter(name='avatar_category6')[0]

        cache.set('avatar_item1', AvatarItems.objects.create(category_id=avatar_category1.id, description=avatar_category1.description,
                                   name='Baseball Cap', premium_price=10, currency_flag=2,
                                   slots_layer=0, display_order=2))

        AvatarItems.objects.create(category_id=avatar_category2.id, description=avatar_category2.description,
                                   name='Shirt', slots_layer=0,
                                   coins_price=2, currency_flag=3, display_order=4)

        AvatarItems.objects.create(category_id=avatar_category3.id,
                                   description=avatar_category3.description, slots_layer=0,
                                   name='Boots', coins_price=3, currency_flag=3, display_order=3)

        cache.set('avatar_item4', AvatarItems.objects.create(category_id=avatar_category4.id, description=avatar_category4.description,
                                   slots_layer=0, name='Fedora', premium_price=5, currency_flag=2, display_order=5))

        AvatarItems.objects.create(category_id=avatar_category5.id, description=avatar_category5.description,
                                   slots_layer=0, name='T-shirt', premium_price=1, currency_flag=2, display_order=7)

        AvatarItems.objects.create(category_id=avatar_category6.id,description=avatar_category6.description,
                                   slots_layer=0, name='Jeans', coins_price=2, currency_flag=3, display_order=10)

        avatar_item4 = AvatarItems.objects.filter(name='Fedora')[0]
        avatar_item5 = AvatarItems.objects.filter(name='T-shirt')[0]
        avatar_item6 = AvatarItems.objects.filter(name='Jeans')[0]

        # UserClothingCoordination
        UserClothingCoordination.objects.create(user_id=user1.id, coordinate_list=[avatar_item4.id, avatar_item5.id,
                                                                                   avatar_item6.id])

    def test_remove_items(self):
        c = Client()
        avatar_item1 = AvatarItems.objects.filter(name='Baseball Cap')[0]

        # buy new item with stones
        param = {'phone_id': 'abcdefgh', 'item_type': 1,
                 'item_id': avatar_item1.id, 'quantity': 1}
        r2 = c.post('/witches/buy_with_stones/0', param)

        user = WUsers.objects.filter(phone_id='abcdefgh')[0]
        user_closet = UserAvatarItemsInCloset.objects.filter(user_id=user.id)

        self.assertEqual(r2.status_code, 200, 'buy new item with stones failed')
        self.assertEqual(user.premium_currency, 10, 'user premium currency should be 10 but got ' + str(user.premium_currency))
        self.assertEqual(user_closet.count(), 1, 'avatar item in closet should be 1 but got ' + str(user_closet.count()))

        param = {'phone_id': 'abcdefgh', 'avatar_item_id': avatar_item1.id}
        c.post('/witches/remove_avatar_item/0', param)
        user_closet = UserAvatarItemsInCloset.objects.filter(user_id=user.id)
        self.assertEqual(user_closet.count(), 0, 'avatar item in closet should be 0 but got ' + str(user_closet.count()))
        user_removed_item = UserItemRemovalHistory.objects.filter(user_id=user.id)
        self.assertEqual(user_removed_item.count(), 1, 'removed avatar item should be 1 but got ' + str(user_removed_item.count()))
        self.assertEqual(user_removed_item[0].avatar_item_id, avatar_item1.id, 'removed avatar item should be ' +
                         str(avatar_item1.id) + ' but got ' + str(user_removed_item.count()))

    def test_save_coordination(self):
        avatar_item1 = AvatarItems.objects.filter(name='Baseball Cap')[0]
        avatar_item2 = AvatarItems.objects.filter(name='Shirt')[0]
        avatar_item3 = AvatarItems.objects.filter(name='Boots')[0]
        avatar_item4 = AvatarItems.objects.filter(name='Fedora')[0]
        avatar_item5 = AvatarItems.objects.filter(name='T-shirt')[0]
        avatar_item6 = AvatarItems.objects.filter(name='Jeans')[0]

        avatar_item_list = [avatar_item1.id, avatar_item2.id, avatar_item3.id, avatar_item4.id, avatar_item5.id,
                            avatar_item6.id]
        avatar_item_jsonlist = json.dumps(avatar_item_list)

        c = Client()
        param = {'phone_id': '12345678', 'coordination_list': avatar_item_jsonlist}
        c.post('/witches/save_coordination/0', param)
        user = WUsers.objects.get(phone_id='12345678')
        user_coordination = UserClothingCoordination.objects.filter(user_id=user.id)
        avatar_closet = UserAvatarItemsInCloset.objects.filter(user_id=user.id)
        self.assertEqual(user_coordination.count(), 1, 'user coordination should be 1 but got ' + str(user_coordination.count()))
        self.assertEqual(avatar_closet.count(), 7, 'user avatar closet should be 7 but got ' + str(avatar_closet.count()))
        for closet_item in avatar_closet:
            if closet_item.coordinate_item_id:
                self.assertEqual(closet_item.coordinate_item_id, user_coordination[0].id,
                                 'coordinate id in closet should be ' + str(user_coordination[0].id) + ' but got '
                                 + str(closet_item.coordinate_item_id))

    def test_remove_coordination_item(self):
        avatar_item1 = AvatarItems.objects.filter(name='Baseball Cap')[0]
        avatar_item2 = AvatarItems.objects.filter(name='Shirt')[0]
        avatar_item3 = AvatarItems.objects.filter(name='Boots')[0]
        avatar_item4 = AvatarItems.objects.filter(name='Fedora')[0]
        avatar_item5 = AvatarItems.objects.filter(name='T-shirt')[0]
        avatar_item6 = AvatarItems.objects.filter(name='Jeans')[0]

        avatar_item_list = [avatar_item1.id, avatar_item2.id, avatar_item3.id, avatar_item4.id, avatar_item5.id,
                            avatar_item6.id]
        avatar_item_jsonlist = json.dumps(avatar_item_list)

        c = Client()
        param = {'phone_id': '12345678', 'coordination_list': avatar_item_jsonlist}
        c.post('/witches/save_coordination/0', param)
        user = WUsers.objects.get(phone_id='12345678')
        user_coordination = UserClothingCoordination.objects.filter(user_id=user.id)
        avatar_closet = UserAvatarItemsInCloset.objects.filter(user_id=user.id)
        self.assertEqual(user_coordination.count(), 1, 'user coordination should be 1 but got ' + str(user_coordination.count()))
        self.assertEqual(avatar_closet.count(), 7, 'user avatar closet should be 7 but got ' + str(avatar_closet.count()))
        for closet_item in avatar_closet:
            if closet_item.coordinate_item_id:
                self.assertEqual(closet_item.coordinate_item_id, user_coordination[0].id,
                                 'coordinate id in closet should be ' + str(user_coordination[0].id) + ' but got '
                                 + str(closet_item.coordinate_item_id))

        param = {'phone_id': '12345678', 'avatar_item_id': avatar_item1.id}
        c.post('/witches/remove_avatar_item/0', param)
        user_closet = UserAvatarItemsInCloset.objects.filter(user_id=user.id)
        self.assertEqual(user_closet.count(), 5, 'avatar item in closet should be 5 but got ' + str(user_closet.count()))
        user_removed_item = UserItemRemovalHistory.objects.filter(user_id=user.id)
        self.assertEqual(user_removed_item.count(), 1, 'removed avatar item should be 1 but got ' + str(user_removed_item.count()))
        self.assertEqual(user_removed_item[0].avatar_item_id, avatar_item1.id, 'removed avatar item should be ' +
                         str(avatar_item1.id) + ' but got ' + str(user_removed_item[0].avatar_item_id))

    def test_cache_avataritems(self):
        avataritems = cache.get('avatar_item1')
        self.assertEqual(avataritems.description, 'ACCESSORIES')
        self.assertEqual(avataritems.premium_price, 10)
        self.assertEqual(avataritems.currency_flag, 2)
        self.assertEqual(avataritems.name, 'Baseball Cap')

    def test_cache_userclothingcoordination(self):
        user = cache.get('user1')
        avatar_item = cache.get('avatar_item4')
        user_coordination = UserClothingCoordination.objects.filter(user_id=user.id)
        self.assertTrue(avatar_item.id in user_coordination[0].coordinate_list)

    def tearDown(self):
            client = MongoClient('localhost', 27017)
            client.drop_database(name_or_database='UnitTest')


if __name__ == '__main__':
    unittest.main()