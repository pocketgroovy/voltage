from django.db import models
from djangotoolbox.fields import DictField, ListField
from django_mongodb_engine.contrib import MongoDBManager
from Voltage.settings import MEDIA_ROOT


class Loadfile(models.Model):
    masterload = models.FileField(upload_to=MEDIA_ROOT)

    class Meta:
        db_table = 'Loadfile'




class EmailTemplates(models.Model):
    sender_id = models.CharField(max_length=30, null=False)
    attach_list = ListField(null=True, blank=True)
    premium_currency = models.CharField(max_length=5, null=True)
    free_currency = models.CharField(max_length=5, null=True)
    stamina_potion = models.CharField(max_length=5, null=True)
    body_text = models.TextField()
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'EmailTemplates'


class Affinities(models.Model):
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)
    total_affinity = models.IntegerField()
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'Affinities'


class Characters(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    shorter = models.CharField(max_length=30)
    initial = models.CharField(max_length=1, null=True)
    romanceable = models.BooleanField(default=False)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'Characters'


class Books(models.Model):
    name = models.CharField(max_length=50)
    display_order = models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    book_prize_id = models.CharField(max_length=30)
    recipes = ListField()  # recipe_id, success_threshold
    mail_id = models.CharField(max_length=50)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'Books'


class BookPrizes(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=100)  # starstone, avatar, potion
    reward_id = models.CharField(max_length=30, null=True)  # starstone=null, potion_id, avatar_item_id
    quantity = models.IntegerField()
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'BooksPrizes'


class Recipes(models.Model):
    name = models.CharField(max_length=50)
    hint = models.TextField()
    display_order = models.IntegerField(default=0)
    replay_flag = models.BooleanField()
    ingredient_list = ListField()  # ingredient_id
    score_list = DictField()    #  {low : float , mid : float, high : float}
    prize_list = DictField()    # low, item_id  mid, item_id  high, item_id
    potion_list = DictField()   # low, potion_id  mid, potion_id   high, potion_id
    game_duration = models.IntegerField()   # seconds
    continue_duration = models.IntegerField()   # seconds
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'Recipes'


class Potions(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    type = models.IntegerField()
    display_order = models.IntegerField(default=0)
    color = models.CharField(max_length=12) # Color according to the levels
    icon_name = models.CharField(max_length=50)
    effect_list = ListField()   # [{character_id, effect_value}]
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'Potions'


class Ingredients(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category_id = models.CharField(max_length=30)  # category_id
    display_order = models.IntegerField(default=0)
    quality = models.IntegerField()
    effect_list = DictField(models.FloatField(default=0.0)) # stroke_abs, stroke_rel, affinity_abs, affinity_rel
    isInfinite = models.BooleanField()
    bottle_bg = models.IntegerField(default=0)
    color = models.CharField(max_length=10)
    coins_price = models.IntegerField(default=0)
    premium_price = models.IntegerField(default=0)
    currency_flag = models.IntegerField(default=0)  # 0->not for sale 1->premium_currency  2->coins  3->both
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'Ingredients'


class Categories(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # ingredients = 0, Avatar items = 1, Glossary = 2
    color = models.CharField(max_length=10)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'Categories'


class PaymentHistory(models.Model):
    user_id = models.CharField(max_length=30, null=False)  # user_id
    store_product_id = models.CharField(max_length=50)  # product name
    store_item_id = models.CharField(max_length=50)  # store item_id
    quantity = models.IntegerField()  # number of items
    shop_type = models.CharField(max_length=30, null=False)  # apple, google, app
    original_transaction_id = models.CharField(max_length=50)  # original transaction_id
    transaction_id = models.CharField(max_length=50)  # transaction_id
    unique_identifier = models.CharField(max_length=50)  # unique id
    unique_vendor_identifier = models.CharField(max_length=50)  # vendor id
    original_purchase_date_pst = models.DateTimeField()  # original purchase date in pt
    purchase_date_pst = models.DateTimeField()  # purchase date in pt
    original_purchase_date = models.DateTimeField()  # original purchase date
    purchase_date = models.DateTimeField()  # purchase date
    cancel_date = models.CharField(max_length=100, null=True)  # cancel date
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'PaymentHistory'


class GameProperties(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    event_flag = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'GameProperties'


class ClothingCoordinates(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    item_list = ListField()
    coins_price = models.IntegerField(default=0)
    premium_price = models.IntegerField(default=0)
    currency_flag = models.IntegerField()   # 0->not for sale 1->premium_currency  2->coins  3->both
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'ClothingCoordinates'


class AvatarItems(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    layer_name = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=30, null=False)
    category_id = models.CharField(max_length=30, null=False)
    display_order = models.IntegerField()
    slots_layer = models.IntegerField()
    coins_price = models.IntegerField(default=0)
    premium_price = models.IntegerField(default=0)
    currency_flag = models.IntegerField()   # 0->not for sale 1->premium_currency  2->coins  3->both
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'AvatarItems'


class EI(models.Model):
    name = models.CharField(max_length=30, null=False)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'EI'


class ShopItems(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    item_index = models.IntegerField(default=0)
    product_id = models.CharField(max_length=50)
    premium_qty = models.IntegerField(default=0)
    bundle_items = DictField()
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'ShopItems'


class Glossary(models.Model):
    name = models.CharField(max_length=50)
    category_id = models.CharField(max_length=30)
    display_order = models.IntegerField()
    body_text = models.TextField()
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'Glossary'


class Games(models.Model):
    name = models.CharField(max_length=50)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)
    objects = MongoDBManager()


class LogInBonusesMaster(models.Model):
    bonus_index = models.IntegerField(default=0)
    bonus_id = models.CharField(max_length=30)
    quantity = models.IntegerField()
    bonus_description = models.CharField(max_length=255)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'LogInBonusesMaster'


class VariableLogInBonuses(models.Model):
    login_cycle = models.PositiveSmallIntegerField()
    cumulative = models.IntegerField()
    reward_id = models.CharField(max_length=30, null=False)
    type = models.CharField(max_length=30, null=False)
    quantity = models.IntegerField()
    bonus_description = models.CharField(max_length=255)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'VariableLogInBonuses'


# class LogIn(models.Model):
#     user_id = models.CharField(max_length=30, null=False)
#     login_cycle = models.PositiveSmallIntegerField()
#     cumulative = models.IntegerField()
#     consecutive = models.IntegerField()
#     delete_flag = models.BooleanField(default=False)
#     install_date = models.DateTimeField(auto_now_add=True, editable=False)
#     last_updated = models.DateTimeField(auto_now=True)
#
#     objects = MongoDBManager()
#
#     class Meta:
#         db_table = 'LogIn'

class ItemExchangeRate(models.Model):
    ticket = models.IntegerField()  # 0:stamina 1:focus 2:closet
    ticket_quantity = models.IntegerField()
    ticket_price = models.IntegerField()  # the number of stamina potion or stone spent
    exchange_type = models.IntegerField()  # 1: stamina potion 2: premium_currency(startstone)
    max = models.IntegerField(null=True)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'ItemExchangeRate'


class SceneTable(models.Model):
    scene_path = models.CharField(max_length=100)
    EI_id = models.CharField(max_length=30, null=True, blank=True)
    mail_template_id = models.CharField(max_length=30, null=True, blank=True)
    book_id = models.CharField(max_length=30, null=True, blank=True)
    stamina_deduction_flag = models.BooleanField(default=False)
    regeneration_flag = models.BooleanField(default=False)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'SceneTable'


class Environment(models.Model):
    description = models.CharField(max_length=10, null=False)
    build_version = models.CharField(max_length=10, null=False)
    base_url = models.CharField(max_length=100, null=False)
    metrics = DictField()
    device = models.CharField(max_length=30, null=False)
    obb_path = models.CharField(max_length=30, blank=True)
    current_api = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'Environment'


class PaymentHistoryError(models.Model):
    error_message = models.CharField(max_length=256, null=True, blank=True)
    phone_id = models.CharField(max_length=30, null=True, blank=True)
    item_id = models.CharField(max_length=30, null=True, blank=True)
    receipt = models.CharField(max_length=256, null=True, blank=True)
    device_os = models.CharField(max_length=64, null=True, blank=True)
    error_date = models.DateTimeField(auto_now_add=True, editable=False)

    objects = MongoDBManager()

    class Meta:
        db_table = 'PaymentHistoryError'


class WUsers(models.Model):

    phone_id = models.CharField(max_length=50)  # randomly created 8 digits number
    sns_id = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    work = ListField(null=True, blank=True)
    email_fb = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    password_date = models.DateTimeField(null=True)
    birthday = models.CharField(max_length=10, null=True, blank=True)
    score = models.FloatField(default=0.0)
    free_currency = models.IntegerField(default=0)
    premium_currency = models.IntegerField(default=0)
    total_affinity = models.IntegerField(default=0)
    light_dark = models.CharField(max_length=1)
    ticket = models.IntegerField(default=0)  # stamina
    ticket_last_update = models.DateTimeField(auto_now=False, blank=True, null=True)
    stamina_potion = models.IntegerField(default=0)
    closet = models.IntegerField()
    current_outfit = ListField()
    scene_id = models.CharField(max_length=50, blank=True)
    howtos_scene_id = models.CharField(max_length=50, blank=True)
    tutorial_progress = models.IntegerField(default=0)
    node_id = models.CharField(max_length=50, blank=True)
    route_version = models.CharField(max_length=50, blank=True)
    current_book_id = models.CharField(max_length=50)
    facebook_flag = models.BooleanField(default=False)
    login_date = models.DateTimeField(null=True)
    device = models.CharField(max_length=30, null=True, blank=True)
    current_outfit = ListField()
    login_bonus_items = ListField()
    next_login_bonus_index = models.IntegerField(default=0)
    last_login_bonus_date = models.DateTimeField(null=True)
    tutorial_flag = models.BooleanField(default=True)
    affinity_update = DictField()
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    # added to resolve production user's who can't login
    # since admin/dev share the same model saves to WUsers on any other database will conform to the dev model
    focus = models.IntegerField(default=0)
    focus_last_update = models.DateTimeField(auto_now=False, blank=True, null=True)

    unrecovered = models.BooleanField(default=False)
    update_client = models.BooleanField(default=False)

    objects = MongoDBManager()

    class Meta:
        db_table = 'WUsers'


class AbstractUserJson(models.Model):
    phone_id = models.CharField(max_length=30)
    playerjson = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        abstract = True

class UserPlayerJson(AbstractUserJson):

    class Meta:
        db_table = 'UserPlayerJson'

class UserClientUpdateJson(AbstractUserJson):

    class Meta:
        db_table = 'UserClientUpdateJson'


class UserItemInventory(models.Model):
    user_id = models.CharField(max_length=30)  # user_id
    ingredient_id = models.CharField(max_length=30)  # ingredient_id
    potion_id = models.CharField(max_length=30)  # potion_id
    quantity = models.IntegerField()
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserItemInventory'


class UserAvatarItemsInCloset(models.Model):
    user_id = models.CharField(max_length=30)  # user_id
    avatar_item_id = models.CharField(max_length=30, null=True, blank=True)  # Avatar_item_id
    coordinate_item_id = models.CharField(max_length=30, null=True, blank=True)  # Clothing Coordination item ID
    quantity = models.IntegerField()
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserAvatarItemsInCloset'


class UserBooks(models.Model):
    user_id = models.CharField(max_length=30, null=False)  # user_id
    book_list = ListField()  # book list
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserBooks'


class UserCompleteRecipes(models.Model):
    user_id = models.CharField(max_length=30, null=False)  # user_id
    recipe_id = models.CharField(max_length=30, null=False)  # recipe_id
    level = models.IntegerField()  # 0-no stars, 1-one star, 2-two stars, 3-three stars
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserCompleteRecipes'


class UserClothingCoordination(models.Model):
    user_id = models.CharField(max_length=30, null=False)  # user_id
    coordinate_list = ListField()
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserClothingCoordination'


class UserItemRemovalHistory(models.Model):
    user_id = models.CharField(max_length=30, null=False)  # user_id
    coordinate_item_id = models.CharField(max_length=30, null=True, blank=True)  # Clothing Coordination item ID
    avatar_item_id = models.CharField(max_length=30, null=True, blank=True)  # Avatar_item_id
    removal_status = models.IntegerField()  # 0:coordination removed 1:only items removed
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserItemRemovalHistory'


class UserMailBox(models.Model):
    user_id = models.CharField(max_length=30, null=False)
    gifts = ListField(null=True)
    EI = models.CharField(max_length=30, null=True)
    premium_currency = models.IntegerField(null=True, blank=True)
    free_currency = models.IntegerField(null=True, blank=True)
    stamina_potion = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=30, null=False)
    message_body = models.CharField(max_length=30, null=False)
    sender_id = models.CharField(max_length=30, null=False)
    sender_flag = models.BooleanField(default=False)  # True == Character, False == System
    read_flag = models.BooleanField(default=False)
    premium_received_flag = models.BooleanField(default=False)
    free_currency_received_flag = models.BooleanField(default=False)
    stamina_potion_received_flag = models.BooleanField(default=False)
    login_bonus_id = models.CharField(max_length=30, null=False)
    sender_type_for_metrics = models.CharField(max_length=10, null=False)
    multiply_bonus_flag = models.BooleanField(default=False)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserMailBox'


class UserChapterTable(models.Model):
    user_id = models.CharField(max_length=30, null=False)
    chapter_id = models.CharField(max_length=30, null=False)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserChapterTable'


class UserCharacters(models.Model):
    user_id = models.CharField(max_length=30, null=False)
    affinities = DictField()  # Character Initial : Affinity Value
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserCharacters'


class UserCompletedScenes(models.Model):
    user_id = models.CharField(max_length=30, null=False)
    scene_id = models.CharField(max_length=30, null=False)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserCompletedScenes'


class UserLoginHistory(models.Model):
    phone_id = models.CharField(max_length=30, null=False)
    device = models.CharField(max_length=30, null=True, blank=True)
    delete_flag = models.BooleanField(default=False)
    install_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'UserLoginHistory'


class ErrorLog(models.Model):
    phone_id = models.CharField(max_length=30, null=False)
    build_version = models.CharField(max_length=30, null=False)
    playerjson = models.TextField()
    error_msg = models.CharField(max_length=256, null=False)
    stacktrace = models.TextField()

    device_id = models.CharField(max_length=64, null=True, blank=True)
    device_model = models.CharField(max_length=64, null=True, blank=True)
    device_os = models.CharField(max_length=64, null=True, blank=True)
    device_system_mem = models.IntegerField()
    device_graphics_mem = models.IntegerField()
    
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    objects = MongoDBManager()
    class Meta:
        db_table = "ErrorLog"



class LittleMonths:
    def __init__(self):
        pass

    Feb = 2
    Apr = 4
    Jun = 6
    Sep = 9
    Nov = 11

    def __contains__(self, item):
        if item == self.Feb:
            return True
        if item == self.Apr:
            return True
        if item == self.Jun:
            return True
        if item == self.Sep:
            return True
        if item == self.Nov:
            return True
