import os

from .base import *  
from .utils import strtobool

DEBUG = strtobool(os.getenv("DEBUG", "y"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ozyl(r!*=wht$a7^pp+wp=zg5g96yg5wz!7fwe$gq63874z9##'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chatapp',
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}
