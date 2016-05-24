from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
                       url(r'^witches/', include('witches.urls_historical', namespace='witches')),
                       url(r'^facebook/', include('django_facebook.urls')),

                       url('', include('social.apps.django_app.urls', namespace='social')),
                       url('', include('django.contrib.auth.urls', namespace='auth')),
)
