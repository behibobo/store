'''Use this for development'''

from .base import *

ALLOWED_HOSTS += ['api.irantechnosanat.com','127.0.0.1', '192.168.1.102', '178.63.238.103']
DEBUG = True

WSGI_APPLICATION = 'home.wsgi.dev.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
CORS_ORIGIN_ALLOW_ALL = True
DEFAULT_CHARSET = 'utf-8'

# CORS_ORIGIN_WHITELIST = (
#     'http://192.168.1.103:3000',
#     'http://192.168.1.103:3003',
# )

# Stripe

STRIPE_PUBLIC_KEY = config('STRIPE_TEST_PUBLIC_KEY')
STRIPE_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY')
