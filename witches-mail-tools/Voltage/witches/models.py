from django.db import models
from djangotoolbox.fields import DictField, ListField
from django_mongodb_engine.contrib import MongoDBManager


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

    unrecovered = models.BooleanField(default=False)
    update_client = models.BooleanField(default=False)

    objects = MongoDBManager()

    class Meta:
        db_table = 'WUsers'


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
