import datetime
import os
from pathlib import Path
import environ


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR

django_env = environ.Env()
django_env.read_env(str(BASE_DIR / ".setting_envs/local/.django"))
# GENERAL
# ------------------------------------------------------------------------------
DEBUG = False
TIME_ZONE = "Asia/Tehran"
LANGUAGE_CODE = "en-gb"
SITE_ID = 1
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(BASE_DIR / "locale")]
LANGUAGES = (
    ('en', 'English'),
    # ('fa', 'Persian'),
)

# DATABASES
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    "rest_framework",
    'drf_yasg',
]


LOCAL_APPS = [

]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------


# AUTHENTICATION
# ------------------------------------------------------------------------------


# PASSWORDS
# ------------------------------------------------------------------------------

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = "/static/"

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# CELERY
# ------------------------------------------------------------------------------


# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),  # Token expiration time
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),  # Refresh token expiration time
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME_GRACE_PERIOD': datetime.timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME_CREATE_OFFSET': datetime.timedelta(minutes=10),
    'TOKEN_OBTAIN_SERIALIZER': 'users.apis.serializers.CustomTokenObtainSerializer'
}

# EMAIL SETTINGS
# ------------------------------------------------------------------------------


# SWAGGER
# ------------------------------------------------------------------------------
SWAGGER_SETTINGS = {
    'LOGIN_URL': 'users:token_obtain_pair',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'SECURITY_REQUIREMENTS': [
        {
            'Bearer': []
        }
    ],
}

# PROJECT REQUIREMENT
# ------------------------------------------------------------------------------
# PROJECT REQUIREMENT
# ------------------------------------------------------------------------------
SERVICE_NAME = "config"

ELASTICSEARCH_HOST = SECRET_KEY = django_env(
    "ELASTICSEARCH_HOST",
)