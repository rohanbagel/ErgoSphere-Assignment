"""Django settings for the AI Book Intelligence backend."""

import os
from pathlib import Path

from dotenv import load_dotenv


def parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_csv(value: str | None, default: list[str] | None = None) -> list[str]:
    if value is None:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "change-me-in-local-env")
DEBUG = parse_bool(os.getenv("DJANGO_DEBUG"), default=True)
ALLOWED_HOSTS = parse_csv(
    os.getenv("DJANGO_ALLOWED_HOSTS"),
    default=["127.0.0.1", "localhost", "testserver"],
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'apps.books',
    'apps.ai',
    'apps.ingestion',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").strip().lower()
if DB_ENGINE == "mysql":
    MYSQL_DB = os.getenv("MYSQL_DB", "")
    if not MYSQL_DB:
        raise ValueError("MYSQL_DB must be set when DB_ENGINE is 'mysql'.")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': MYSQL_DB,
            'USER': os.getenv("MYSQL_USER", "root"),
            'PASSWORD': os.getenv("MYSQL_PASSWORD", ""),
            'HOST': os.getenv("MYSQL_HOST", "127.0.0.1"),
            'PORT': os.getenv("MYSQL_PORT", "3306"),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = parse_bool(os.getenv("CORS_ALLOW_ALL_ORIGINS"), False)
CORS_ALLOWED_ORIGINS = parse_csv(
    os.getenv("CORS_ALLOWED_ORIGINS"),
    default=["http://127.0.0.1:5173", "http://localhost:5173"],
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

SCRAPER_BASE_URL = os.getenv("SCRAPER_BASE_URL", "https://books.toscrape.com/")
SCRAPER_DEFAULT_MAX_PAGES = int(os.getenv("SCRAPER_DEFAULT_MAX_PAGES", "3"))
