"""
Django settings for boutique_ado project.
"""

import os
import dj_database_url
from pathlib import Path
from boutique_ado.custom_storages import StaticStorage, MediaStorage

if os.path.isfile('env.py'):
    import env

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# SECURITY
# =========================

SECRET_KEY = os.environ.get('SECRET_KEY', '')

DEBUG = 'DEVELOPMENT' in os.environ

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'boutique-ado-v3-c0411b2af4c5.herokuapp.com'
]


# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'home',
    'products',
    'bag',
    'checkout',
    'profiles',

    'crispy_forms',
    'crispy_bootstrap4',
    'storages',
]


# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


ROOT_URLCONF = 'boutique_ado.urls'
WSGI_APPLICATION = 'boutique_ado.wsgi.application'


# =========================
# TEMPLATES
# =========================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'bag.contexts.bag_contents',
            ],
        },
    },
]


# =========================
# DATABASE
# =========================

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}


# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# =========================
# STATIC FILES
# =========================

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================
# MEDIA FILES
# =========================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =========================
# AWS / S3 (PRODUCTION ONLY)
# =========================

USE_AWS = os.environ.get('USE_AWS', '').lower() == 'true'

if USE_AWS:

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

    AWS_S3_REGION_NAME = 'eu-west-2'
    AWS_QUERYSTRING_AUTH = False

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'


STORAGES = {
    "default": {
        "BACKEND": "custom_storages.MediaStorage",
    },
}


# =========================
# AUTHENTICATION
# =========================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'


# =========================
# EMAIL
# =========================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# =========================
# MESSAGES
# =========================

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# =========================
# DEFAULT AUTO FIELD
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================
# STRIPE
# =========================

FREE_DELIVERY_THRESHOLD = 50
STANDARD_DELIVERY_PERCENTAGE = 10

STRIPE_CURRENCY = 'usd'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')

DEFAULT_FROM_EMAIL = 'boutiqueado@example.com'