from django.conf.urls import patterns, include, url
from django.contrib import admin
from witches.admintool import adm_views

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^witches/admintool/$', adm_views.home, name='home'),
                       url(r'^witches/admintooldeliver/', adm_views.deliver_window, name='deliver_window'),
                       url(r'^witches/admintool/deliver/', adm_views.deliver, name='deliver'),

                       )
