import environ
from decouple import config

from .base import *  # noqa

env = environ.Env()
env.read_env(str(BASE_DIR / ".setting_envs/test/.env"))

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = config('SECRET_KEY')

# DATABASES
# ------------------------------------------------------------------------------
# DATABASES = {
#     'default': {
#         'ENGINE': config('MAIN_DATABASE_ENGINE'),
#         'NAME': config('MAIN_DATABASE_NAME'),
#         'USER': config('MAIN_DATABASE_USER'),
#         'PASSWORD': config('MAIN_DATABASE_PASSWORD'),
#         'HOST': config('MAIN_DATABASE_HOST'),
#         'PORT': config('MAIN_DATABASE_PORT'),
#         'OPTIONS': {'threaded': True}
#     },
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# NOSE_ARGS = [
#     '--with-coverage',  # Enable coverage reporting
#     '--cover-package=users',  # Specify the app for coverage
# ]


# NOSE_ARGS = [    
#     '--cover-erase',
#     '--cover-package=users', 
# ]


DATABASES["default"]["ATOMIC_REQUESTS"] = True

# HOSTS
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])


