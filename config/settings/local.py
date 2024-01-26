import environ
from decouple import config

from .base import *  # noqa


# env files
django_env = environ.Env()
django_env.read_env(str(BASE_DIR / ".setting_envs/local/.django"))
database_env = environ.Env()
database_env.read_env(str(BASE_DIR / ".setting_envs/local/.postgres"))

# local databases
DATABASES = {
    'default': {
        'ENGINE': database_env('MAIN_DB_ENGINE'),
        'NAME': database_env('MAIN_DB_NAME'),
        'USER': database_env('MAIN_DB_USER'),
        'PASSWORD': database_env('MAIN_DB_PASSWORD'),
        'HOST': database_env('MAIN_DB_HOST'),
        'PORT': database_env('MAIN_DB_PORT'),
    }
}

DEBUG = True

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = django_env(
    "SECRET_KEY",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]


DATABASES["default"]["ATOMIC_REQUESTS"] = True

# HOSTS
# ------------------------------------------------------------------------------

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
LOCAL_APPS = [
    'debug_toolbar',
]

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE