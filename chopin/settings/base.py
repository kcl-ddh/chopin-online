"""
Django settings for hp project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/

For production settings see
https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

PROJECT_NAME = 'chopin'
PROJECT_TITLE = 'Chopin Online'

SITE_TITLE = {
    'aco': 'Annotated Catalogue Online',
    'cfeo': 'Chopin\'s First Editions Online',
    'ocve': 'Online Chopin Variorum Edition'
}

#------------------------------------------------------------------------------
# Core Settings
# https://docs.djangoproject.com/en/1.6/ref/settings/#id6
#------------------------------------------------------------------------------

ADMINS = (
    ('Miguel Vieira', 'jose.m.vieira@kcl.ac.uk'),
)
MANAGERS = ADMINS

ALLOWED_HOSTS = []

# https://docs.djangoproject.com/en/1.6/ref/settings/#caches
# https://docs.djangoproject.com/en/dev/topics/cache/
# http://redis.io/topics/lru-cache
# http://niwibe.github.io/django-redis/
CACHE_REDIS_DATABASE = '0'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:' + CACHE_REDIS_DATABASE,
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True
        }
    }
}

# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
}

DATABASE_ROUTERS = ['chopin.dbrouter.ChopinOnlineRouter']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'compressor',
    'haystack',
    'modelcluster',
    'taggit',
    'tinymce',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailredirects',
)

INSTALLED_APPS += (
    'catalogue',
    'chopin',
    'ocve',
)

INTERNAL_IPS = ('127.0.0.1', )

# https://docs.djangoproject.com/en/1.6/topics/logging/
import logging

LOGGING_ROOT = os.path.join(BASE_DIR, 'logs')
LOGGING_LEVEL = logging.WARN

if not os.path.exists(LOGGING_ROOT):
    os.makedirs(LOGGING_ROOT)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(module)s '
                       '%(process)d %(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
        'django_auth_ldap': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
        'catalogue': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
        'elasticsearch': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
    }
}


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = PROJECT_NAME + '.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'catalogue.context_processors.settings',
    'ocve.context_processors.ocve_constants',
)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'), )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = False
USE_TZ = True

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'


#------------------------------------------------------------------------------
# Authentication
# https://docs.djangoproject.com/en/1.6/ref/settings/#auth
# https://scm.cch.kcl.ac.uk/hg/ddhldap-django
#------------------------------------------------------------------------------

from ddhldap.settings import *

AUTH_LDAP_REQUIRE_GROUP = 'cn=ocve,' + LDAP_BASE_OU

LOGIN_URL = 'wagtailadmin_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'


#------------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# https://docs.djangoproject.com/en/1.6/ref/settings/#static-files
#------------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip('/'))

if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',

    'compressor.finders.CompressorFinder',
)

MEDIA_URL = STATIC_URL + 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL.strip('/'))

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)


#------------------------------------------------------------------------------
# Installed Applications Settings
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Catalogue
#------------------------------------------------------------------------------

AC_ENCODING = 'UTF-8'

CFEO_BASE_URL = '/cfeo/ui/acview/'
OCVE_BASE_URL = '/ocve/ui/acview/'

WORKS_WITHOUT_OPUS = ['GDC', 'HEX', 'MEG', 'MFM', 'MazG&Bflat', 'PolGm', 'MM',
                      'VGNA']
POSTHUMOUS_WORKS_WITH_OPUS = 66
POSTHUMOUS_WORKS_WITHOUT_OPUS = ['MazC', 'MazD, Bflat, G, Lento', 'PolGflat',
                                 'PolGsharpm', 'WaltzE', 'WaltzEm']
ALL_WORKS_WITHOUT_OPUS = WORKS_WITHOUT_OPUS + POSTHUMOUS_WORKS_WITHOUT_OPUS


#------------------------------------------------------------------------------
# CMS
#------------------------------------------------------------------------------

ITEMS_PER_PAGE = 10
ALLOW_COMMENTS = True
DISQUS_SHORTNAME = None

#------------------------------------------------------------------------------
# Django Compressor
# http://django-compressor.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

#------------------------------------------------------------------------------
# Django Grappelli
# http://django-grappelli.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

GRAPPELLI_ADMIN_TITLE = PROJECT_TITLE

#------------------------------------------------------------------------------
# Django Haystack
# http://django-haystack.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE':
        'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': PROJECT_NAME,
        'TIMEOUT': 60 * 5,
        'BATCH_SIZE': 10,
    }
}

HAYSTACK_LIMIT_TO_REGISTERED_MODELS = False

# -----------------------------------------------------------------------------
# FABRIC
# -----------------------------------------------------------------------------

import getpass
FABRIC_USER = getpass.getuser()

# -----------------------------------------------------------------------------
# IIP
# -----------------------------------------------------------------------------

IIP_URL = '/iip/iipsrv.fcgi'
IMAGE_SERVER_URL = IIP_URL

# -----------------------------------------------------------------------------
# OCVE
# -----------------------------------------------------------------------------

SOURCEJSONPATH = os.path.join(STATIC_ROOT, 'javascripts')

IMAGE_UPLOAD_PATH = '/vol/ocve2/images/upload/'
CONVERTED_UPLOAD_PATH = '/vol/ocve2/images/temp/'
NEWJP2_UPLOAD_PATH = '/vol/ocve2/images/jp2/newjp2/'
UPLOAD_EXTENSION = '.tif'

# The width of the image when extracting bar region thumbnails in iip
THUMBNAIL_WIDTH = 500

# -----------------------------------------------------------------------------
# Registration
# -----------------------------------------------------------------------------

ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_HOST = 'smtp.cch.kcl.ac.uk'
EMAIL_PORT = 25

# -----------------------------------------------------------------------------
# TinyMCE
# -----------------------------------------------------------------------------

TINYMCE_DEFAULT_CONFIG = {
    'mode': 'textareas',
    'plugins': 'paste,searchreplace,xhtmlxtras',
    'theme': 'advanced',
    'theme_advanced_buttons1': 'bold,italic,sup,sub,undo,redo',
    'theme_advanced_buttons2': '',
    'theme_advanced_buttons3': '',
    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_statusbar_location': 'bottom',
    'theme_advanced_resizing': True,
}

#------------------------------------------------------------------------------
# Wagtail
# http://wagtail.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

WAGTAIL_SITE_NAME = PROJECT_TITLE
