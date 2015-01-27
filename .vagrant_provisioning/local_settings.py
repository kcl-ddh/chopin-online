CACHE_REDIS_DATABASE = '0'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_ocve_dev',
        'USER': 'app_ocve',
        'PASSWORD': 'app_ocve',
        'HOST': 'localhost'
    },
    'ocve_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app_ocve_dev',
        'USER': 'app_ocve',
        'PASSWORD': 'password',
        'HOST': 'localhost',
    }
}

INTERNAL_IPS = ('0.0.0.0', '127.0.0.1', '::1')

SECRET_KEY = 'nvvx43-#q2$r_24eo1rz*@*va8k5na1us7804-z+=u%1)*^y4n'

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'chopin.settings.local.show_toolbar',
}

# https://github.com/sehmaschine/django-grappelli/issues/456
# Any value other than "" in the setting value will break the inline templates
TEMPLATE_STRING_IF_INVALID = 'INVALID %s'
