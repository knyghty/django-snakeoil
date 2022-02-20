import os
from pathlib import Path

TESTS_DIR = Path(__file__).resolve(strict=True).parents[0]

db = os.getenv("DB")
if db == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": "127.0.0.1",
            "PORT": int(os.getenv("DB_PORT", 5432)),
            "NAME": "snakeoil",
            "USER": "snakeoil",
            "PASSWORD": "snakeoil",
        },
    }
elif db in {"mysql", "mariadb"}:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": "127.0.0.1",
            "PORT": int(os.getenv("DB_PORT", 3306)),
            "USER": "root",
            "PASSWORD": "snakeoil",
            "TEST": {
                "NAME": "default_test_snakeoil",
                "CHARSET": "utf8",
                "COLLATION": "utf8_general_ci",
            },
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": TESTS_DIR / "test.sqlite3",
        }
    }

INSTALLED_APPS = [
    "snakeoil",
    "tests",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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

ROOT_URLCONF = "tests.urls"

SECRET_KEY = "dummy"

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
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"environment": "tests.jinja2.environment"},
    },
]

LANGUAGE_CODE = "en"

USE_I18N = True

STATIC_URL = "/static/"

MEDIA_ROOT = TESTS_DIR / "media"

MEDIA_URL = "/media/"
