import os
from pathlib import Path
from dotenv import load_dotenv

# TODO: Extract all environment variables from .env file

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_ai.settings")
address = os.environ.get("RABBITMQ_ADDRESS")
address = "localhost" if address is None else address
# CELERY_BROKER_URL = "amqp://guest:guest@" + address + ":5672//"
CELERY_RESULT_BACKEND = "rpc://"
# TODO: These should be in env file
GCP_ADDRESS = os.environ.get("GCP_ADDRESS")
ALLOWED_HOSTS = ["localhost", "0.0.0.0", GCP_ADDRESS]
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
BASE_DIR = Path(__file__).resolve().parent.parent
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
SECRET_KEY = "django-insecure-nh@+rk!cf-vr=*q%ftln*i2dhqcjk4(a(w#kn$unv7p+ajm339"
DEBUG = True
# TODO: Review these apps
INSTALLED_APPS = [
    "task_ai.app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_yasg",
    "task_ai.openai_client",
    "task_ai.celery",
    "task_ai.signals",
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
ROOT_URLCONF = "task_ai.urls"
# TODO: Do I need this?
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
WSGI_APPLICATION = "task_ai.wsgi.application"
# Database
# TODO: Update this to use postgres
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# Password validation
AUTH_USER_MODEL = "app.CustomUser"
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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
