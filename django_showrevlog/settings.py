"""
Django settings for django_showrevlog project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@n+%&xv&$_e=d8rc$vcbhk@aaz3mecz!i(m$+nyq!5(ixm^h(d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'showrevlog.apps.ShowRevLogConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_showrevlog.urls'

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

WSGI_APPLICATION = 'django_showrevlog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'showrevlog', 'locale'),
]

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'normal': {
            'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)s] %(process)d %(message)s'
        },
    },

    'handlers': {
        'django_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'normal',
            'filename': os.path.join(BASE_DIR, 'log', 'django.log'),
            'encoding': 'utf-8',
            'when': 'midnight',
            'backupCount': 16,
        },
        'showrevlog_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'normal',
            'filename': os.path.join(BASE_DIR, 'log', 'showrevlog.log'),
            'encoding': 'utf-8',
            'when': 'midnight',
            'backupCount': 16,
        },
    },

    'loggers': {
        'django': {
            'handlers': ['django_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'showrevlog': {
            'handlers': ['showrevlog_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


SHOWREVLOG_DIRS = (os.path.join(BASE_DIR, 'log'),)
SHOWREVLOG_PER_PAGE = 32
SHOWREVLOG_LINEXP = ('(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})'
                     '\s(?P<type>[A-Z]+)'
                     '\s\[(?P<source>[^:]+):(?P<line>[0-9]+)\]'
                     '\s(?P<process>[0-9]+)'
                     '\s(?P<message>.+)')
SHOWREVLOG_TARGET = lambda f: f.find('.log') and os.path.getsize(f) > 0
