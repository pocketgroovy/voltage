__author__ = 'yoshi.miyamoto'

from witches.models import *
from witches.utils.util import get_properties, throw_error, throw_error_in_json


def pick_up_items(user, item_id, received_mail, type_res, other, context):
     # check to see if the item has been received or not
    update_list = []
    try:
        # user_mail = UserMailBox.objects.get(id=ObjectId(mail_id), delete_flag=False)
        user_mail = received_mail
        for gift in user_mail.gifts:
            if gift['id'] == item_id:
                if gift['received_flag']:
                    Error = get_properties(err_type='Error', err_code='ERR0054')
                    res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                    if type_res == 0:
                        return throw_error(template="home.html", obj_dict=res_dict, context=context)
                    elif type_res == 1:
                        return throw_error_in_json(res_dict, user.phone_id)

    except UserMailBox.DoesNotExist:
        Error = get_properties(err_type='Error', err_code='ERR0017')
        res_dict = {'status': 'failed', 'function': other, 'Error': Error}
        if type_res == 0:
            return throw_error(template="home.html", obj_dict=res_dict, context=context)
        elif type_res == 1:
            return throw_error_in_json(res_dict, user.phone_id)

    try:
        AvatarItems.objects.get(id=item_id, delete_flag=False)
        for item in user_mail.gifts:
            if item['id'] == item_id:
                item['received_flag'] = True
            update_list.append(item)

        UserAvatarItemsInCloset.objects.create(user_id=user.id, avatar_item_id=item_id, quantity=1)
        user_mail.gifts = update_list
        user_mail.read_flag = True

    except AvatarItems.DoesNotExist:
        try:
            Potions.objects.get(id=item_id, delete_flag=False)
            for item in user_mail.gifts:
                if item['id'] == item_id:
                    item['received_flag'] = True
                update_list.append(item)

            UserItemInventory.objects.create(user_id=user.id, potion_id=item_id, quantity=1)
            user_mail.gifts = update_list
            user_mail.read_flag = True

        except Potions.DoesNotExist:
            try:
                Ingredients.objects.get(id=item_id, delete_flag=False)
                for item in user_mail.gifts:
                    if item['id'] == item_id:
                        item['received_flag'] = True
                    update_list.append(item)

                UserItemInventory.objects.create(user_id=user.id, ingredient_id=item_id, quantity=1)
                user_mail.gifts = update_list
                user_mail.read_flag = True

            except Ingredients.DoesNotExist:
                try:
                    ClothingCoordinates.objects.filter(id=item_id, delete_flag=False)
                    for item in user_mail.gifts:
                        if item['id'] == item_id:
                            item['received_flag'] = True
                        update_list.append(item)

                    UserItemInventory.objects.create(user_id=user.id, ingredient_id=item_id, quantity=1)
                    user_mail.gifts = update_list
                    user_mail.read_flag = True

                except ClothingCoordinates.DoesNotExist:
                    Error = get_properties(err_type='Error', err_code='ERR0014')
                    res_dict = {'status': 'failed', 'function': other, 'Error': Error}
                    if type_res == 0:
                        return throw_error(template="home.html", obj_dict=res_dict, context=context)
                    elif type_res == 1:
                        return throw_error_in_json(res_dict, user.phone_id)
