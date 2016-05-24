
__author__ = 'yoshi.miyamoto'

from witcheskpi.models import WUsers, UserLoginHistory, PaymentHistory


def get_installed_users(startDate, endDate, device_type):
    if device_type == 'ALL':
        installed_users = WUsers.objects.filter(install_date__gte=startDate, install_date__lte=endDate, delete_flag=False)
    else:
        installed_users = WUsers.objects.filter(install_date__gte=startDate, install_date__lte=endDate, device=device_type,
                                                delete_flag=False)
    return installed_users


def get_unique_users(startDate, endDate, device_type):
    if device_type == 'ALL':
        unique_login_users = UserLoginHistory.objects.filter(install_date__gte=startDate, install_date__lte=endDate, delete_flag=False).distinct('phone_id')
    else:
        unique_login_users = UserLoginHistory.objects.filter(install_date__gte=startDate, install_date__lte=endDate, device=device_type,
                                                       delete_flag=False).distinct('phone_id')

    installed_users = get_installed_users(startDate, endDate, device_type)

    unique_users = get_unique_users_include_installed_users(installed_users, unique_login_users)

    return unique_users


def get_purchased_unique_users(startDate, endDate, shop_type):
    if shop_type == 'ALL':
        purchased_unique_users = PaymentHistory.objects.filter(original_purchase_date__gte=startDate,
                                                               original_purchase_date__lte=endDate, delete_flag=False).distinct('user_id')
    else:
        purchased_unique_users = PaymentHistory.objects.filter(original_purchase_date__gte=startDate, shop_type=shop_type,
                                                               original_purchase_date__lte=endDate, delete_flag=False).distinct('user_id')
    return purchased_unique_users


def get_unique_users_include_installed_users(installed_users, unique_login_users):
    unique_users = unique_login_users

    for user in installed_users:
        if user.phone_id not in unique_login_users:
            unique_users.append(user.phone_id)

    return unique_users
