"""
Django settings for promgen project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

import dj_database_url
import raven
import yaml

from promgen.plugins import apps_from_setuptools

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.environ['CONFIG_DIR']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.path.exists(os.path.join(CONFIG_DIR, 'DEBUG'))

# Settings for Prometheus paths and such
PROMGEN_CONFIG = os.path.join(CONFIG_DIR, 'settings.yaml')
if os.path.exists(PROMGEN_CONFIG):
    with open(PROMGEN_CONFIG) as fp:
        PROMGEN = yaml.load(fp)
else:
    PROMGEN = {}

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'promgen',
] + apps_from_setuptools

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'promgen.middleware.RemoteTriggerMiddleware',
]

ROOT_URLCONF = 'promgen.urls'

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
                'promgen.context_processors.settings_in_view',
            ],
        },
    },
]

WSGI_APPLICATION = 'promgen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {'default': dj_database_url.config(
    env='DATABASE_URL',
    default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
)}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.expanduser('~/.cache/promgen')

SITE_ID = 1

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS += ['raven.contrib.django.raven_compat']
    RAVEN_CONFIG = {
        'dsn': os.environ['SENTRY_DSN'],
        'release': raven.fetch_git_sha(BASE_DIR),
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'dsn': os.environ['SENTRY_DSN'],
            },
        },
        'loggers': {
            '': {
                'handlers': ['sentry'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }

# If CELERY_BROKER_URL is set in our environment, then we configure celery as
# expected. If it is not configured, then we set CELERY_TASK_ALWAYS_EAGER to
# force celery to run all tasks in the same process (effectively runs each task
# as a normal function)
if 'CELERY_BROKER_URL' in os.environ:
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_BROKER_URL')
else:
    CELERY_TASK_ALWAYS_EAGER = True

if DEBUG:
    try:
        import debug_toolbar  # NOQA
        INSTALLED_APPS += ['debug_toolbar']
        MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
        INTERNAL_IPS = ['127.0.0.1']
    except:
        pass
