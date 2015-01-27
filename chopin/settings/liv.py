from base import *

CACHE_REDIS_DATABASE = '0'
CACHES['default']['LOCATION'] = '127.0.0.1:6379:' + CACHE_REDIS_DATABASE

INTERNAL_IPS = ('ocve3.dighum.kcl.ac.uk', )
ALLOWED_HOSTS = ['ocve3.dighum.kcl.ac.uk', 'www,chopinonline.ac.uk',
                 'chopinonline.ac.uk']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_ocve_aco_liv',
        'USER': 'app_ocve',
        'PASSWORD': '',
        'HOST': 'db-pg-1.cch.kcl.ac.uk'
    },
    'ocve_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ocve2real_liv',
        'USER': 'app_ocve2',
        'PASSWORD': '',
        'HOST': 'my-liv-2.cch.kcl.ac.uk',
    }
}

#------------------------------------------------------------------------------
# Local settings
#------------------------------------------------------------------------------

try:
    from local import *
except ImportError:
    pass
