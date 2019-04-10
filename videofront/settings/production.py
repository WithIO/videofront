"""
These are the settings to run videofront in production.
They require setting environment variables as referenced in the following.
"""
import os
from datetime import timedelta

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", os.getenv("DJANGO_SECRET_KEY", ""))
DEBUG = os.getenv("DJANGO_DEBUG") == "yes"
ALLOWED_HOSTS = [h for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h]

# AWS

AWS_ACCESS_KEY_ID = os.environ.get("DJANGO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("DJANGO_AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("DJANGO_AWS_REGION", "eu-west-1")
AWS_S3_SIGNATURE_VERSION = "s3v4"

# S3 bucket that will store all public video assets.
S3_BUCKET = os.environ.get("DJANGO_S3_BUCKET")

# S3 bucket that will store all private video assets. In particular, source
# video files will be stored in this bucket. If you do not wish your source
# video files to be private, just set this setting to the same value as
# S3_BUCKET.
S3_PRIVATE_BUCKET = os.environ.get("DJANGO_S3_PRIVATE_BUCKET")

# Eventually use a cloudfront distribution to stream and download objects
_cf = os.getenv("DJANGO_CLOUDFRONT_DOMAIN_NAME")

if _cf:
    CLOUDFRONT_DOMAIN_NAME = _cf

# Presets are of the form: (name, ID, bitrate)
ELASTIC_TRANSCODER_PRESETS = [
    ("LD", "1351620000001-000030", 900),  # System preset: Generic 480p 4:3
    ("SD", "1351620000001-000010", 2400),  # System preset: Generic 720p
    ("HD", "1351620000001-000001", 5400),  # System preset: Generic 1080p
]
ELASTIC_TRANSCODER_THUMBNAILS_PRESET = "1351620000001-000001"
ELASTIC_TRANSCODER_PIPELINE_ID = os.environ.get("DJANGO_ELASTIC_TRANSCODER_PIPELINE_ID")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd-party
    "django_celery_results",
    "django_celery_beat",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_swagger",
    # Local apps
    "api",
    "contrib.plugins.aws",  # This is only useful for storing videos on S3
    "pipeline",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "videofront.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "videofront.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {"default": dj_database_url.config("DJANGO_DATABASE_URL")}

# Caching
# https://docs.djangoproject.com/en/1.9/topics/cache/#database-caching

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "videofront_default_cache",
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = "/static/"

# REST Framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # It is important to have BasicAuthentication as the first auth class
        # in order to prompt the user for a login/password from the GUI.
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    )
}

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "complete": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "handlers": {
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "complete",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "django": {"handlers": ["console"]},
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "botocore.vendored.requests.packages.urllib3.connectionpool": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "py.warnings": {"handlers": ["console"]},
    },
}

# Celery

CELERY_BROKER_URL = os.getenv("DJANGO_CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_TASK_ALWAYS_EAGER = DEBUG
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_BEAT_SCHEDULE = {
    "clean_upload_urls": {"task": "clean_upload_urls", "schedule": timedelta(hours=1)},
    "transcode_video_restart": {
        "task": "transcode_video_restart",
        "schedule": timedelta(seconds=5),
    },
}

# Swagger documentation

SWAGGER_SETTINGS = {
    "APIS_SORTER": "alpha",
    "OPERATIONS_SORTER": "alpha",
    "USE_SESSION_AUTH": False,
    "VALIDATOR_URL": None,
}

##############################
# Videofront-specific settings
##############################

# Maximum size of subtitle files
SUBTITLES_MAX_BYTES = 1024 * 1024 * 5  # 5 Mb

# Override this setting to provide your own custom implementation of pipeline tasks.
PLUGIN_BACKEND = "contrib.plugins.aws.backend.Backend"

# Maximum of width and height size for video thumbnails
THUMBNAILS_SIZE = 1024
