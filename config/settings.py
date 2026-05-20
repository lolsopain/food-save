import os
from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key-for-local-dev-12345')

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Uchinchi tomon kutubxonalari
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',

    # Loyihaning ichki ilovalari (Apps)
    'users',
    'restaurants',
    'foods',
    'reservations',
]

AUTH_USER_MODEL = 'users.User'

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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'FoodSave API',
    'DESCRIPTION': 'Restaurant food reservation platform API',
    'VERSION': '1.0.0',
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# SUPABASE BULUTLI SAQLASH TIZIMI SOZLAMALARI
# ==============================================================================
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'django_storage_supabase.storage.SupabaseStorage'

# Supabase kalitlari
SUPABASE_URL = config('SUPABASE_URL', default='https://npvazxxcraaywvdupdoo.supabase.co')
SUPABASE_KEY = config('SUPABASE_KEY', default='sb_publishable_0vlg4xbYiNQGW1G-CXBZUQ_t7y5cmQvVpB-vG')
SUPABASE_BUCKET_NAME = 'foods'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'