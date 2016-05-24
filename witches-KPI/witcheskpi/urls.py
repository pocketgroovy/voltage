__author__ = 'carlos.matsumoto'

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',

    url(r'^$', views.home, name='home'),
    url(r'^kpi/', views.kpi, name='kpi'),


)