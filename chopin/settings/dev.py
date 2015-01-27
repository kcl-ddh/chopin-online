from base import *

DEBUG = True

CACHE_REDIS_DATABASE = '2'
CACHES['default']['LOCATION'] = '127.0.0.1:6379:' + CACHE_REDIS_DATABASE

INTERNAL_IPS = ('ocve3-aco-dev.cch.kcl.ac.uk', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_ocve_aco_dev',
        'USER': 'app_ocve',
        'PASSWORD': '',
        'HOST': 'db-pg-1.cch.kcl.ac.uk'
    },
    'ocve_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ocve2real_dev',
        'USER': 'app_ocve2',
        'PASSWORD': '',
        'HOST': 'my-dev-1.cch.kcl.ac.uk',
    }
}

LOGGING_LEVEL = logging.DEBUG

LOGGING['loggers']['django_auth_ldap']['level'] = LOGGING_LEVEL
LOGGING['loggers']['catalogue']['level'] = LOGGING_LEVEL

HAYSTACK_CONNECTIONS['default']['INDEX_NAME'] = PROJECT_NAME + '_dev'

TEMPLATE_DEBUG = True

#------------------------------------------------------------------------------
# Django Extensions
# http://django-extensions.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

try:
    import django_extensions

    INSTALLED_APPS = INSTALLED_APPS + ('django_extensions',)
except ImportError:
    pass

#------------------------------------------------------------------------------
# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

try:
    import debug_toolbar

    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_PATCH_SETTINGS = True
except ImportError:
    pass

#------------------------------------------------------------------------------
# Local settings
#------------------------------------------------------------------------------

try:
    from local import *
except ImportError:
    print('failed to import local settings')
    raise ImportError('Error importing local settings')
