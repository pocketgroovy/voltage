__author__ = 'carlos.matsumoto'

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_user, name='login'),
    url(r'^home/', views.home, name='home'),
    url(r'^register/', views.register, name='register'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^results/', views.results, name='results'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page':'/sales/login/'}),

)