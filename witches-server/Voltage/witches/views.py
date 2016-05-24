__author__ = 'carlos.matsumoto', 'yoshi.miyamoto'

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from pymongo.errors import ConnectionFailure
from witches.user import get_playerstate
import datetime
import logging
import const
from witches.utils.util import throw_error_in_json, get_now_datetime

from user_functions import create_user_routine

const.user_length = 8

logger = logging.getLogger(__name__)


def home(request):
    other = 'environment'
    logger.debug("accessing to witches!!")
    context = RequestContext(request, {request: request, 'user': request.user, 'option': 'environment',
                                           'action': other, 'type_res': 0})
    try:
        return render_to_response('home.html', context_instance=context)
    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, '')

@csrf_exempt
def create_user(request, type_res):
    other = 'create_user'
    if type_res:
        type_res = int(type_res)
    else:
        type_res = 0

    try:
        user = create_user_routine()

        logger.debug("Welcome New User! your new user ID is [" + user.phone_id + "]")

        request.user = user
        
    except ConnectionFailure as e:
        res_dict = {'status': 'maintenance', 'function': other, 'Error': str(e)}
        return throw_error_in_json(res_dict, 'maintenance')

    request.session['phone_id'] = user.phone_id
    request.POST = request.POST.copy()

    request.POST['phone_id'] = user.phone_id
    return get_playerstate(request=request, type_res=type_res, extra_parms={'notificationsEnabled': False})


def is_password_expired(user):
    if user.password:
        now = get_now_datetime()
        date_one_week_before = now - datetime.timedelta(days=7)
        if user.password_date < date_one_week_before:
            logger.debug('the password is expired')
            return True
        return False
    else:
        logger.debug('no password has been set')


def logout(request):
    if request.session.get('phone_id', None):
        request.session.delete('phone_id')
        request.session.flush()
    return home(request)
