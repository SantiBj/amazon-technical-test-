from .base import *
from decouple import config
import sys

DEBUG = config('DEBUG')

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    },
    'test':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME_TEST'),
        'USER': config('DB_USER_TEST'),
        'PASSWORD': config('DB_PASSWORD_TEST'),
        'HOST': config('DB_HOST_TEST'),
        'PORT': config('DB_PORT_TEST'),
    }
}

STATIC_URL = 'static/'

