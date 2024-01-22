import environ
from decouple import config

from .base import *  # noqa

env = environ.Env()
env.read_env(str(BASE_DIR / ".setting_envs/production/.env"))

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = config('DEBUG')
SECRET_KEY = config('SECRET_KEY')

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': config('MAIN_DATABASE_ENGINE'),
        'NAME': config('MAIN_DATABASE_NAME'),
        'USER': config('MAIN_DATABASE_USER'),
        'PASSWORD': config('MAIN_DATABASE_PASSWORD'),
        'HOST': config('MAIN_DATABASE_HOST'),
        'PORT': config('MAIN_DATABASE_PORT'),
        'OPTIONS': {'threaded': True}
    },
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# HOSTS
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])


INSTALLED_APPS += [
    'django_prometheus'
]
MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_prometheus.middleware.PrometheusBeforeMiddleware',  # this line was added
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',  # this line was added
]