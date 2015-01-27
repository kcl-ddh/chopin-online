from base import *

CACHE_REDIS_DATABASE = '1'
CACHES['default']['LOCATION'] = '127.0.0.1:6379:' + CACHE_REDIS_DATABASE

INTERNAL_IPS = ('ocve3-aco-stg.cch.kcl.ac.uk', )
ALLOWED_HOSTS = ['ocve3-aco-stg.cch.kcl.ac.uk']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_ocve_aco_stg',
        'USER': 'app_ocve',
        'PASSWORD': '',
        'HOST': 'db-pg-1.cch.kcl.ac.uk'
    },
    'ocve_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ocve2real_stg',
        'USER': 'app_ocve2',
        'PASSWORD': '',
        'HOST': 'my-stg-1.cch.kcl.ac.uk',
    }
}

HAYSTACK_CONNECTIONS['default']['INDEX_NAME'] = PROJECT_NAME + '_stg'

#------------------------------------------------------------------------------
# Local settings
#------------------------------------------------------------------------------

try:
    from local import *
except ImportError:
    pass
