"""
Django settings for staffsense project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "daphne",
    "channels",
    "cloudinary",
    "cloudinary_storage",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authentication",  # All authentication functions are present in this app
    "projectTaskManagement",  # Project and Task Management
    "complaints",  # Complaints and Request
    "leavemanagement",  # Leave Management
    "chat",  # Chat Management
    "meetingmanagement",  # Meeting Management
    "visitormanagement",  # Visitor Management
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "staffsense.urls"

TEMPLATES = [
    {
        "BACKEND" : "django.template.backends.django.DjangoTemplates",
        "DIRS"    : ["templates"],
        "APP_DIRS": True,
        "OPTIONS" : {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "staffsense.asgi.application"
# WSGI_APPLICATION = "staffsense.wsgi.application"
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


# Database
# DATABASES = {
#     "default": {
#         "ENGINE"  : "django.db.backends.postgresql",
#         "HOST"    : config("Hostname"),
#         "USER"    : config("Username"),
#         "PASSWORD": config("Password"),
#         "NAME"    : config("Database"),
#         "PORT"    : config("Port"),
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE"  : "django.db.backends.postgresql",
#         "HOST"    : "localhost",
#         "USER"    : "postgres",
#         "PASSWORD": "3254595",
#         "NAME"    : "staffsense",
#         "PORT"    : "5432",
#     }
# }

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}


# Cloudinary Configruation settings
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config("CLOUD_NAME"),
    'API_KEY'   : config('API_KEY'),
    'API_SECRET': config('API_SECRET'),
}

# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# JWT Token
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
}

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND"  : "channels_redis.core.RedisChannelLayer",
        "CONFIG"   : {
            "hosts": [config("redis")],
        },
    },
}

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             # "hosts": [("127.0.0.1", 6379)],
#             "hosts": "rediss://red-ckkh6fsl4vmc73a0jr1g:WPlw394luUNFQ9IlpR8MmkFTsCmUObZh@singapore-redis.render.com:6379",
#         },
#     },
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE   = "en-us"

TIME_ZONE       = "UTC"

USE_I18N        = True

USE_L10N        = True

USE_TZ          = True

AUTH_USER_MODEL = "authentication.Employee"


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # Add other authentication backends if needed
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL       = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]



MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL  = "/media/"

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD    = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS  = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
]


EMAIL_BACKEND       = config("EMAIL_BACKEND")
EMAIL_HOST          = config("EMAIL_HOST")
EMAIL_USE_TLS       = config("EMAIL_USE_TLS", "")
EMAIL_PORT          = config("EMAIL_PORT")
EMAIL_HOST_USER     = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
