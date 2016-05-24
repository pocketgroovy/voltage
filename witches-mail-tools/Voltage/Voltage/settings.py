# Django settings for Voltage project.
import os
import sys

from Voltage.witch_mail_config import get_environment

ENVIRONMENT = get_environment('Env', 'environment')
print ("Server Environment: " + ENVIRONMENT)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine',
        'NAME': 'witches',
        'USER': '',
        'PASSWORD': '',
        'HOST': get_environment(ENVIRONMENT, 'db_primary_host'),
        'PORT': '27017'
    }
}

import os
CFG_FILE = os.path.join(os.path.dirname(__file__), '../witches/utils/witches.cfg').replace('\\', '/')

# SETTINGS_DIR = os.path.dirname(__file__)
#
# PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
# PROJECT_PATH = os.path.abspath(PROJECT_PATH)

# TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = u'54493437fd29b00db507de34'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/Users/yoshi.miyamoto/PycharmProjects/VoltageTool/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

ASSET_BUNDLE_ROOT = '/Users/yoshi.miyamoto/witches-server/Voltage/asset_bundles/'
# STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '..', 'static').replace('\\','/'),
)


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '../templates').replace('\\', '/'),
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'nwksfswfe1)x5_+n9*j0+ez_*j55h=2!&#7qisoyi=qyw2dl6('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'Voltage.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Voltage.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.me',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'facebook',
    'witches',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Authentication
# witches_test1
#SOCIAL_AUTH_FACEBOOK_KEY = '1483116655261771'
#SOCIAL_AUTH_FACEBOOK_SECRET = '44bfdab16905e146427bd515de8ff738'
#SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'en_US'}

# witchestest
SOCIAL_AUTH_FACEBOOK_KEY = '1483115788595191'
SOCIAL_AUTH_FACEBOOK_SECRET = '10f345a53b237b8cc2f20e21f70375d8'
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'en_US'}


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '827476067692-libn34e5pfj8ufn4jdl2vm93jdkf49ob.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'K5s15N8cQWx6ZXbbAF7vbvuj'

SOCIAL_AUTH_TWITTER_KEY = 'k9kswqOgyQFTJx5jofygOlPFa'
SOCIAL_AUTH_TWITTER_SECRET = 'ylg59tCOl0uukY7gnjMMOFK3hxB6KsXv5ryaMLoRW0q06oIbLV'


# Facebook API related Settings
FACEBOOK_APP_ID = '1483116655261771'
FACEBOOK_SECRET_KEY = '44bfdab16905e146427bd515de8ff738'
FACEBOOK_REDIRECT_URL = 'http://carloslocal.com:8000/witches/facebook_login_success'


# Receipt Verification apple sandbox
SANDBOX_URL_APPLE = 'https://sandbox.itunes.apple.com/verifyReceipt'
LIVE_URL_APPLE = 'https://buy.itunes.apple.com/verifyReceipt'
APPLE_TEST_USER = 'yoshi.miyamoto+8@voltage-ent.com'
APPLE_TEST_PASSWORD = 'Voltage123'


# Receipt Verification amazon sandbox
AMAZON_USER_ID = '99FD_DL23EMhrOGDnur9-ulvqomrSg6qyLPSD3CFE='
AMAZON_DEVELOPER_SECRET = 'developerSecret'
AMAZON_URL_SANDBOX = 'http://localhost:8080/RVSSandbox/version/1.0/verifyReceiptId/developer/' + \
                     AMAZON_DEVELOPER_SECRET + '/user/' + AMAZON_USER_ID + '/receiptId/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': [],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.dirname(__file__), '../log/witches.log'),
            'formatter': 'verbose'
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'witches': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
