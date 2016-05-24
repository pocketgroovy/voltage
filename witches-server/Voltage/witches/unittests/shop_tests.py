import json
from witches.utils.purchase import verify_amazon_receipt

__author__ = 'yoshi.miyamoto'

from django.utils import unittest
from pymongo import MongoClient
from django.test.client import Client
from witches.unittests import const
from witches.models import *
# ticket type
const.stamina_ticket = 0
const.closet_ticket = 2

# currency type
const.currency_stamina_potion = 1
const.currency_stone = 2
new_receipt = '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'
old_receipt = 'ewoJInNpZ25hdHVyZSIgPSAiQWpSZmZkOGpJZXpWSDRiYjQ3YlFRU2U5QnNxL09VQ2FXb2p4SVU1M29iM2FSOXprWDRxeC9Mb0NMZEIrRGh3V21JNmRzZHZhTEhZRldlTzRsa05XR1dDU3V1Rm1PMlp4UE94ME5jNFROVW0yTENNbng2K3VUVDhQb2RQZXN5dk5YU3RJMkZNZGxaYXB1Tk12UzlidmhoWC9LNEVhMWpYMkovL1pZY1Z6WCtQRUFBQURWekNDQTFNd2dnSTdvQU1DQVFJQ0NCdXA0K1BBaG0vTE1BMEdDU3FHU0liM0RRRUJCUVVBTUg4eEN6QUpCZ05WQkFZVEFsVlRNUk13RVFZRFZRUUtEQXBCY0hCc1pTQkpibU11TVNZd0pBWURWUVFMREIxQmNIQnNaU0JEWlhKMGFXWnBZMkYwYVc5dUlFRjFkR2h2Y21sMGVURXpNREVHQTFVRUF3d3FRWEJ3YkdVZ2FWUjFibVZ6SUZOMGIzSmxJRU5sY25ScFptbGpZWFJwYjI0Z1FYVjBhRzl5YVhSNU1CNFhEVEUwTURZd056QXdNREl5TVZvWERURTJNRFV4T0RFNE16RXpNRm93WkRFak1DRUdBMVVFQXd3YVVIVnlZMmhoYzJWU1pXTmxhWEIwUTJWeWRHbG1hV05oZEdVeEd6QVpCZ05WQkFzTUVrRndjR3hsSUdsVWRXNWxjeUJUZEc5eVpURVRNQkVHQTFVRUNnd0tRWEJ3YkdVZ1NXNWpMakVMTUFrR0ExVUVCaE1DVlZNd2daOHdEUVlKS29aSWh2Y05BUUVCQlFBRGdZMEFNSUdKQW9HQkFNbVRFdUxnamltTHdSSnh5MW9FZjBlc1VORFZFSWU2d0Rzbm5hbDE0aE5CdDF2MTk1WDZuOTNZTzdnaTNvclBTdXg5RDU1NFNrTXArU2F5Zzg0bFRjMzYyVXRtWUxwV25iMzRucXlHeDlLQlZUeTVPR1Y0bGpFMU93QytvVG5STStRTFJDbWVOeE1iUFpoUzQ3VCtlWnRERWhWQjl1c2szK0pNMkNvZ2Z3bzdBZ01CQUFHamNqQndNQjBHQTFVZERnUVdCQlNKYUVlTnVxOURmNlpmTjY4RmUrSTJ1MjJzc0RBTUJnTlZIUk1CQWY4RUFqQUFNQjhHQTFVZEl3UVlNQmFBRkRZZDZPS2RndElCR0xVeWF3N1hRd3VSV0VNNk1BNEdBMVVkRHdFQi93UUVBd0lIZ0RBUUJnb3Foa2lHOTJOa0JnVUJCQUlGQURBTkJna3Foa2lHOXcwQkFRVUZBQU9DQVFFQWVhSlYyVTUxcnhmY3FBQWU1QzIvZkVXOEtVbDRpTzRsTXV0YTdONlh6UDFwWkl6MU5ra0N0SUl3ZXlOajVVUllISytIalJLU1U5UkxndU5sMG5rZnhxT2JpTWNrd1J1ZEtTcTY5Tkluclp5Q0Q2NlI0Szc3bmI5bE1UQUJTU1lsc0t0OG9OdGxoZ1IvMWtqU1NSUWNIa3RzRGNTaVFHS01ka1NscDRBeVhmN3ZuSFBCZTR5Q3dZVjJQcFNOMDRrYm9pSjNwQmx4c0d3Vi9abEwyNk0ydWVZSEtZQ3VYaGRxRnd4VmdtNTJoM29lSk9PdC92WTRFY1FxN2VxSG02bTAzWjliN1BSellNMktHWEhEbU9Nazd2RHBlTVZsTERQU0dZejErVTNzRHhKemViU3BiYUptVDdpbXpVS2ZnZ0VZN3h4ZjRjemZIMHlqNXdOelNHVE92UT09IjsKCSJwdXJjaGFzZS1pbmZvIiA9ICJld29KSW05eWFXZHBibUZzTFhCMWNtTm9ZWE5sTFdSaGRHVXRjSE4wSWlBOUlDSXlNREUyTFRBeExUQTRJREUxT2pFeE9qRTNJRUZ0WlhKcFkyRXZURzl6WDBGdVoyVnNaWE1pT3dvSkluVnVhWEYxWlMxcFpHVnVkR2xtYVdWeUlpQTlJQ0k1TTJSaE5qWTJNV0pqT0RoaE56QmlOekkxWkRSa1pETXlZMkkyTnpjMU0yRXhPRFExWVdSaklqc0tDU0p2Y21sbmFXNWhiQzEwY21GdWMyRmpkR2x2YmkxcFpDSWdQU0FpTVRBd01EQXdNREU0T0RBMU56STVNQ0k3Q2draVluWnljeUlnUFNBaU1DSTdDZ2tpZEhKaGJuTmhZM1JwYjI0dGFXUWlJRDBnSWpFd01EQXdNREF4T0Rnd05UY3lPVEFpT3dvSkluRjFZVzUwYVhSNUlpQTlJQ0l4SWpzS0NTSnZjbWxuYVc1aGJDMXdkWEpqYUdGelpTMWtZWFJsTFcxeklpQTlJQ0l4TkRVeU1qazBOamMzTURBd0lqc0tDU0oxYm1seGRXVXRkbVZ1Wkc5eUxXbGtaVzUwYVdacFpYSWlJRDBnSWpjd09VVkVRa00zTFVFMk5UQXRORFpFTmkwNU56bEZMVFZHT1VSRU4wWTVNVFZCUXlJN0Nna2ljSEp2WkhWamRDMXBaQ0lnUFNBaVkyOXRMblp2YkhSaFoyVXVaVzUwTG5kcGRHTm9MakF3TVNJN0Nna2lhWFJsYlMxcFpDSWdQU0FpT1RZNE5EYzJNekUySWpzS0NTSmlhV1FpSUQwZ0ltTnZiUzUyYjJ4MFlXZGxMbU4xY25ObExtVnVJanNLQ1NKd2RYSmphR0Z6WlMxa1lYUmxMVzF6SWlBOUlDSXhORFV5TWprME5qYzNNREF3SWpzS0NTSndkWEpqYUdGelpTMWtZWFJsSWlBOUlDSXlNREUyTFRBeExUQTRJREl6T2pFeE9qRTNJRVYwWXk5SFRWUWlPd29KSW5CMWNtTm9ZWE5sTFdSaGRHVXRjSE4wSWlBOUlDSXlNREUyTFRBeExUQTRJREUxT2pFeE9qRTNJRUZ0WlhKcFkyRXZURzl6WDBGdVoyVnNaWE1pT3dvSkltOXlhV2RwYm1Gc0xYQjFjbU5vWVhObExXUmhkR1VpSUQwZ0lqSXdNVFl0TURFdE1EZ2dNak02TVRFNk1UY2dSWFJqTDBkTlZDSTdDbjA9IjsKCSJlbnZpcm9ubWVudCIgPSAiU2FuZGJveCI7CgkicG9kIiA9ICIxMDAiOwoJInNpZ25pbmctc3RhdHVzIiA9ICIwIjsKfQ=='
temp_receipt = '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'
user_receipt_missing_in_app ='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'
android_receipt = '{"json":"{\"orderId\":\"GPA.1313-2048-1054-43880\",\"packageName\":\"com.voltage.curse.en\",\"productId\":\"com.voltage.ent.witch.201\",\"purchaseTime\":1458083737013,\"purchaseState\":0,\"purchaseToken\":\"hmdfhdhelneenamjoeijncek.AO-J1OysWboSIVA8DAyQ43_7IcuAnQuHGgVQE-Q9O_VTsEWbLimyO-ZNmPY3Pyf0g-cnweCQ2RfjpaXXwbiQNIb_GxiLAs1iWLXVpOHUpevqlfzbkFav4wkToBEd1I8ZmW67e3floGhd\"}","signature":"AZOw\/59t\/YKuW6sJ\/vPVMoZcH3C6DmE+Mu0\/Eq+VbUxbGVasyhP44Q5l4ZRujFNx8yJOuWZgiu9DJwJvrNVKgOG0RYslG6kTMQDe14M\/iT935oVVhk+qDgrQnXLiqZ+igw7\/UW3TJgHZ1jGvCHIOCLMKcPuF0GuXeK60\/tN5EwjwRzyDM45lP\/MmDnbA4j467tdtAuE8VGnw1BNQHyXUCwNbsCF7MeZOrFB5E+jHByqWwIgqWToqZgOBp+wHdSB0NwAV+ERr3AnfltObWQ4qDwVX\/Dl94BZ3Wm35S+HJUnVBwlveUEHRmGXzH7JLbo60Y1dRIC98jHfw00bfcsIdoQ=="}'
fail_receipt = '{"json":"{\"orderId\":\"4775997339261082820.6293655457270568\",\"packageName\":\"com.voltage.curse.en\",\"productId\":\"com.voltage.ent.witch.006\",\"purchaseTime\":1460445733195,\"purchaseState\":0,\"developerPayload\":\"\",\"purchaseToken\":\"idtiktqfjboenlpgsglzqedl\"}","signature":"VS8dYZeew1lQn9L91bd+qsaRf8hLLzp1ZoifOlP0TH\/Id9lSjvOnlLAnLWUAIlV7uP8tRsBtrqiuC1wWJwTZL\/EabvjeMH8RfFDuBkM+D\/SU1W0x9IZ10zC3b4uNISl0itZ\/I9CK\/6GGT31w1T9vecpb+n74qJIwv5erl5XXE5fXNlkP3buy5MU21D9CbbeZjI3kiU830lCStIJk5SWNihtj\/GUzF0Xx09TJmeq20b9SLaWqdIXnkch3QaI4\/yDcIPrxAzdrtNdtJYc+gZ1jIljprGFSYZdk3qaZTtoXzxW0\/mYP\/bOIYPdRCuCNaAg="}'
sample_amazon_response = '{"receiptId":"q1YqVrJSSs7P1UvMTazKz9PLTCwoTswtyEktM9JLrShIzCvOzM-LL04tiTdW0lFKASo2NDEwMjCwMDM2MTC0AIqVAsUsLd1c4l18jIxdfTOK_N1d8kqLLHVLc8oK83OLgtPNCit9AoJdjJ3dXG2BGkqUrAxrAQ","productId":"com.amazon.iapsamplev2.expansion_set_3","parentProductId":null,"productType":"ENTITLED","cancelDate":null,"quantity":1,"betaProduct":false,"testTransaction":true,"purchaseDate":1402008634018}'
amazon_receipt_id = 'q1YqVrJSSs7P1UvMTazKz9PLTCwoTswtyEktM9JLrShIzCvOzM-LL04tiTdW0lFKASo2NDEwMjCwMDM2MTC0AIqVAsUsLd1c4l18jIxdfTOK_N1d8kqLLHVLc8oK83OLgtPNCit9AoJdjJ3dXG2BGkqUrAxrAQ'
amazon_user_id = '99FD_DL23EMhrOGDnur9-ulvqomrSg6qyLPSD3CFE='
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
        AvatarItems.objects.create(category_id=avatar_category1.id,
                                                             description=avatar_category1.description,
                                                             name='Baseball Cap', premium_price=1, currency_flag=2,
                                                             slots_layer=0,
                                                             display_order=2)
        AvatarItems.objects.create(category_id=avatar_category2.id,
                                                             description=avatar_category2.description,
                                                             name='Shirt', slots_layer=0,
                                                             coins_price=2, currency_flag=3, display_order=4)
        AvatarItems.objects.create(category_id=avatar_category3.id,
                                                             description=avatar_category3.description, slots_layer=0,
                                                             name='Boots', coins_price=3, currency_flag=3,
                                                             display_order=3)
        AvatarItems.objects.create(category_id=avatar_category4.id,
                                                             description=avatar_category4.description, slots_layer=0,
                                                             name='Fedora', premium_price=5, currency_flag=2,
                                                             display_order=5)
        AvatarItems.objects.create(category_id=avatar_category5.id,
                                                             description=avatar_category5.description, slots_layer=0,
                                                             name='T-shirt', premium_price=1, currency_flag=2,
                                                             display_order=7)
        AvatarItems.objects.create(category_id=avatar_category6.id,
                                                             description=avatar_category6.description, slots_layer=0,
                                                             name='Jeans', coins_price=2, currency_flag=3,
                                                             display_order=10)
        AvatarItems.objects.create(category_id=avatar_category7.id,
                                                             description=avatar_category7.description, slots_layer=0,
                                                             name='short cardigan', premium_price=2, currency_flag=2,
                                                             display_order=12)
        AvatarItems.objects.create(category_id=avatar_category8.id,
                                                             description=avatar_category8.description, slots_layer=0,
                                                             name='black hair', coins_price=3, currency_flag=3,
                                                             display_order=24)

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

        # item exchange rate
        ItemExchangeRate.objects.create(ticket_quantity=1, max=5, ticket=0, ticket_price=1, exchange_type=1)
        ItemExchangeRate.objects.create(ticket_quantity=1, max=5, ticket=1, ticket_price=1, exchange_type=2)
        ItemExchangeRate.objects.create(ticket_quantity=5, max=0, ticket=2, ticket_price=1, exchange_type=2)


        # User
        WUsers.objects.create(last_name='t_last1', first_name='t_user1', gender='Male', work=[],
                                                 email='t_user1@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=4, delete_flag=0,
                                                 phone_id='abcdefgh', closet=30, stamina_potion=10)

        WUsers.objects.create(last_name='t_last2', first_name='t_user2', gender='Male', work=[],
                                                 email='t_user2@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=20, ticket=5, delete_flag=0,
                                                 phone_id='12345678', closet=30, stamina_potion=10)

        WUsers.objects.create(last_name='t_last3', first_name='t_user3', gender='Male', work=[],
                                                 email='t_user2@test.com', birthday='08/21/1999', free_currency=1000,
                                                 premium_currency=0, ticket=1, delete_flag=0,
                                                 phone_id='98765432', closet=30, stamina_potion=0)

        user1 = WUsers.objects.filter(phone_id='abcdefgh')[0]


        # User Books
        UserBooks.objects.create(user_id=user1.id, book_list=[book1.id, book2.id])

        ShopItems.objects.create(product_id='com.voltage.ent.witch.001', price=4.99, premium_qty=5, name='Starstone Quintet')
        ShopItems.objects.create(product_id='com.voltage.ent.witch.101', price=4.99, premium_qty=5, name='Stamina Potion Batch')
        ShopItems.objects.create(product_id='com.voltage.ent.witch.201', price=2.99, premium_qty=0, name='Starter Pack',
                                 bundle_items={'Starstone': 1, 'Stamina': 3, 'Avatar': ["54da8ad76f983f60ee01f859", "54da8ad76f983f60ee01f85a"], 'Potion': ["54da8ad66f983f60ee01f7f3"]})

        # User Characters
        affinities_dict = {"A": 0, "M": 0, "N": 0, "R": 0, "T": 0}
        UserCharacters.objects.create(user_id=user1.id, affinities=affinities_dict)


    def test_iap_ios(self):
        receipt = new_receipt
        c = Client()

        param = {'phone_id':'abcdefgh', 'receipt': receipt, 'premium_id':'com.voltage.ent.witch.001', 'device_os': 'ios'}
        c.post('/witches/buy_inapp/1', param)
        user = WUsers.objects.get(phone_id='abcdefgh')
        self.assertEqual(user.premium_currency, 25, 'premium_currency should be 25 but got ' + str(user.premium_currency))

    def test_iap_bundle(self):
        receipt = old_receipt
        c = Client()

        param = {'phone_id':'abcdefgh', 'receipt': receipt, 'premium_id':'com.voltage.ent.witch.201', 'device_os': 'ios'}
        c.post('/witches/buy_inapp/1', param)
        user = WUsers.objects.get(phone_id='abcdefgh')
        avatar = UserAvatarItemsInCloset.objects.filter(user_id=user.id)
        userItem = UserItemInventory.objects.filter(user_id=user.id)
        self.assertEqual(user.premium_currency, 21, 'premium_currency should be 21 but got ' + str(user.premium_currency))
        self.assertEqual(user.stamina_potion, 13, 'stamina_potion should be 13 but got ' + str(user.stamina_potion))
        avatar_list = ["54da8ad76f983f60ee01f859", "54da8ad76f983f60ee01f85a"]
        self.assertTrue(avatar[0].avatar_item_id in avatar_list)

        self.assertEqual(userItem[0].potion_id, '54da8ad66f983f60ee01f7f3', '54da8ad66f983f60ee01f7f3 but got ' +
                         userItem[0].potion_id)

    def test_iap_ios2(self):
        # receipt = old_receipt
        receipt = temp_receipt
        c = Client()

        param = {'phone_id':'abcdefgh', 'receipt': receipt, 'premium_id':'com.voltage.ent.witch.101', 'device_os': 'ios'}
        c.post('/witches/buy_inapp/1', param)
        user = WUsers.objects.get(phone_id='abcdefgh')
        self.assertEqual(user.stamina_potion, 15, 'stamina potion should be 15 but got ' + str(user.stamina_potion))

    def test_iap_android(self):
        c = Client()
        receipt = android_receipt
        transaction_id = "GPA.1334-9182-9849-70173"
        param = {'phone_id':'abcdefgh', 'receipt': receipt, 'transaction_id': transaction_id,
                 'premium_id':'com.voltage.ent.witch.001', 'device_os': 'android'}
        c.post('/witches/buy_inapp/1', param)
        user = WUsers.objects.get(phone_id='abcdefgh')
        self.assertEqual(user.premium_currency, 25, 'user premium currency should be 25 but got '+ str(user.premium_currency))

    def test_iap_amazon_verify_receipt(self):
        receipt_data ='{"amazon_user_id":' + '"' + amazon_user_id + '"' + ', "receipt_id":' + '"' + amazon_receipt_id + '"' + '}'
        response, amazon_id = verify_amazon_receipt(receipt_data)
        str_response = json.dumps(response)
        self.assertTrue(str_response)
        self.assertTrue(amazon_id, amazon_user_id)

    def test_iap_amazon(self):
        c = Client()
        receipt = '{"amazon_user_id":' + '"' + amazon_user_id + '"' + ', "receipt_id":' + '"' + amazon_receipt_id + '"' + '}'
        param = {'phone_id':'abcdefgh', 'receipt': receipt, 'premium_id': 'com.voltage.ent.witch.201', 'device_os': 'amazon'}
        c.post('/witches/buy_inapp/1', param)
        user = WUsers.objects.get(phone_id='abcdefgh')
        payment = PaymentHistory.objects.get(user_id=user.id)
        self.assertEqual(payment.user_id, user.id, 'user id should be ' + user.id + ' but got ' + payment.user_id)
        self.assertEqual(payment.unique_identifier, amazon_user_id, 'amazon_user_id should be ' + amazon_user_id +
                         ' but got ' + payment.unique_identifier)

    def test_iap_android_old(self):
        c = Client()
        receipt = '{"json":"{\"orderId\":\"GPA.1350-7731-9572-43558\",\"packageName\":\"com.voltage.curse.en\",\"productId\":\"com.voltage.ent.witch.001\",\"purchaseTime\":1440017062276,\"purchaseState\":0,\"purchaseToken\":\"ndocppedpnlhcmcnelinmanl.AO-J1OwiM4tH9D0gmvqdCwql9h546gEMb4pxBxDoBxXBvBTKpV2G4HjA4uWLEt-0kfCAPPmBDIJ5fOCeQAa9GBqqR6PEKYVkAde87Z3I-AOaEKQyyXM1ISm-ad6QI-oHMArhQvQn3RuK\"}","developerPayload":"","signature":"I0\/UBnPiNdvalwp2v4cRxCeFW2aDUkUqDHC4tFVufK5UINYgWTHjtMlLrKbNKrTY9e+W2v2mupNtZotkQ38w8yTOfJwvPbKc0ILKpmf4QOo2sZDyJeKOKhHNwGnwKODx4zSq5yh2Gtzg+5n4\/xLCaslK+Te48Lb3XBTxiMsyxawCsevSmcvJtWCUER5FL3R2PKmhoDkTIUM0M5dzAeg11ocBnHgfXunpqBQSkjQkSszHgrzJW5HeVoOPJg2zG33NGlL7uoPKQABNbTT8kifR6Ucynek9LifQqNQyc1vKCYXw1wB0bdxAB935bMkRFF9ek2vIN0VpHQdNXSSMe7tVlA=="}'
        transaction_id = "GPA.1334-9182-9849-70173"

        param = {'phone_id':'abcdefgh', 'receipt': receipt, 'transaction_id': transaction_id,
                 'premium_id':'com.voltage.ent.witch.001', 'device_os': 'android'}
        c.post('/witches/buy_inapp/1', param)
        user = WUsers.objects.get(phone_id='abcdefgh')
        self.assertEqual(user.premium_currency, 25, 'user premium currency should be 25 but got '+ str(user.premium_currency))

    def test_buy_stamina(self):
        c = Client()

        param = {'phone_id': 'abcdefgh', 'ticket_type': const.stamina_ticket}
        c.post('/witches/buy_tickets/1', param)

        user = WUsers.objects.get(phone_id='abcdefgh')
        self.assertEqual(user.ticket, 5, 'ticket should be 5 but got ' + str(user.ticket))
        self.assertEqual(user.stamina_potion, 9, 'stamina potion should be 9 but got ' + str(user.stamina_potion))


    def test_buy_stamina_full_user(self):
        c = Client()

        param = {'phone_id': '12345678', 'ticket_type': const.stamina_ticket}
        c.post('/witches/buy_tickets/1', param)

        user = WUsers.objects.get(phone_id='12345678')
        self.assertEqual(user.ticket, 5, 'ticket should be 5 but got ' + str(user.ticket))
        self.assertEqual(user.stamina_potion, 10, 'stamina potion should be 10 but got ' + str(user.stamina_potion))


    def test_buy_stamina_no_currency(self):
        c = Client()

        param = {'phone_id': '98765432', 'ticket_type': const.stamina_ticket}
        c.post('/witches/buy_tickets/1', param)

        user = WUsers.objects.get(phone_id='98765432')
        self.assertEqual(user.ticket, 1, 'ticket should be 1 but got ' + str(user.ticket))
        self.assertEqual(user.stamina_potion, 0, 'stamina potion should be 0 but got ' + str(user.stamina_potion))

    def test_no_shop_item(self):
        receipt = new_receipt
        c = Client()
        param = {'phone_id':'abcdefgh', 'receipt': receipt, 'premium_id': 'com.voltage.ent.witch.301', 'device_os':
            'ios'}
        r = c.post('/witches/buy_inapp/1', param)
        self.assertTrue('Error' in r.content)


    def tearDown(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(name_or_database='UnitTest')

if __name__ == '__main__':
    unittest.main()
