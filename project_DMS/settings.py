"""
Django settings for project_DMS project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from pickle import FALSE

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-tx-6s#w--wo^bfsa@np64zni7g34pwl%s5=ku%fp4-k@&#^osp"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# '192.168.43.97'
ALLOWED_HOSTS = [
    "192.168.43.97",
    "127.0.0.1",
    ".herokuapp.com",
    "example.herokuapp.com",
]

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "student",
    "staff",
    "hod",
    "login",
    "home_page",
    "tutor",
    "parent"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project_DMS.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project_DMS.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

"""
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'project_DMS',
    }
}"""

import dj_database_url

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'project_DMS',
#         'USER': 'postgres',
#         'PASSWORD': '123456789',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
# '''DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'project_DMS',
#         'USER': 'postgres',
#         'PASSWORD': '123456789',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }'''
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "project_dms",
        "USER": "postgres",
        "PASSWORD": "123456789",#use 123456789 for linz,abhi,jayakri
        "HOST": "localhost",
        "PORT": "5432",
    },
    # 'default':{
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'd6r6g1el4m892u',
    #     'USER': 'wpiuxtrduedake',
    #     'PASSWORD':'4590bf46a3dbb1dca1d0f67e5402c6d60e09efca0a332720ae97030ea936cb7a',
    #     'HOST': 'ec2-44-198-82-71.compute-1.amazonaws.com',
    #     'PORT': '5432',
    # }
}
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

WHITENOISE_USE_FINDERS = True
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
# STATICFILES_DIRS = [(os.path.join(BASE_DIR, 'static'))]
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Storing images
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "login.MyUser"

LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"
