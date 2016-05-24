__author__ = 'carlos.matsumoto'

from django.http import HttpResponse
from django.core import serializers
from witches.models import WUsers, GameProperties
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from social.apps.django_app.default.models import UserSocialAuth

import facebook

import logging

logger = logging.getLogger(__name__)


def facebook_graph_login(request):
    response = HttpResponse()
    user = request.user
    social_auth = UserSocialAuth.objects.get(user=user, provider='facebook')
    token = social_auth.tokens
    graph = facebook.GraphAPI(token)
    if graph:
        profile = graph.get_object('me')
        friends = graph.get_connections("me", "friends")


    if profile and request.session.get('phone_id', None):
        user_me = WUsers.objects.filter(phone_id=request.session['phone_id'], delete_flag=False)
        if len(user_me) <= 0:
            default_free_currency = GameProperties.objects.filter(name='default_free_currency')[0]
            default_premium_currency = GameProperties.objects.filter(name='default_premium_currency')[0]
            default_ticket = GameProperties.objects.filter(name='default_ticket')[0]

            work_list = []
            # getting work list
            for work in profile.get('work'):
                json = ''
                if hasattr(work, 'employer'):
                    json += "{'employer':" + work.employer.name
                else:
                    continue
                if hasattr(work, 'position'):
                    json += ", 'position':" + work.position.name
                if hasattr(work, 'location'):
                    json += ", 'location':" + work.location.name

                json += "}"
                work_list.append(json)

            logger.debug("storing user data in mongo")
            WUsers.objects.create(sns_id=profile.get('id'), phone_id=request.session['phone_id'],
                                  last_name=profile.get('last_name'),
                                  name=profile.get('first_name'),
                                  gender=profile.get('gender'), work=work_list, email=profile.get('email'),
                                  birthday=profile.get('birthday'),
                                  free_currency=default_free_currency.value,
                                  premium_currency=default_premium_currency.value,
                                  ticket=default_ticket.value, facebook_flag=1, delete_flag=False)
            phone_id = request.session['phone_id']
            # DevicesInfo.objects.filter(phone_id=phone_id).update(sns_id=profile.get('id'))
            user_me = WUsers.objects.filter(phone_id=request.session['phone_id'], delete_flag=False)
            user_me = serializers.serialize('json', user_me)
        else:
            work_list = []
            # getting work list
            for work in profile.get('work'):
                json = ''
                if hasattr(work, 'employer'):
                    json += "{'employer':" + work.employer.name
                else:
                    continue
                if hasattr(work, 'position'):
                    json += ", 'position':" + work.position.name
                if hasattr(work, 'location'):
                    json += ", 'location':" + work.location.name

                json += "}"
                work_list.append(json)
            WUsers.objects.filter(phone_id=request.session['phone_id']).update(sns_id=profile.get('id'),
                                                                              last_name=profile.get('last_name'),
                                                                              name=profile.get('first_name'),
                                                                              gender=profile.get('gender'),
                                                                              work=work_list,
                                                                              email=profile.get('email'),
                                                                              birthday=profile.get('birthday'),
                                                                              facebook_flag=1, delete_flag=False)
            # DevicesInfo.objects.filter(phone_id=request.session['phone_id']).update(sns_id=profile.get('id'))
            user_me = WUsers.objects.filter(phone_id=request.session['phone_id'], delete_flag=False)
            user_me = serializers.serialize('json', user_me)

        logger.debug("there you go!!! user " + profile.get('first_name') + ' ' + profile.get('last_name'))
        welcome = "Welcome <b>%s</b>. Your Facebook login has been completed successfully!!"
        response.write(welcome % profile.get('name'))
        request.session['user_me'] = user_me
        response.write('friends : ' + str(len(friends)))
        context = RequestContext(request, {request: request, 'user': request.user})
    return render_to_response('home.html', context_instance=context)
