"""
Django settings for bank project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from datetime import timedelta

import dj_database_url
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'silk',
    'corsheaders',
    # Internal
    'clients',
    'transactions',
    'currency',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bank.urls'

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

TEMPLATE_DEBUG = DEBUG

WSGI_APPLICATION = 'bank.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(config('PSQL_URL')),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} m:{module} p-id:{process:d} t-id:{thread:d}\n\"{message}\"',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'info.log'),
            'formatter': 'simple',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'error.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'info_logger': {
            'handlers': ['file_info'],
            'level': 'INFO',
        },
        'error_logger': {
            'handlers': ['file_error'],
            'level': 'ERROR',
        },
        # Redirect all django log messages to our file handlers
        'django': {
            'handlers': ['console', 'file_info', 'file_error'],
        },
    }
}

AUTH_USER_MODEL = 'clients.Client'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# Cache configuration


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config('REDIS_PASSWORD')
        }
    }
}


# REST configuration

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'drf_utils.auth.JWTCachedAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'drf_utils.renderers.PlainJsonRenderer',
    ),
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': (
        'drf_utils.negotiation.IgnoreContentNegotiation'
    ),
}

SIMPLE_JWT = {
    'SIGNING_KEY': config('JWT_SECRET'),
    # Signing key must be 256+ bit long (about 64 chars)
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    # Added for development needs.
    # WARNING: remove this line in production
}

CORS_ORIGIN_ALLOW_ALL = True
# All origins are allowed. Our customers may connect to our API
# from a lot of origins. So, instead of the CORS protection
# the application needs a lot of authentication required views.
# CORS is needed to bypass browsers' same origin policy.
# Without CORS users cannot access our API through third-party site.

# Exchange rates server parameters

EXCHANGE_APP_ID = config('EXCHANGE_APP_ID')

EXCHANGE_LINK = 'https://openexchangerates.org/api/latest.json'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join('public', 'static')

# Silk profiler
SILKY_PYTHON_PROFILER = True
