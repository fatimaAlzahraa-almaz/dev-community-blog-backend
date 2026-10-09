"""
Django settings for core project.
"""

import os
from pathlib import Path
from datetime import timedelta

import dj_database_url
from dotenv import load_dotenv


# Load local .env during development.
# On Render, environment variables are configured in the dashboard.
load_dotenv()


# Build paths inside the project.
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# Environment helpers
# --------------------------------------------------

def get_env_list(name, default=""):
    """
    Read comma-separated values from an environment variable.
    Example:
    CORS_ALLOWED_ORIGINS=https://app.example.com,http://localhost:3000
    """
    return [
        item.strip()
        for item in os.environ.get(name, default).split(",")
        if item.strip()
    ]


# --------------------------------------------------
# Core settings
# --------------------------------------------------

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = (
    os.environ.get("DEBUG", "False").strip().lower() == "true"
)


# --------------------------------------------------
# Allowed hosts
# --------------------------------------------------

ALLOWED_HOSTS = get_env_list(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1",
)

# Render can provide the service hostname automatically.
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if render_hostname and render_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_hostname)


# --------------------------------------------------
# Applications
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "django_filters",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",

    "users",
    "posts",
    "interactions",
]


# --------------------------------------------------
# Middleware
# --------------------------------------------------

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


# --------------------------------------------------
# URL and application configuration
# --------------------------------------------------

ROOT_URLCONF = "core.urls"

WSGI_APPLICATION = "core.wsgi.application"

AUTH_USER_MODEL = "users.User"


# --------------------------------------------------
# Templates
# --------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# --------------------------------------------------
# Database: PostgreSQL / Neon
# --------------------------------------------------

DATABASE_URL = os.environ["DATABASE_URL"]

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=0,
    ),
}

# Ensure SSL for Neon without removing other URL options.
DATABASES["default"].setdefault("OPTIONS", {})
if "sslmode" not in DATABASES["default"]["OPTIONS"]:
    DATABASES["default"]["OPTIONS"]["sslmode"] = "require"


# --------------------------------------------------
# Password validation
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# --------------------------------------------------
# Internationalization
# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# --------------------------------------------------
# Static files
# --------------------------------------------------

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# --------------------------------------------------
# Uploaded media files
# --------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# --------------------------------------------------
# Email
# --------------------------------------------------

# No email-sending feature is currently implemented.
# Intentionally omit MAILERS so missing EMAIL_HOST variables
# do not prevent Django from starting.
#
# If you add email features later, configure a real SMTP
# service through environment variables.


# --------------------------------------------------
# Django REST Framework
# --------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),

    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],

    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),

    "PAGE_SIZE": 10,

    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES": {
        "anon": "1000/day",
        "user": "1000/day",
    },
}


# --------------------------------------------------
# CORS
# --------------------------------------------------

CORS_ALLOWED_ORIGINS = get_env_list(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
)

CORS_ALLOW_CREDENTIALS = True


# --------------------------------------------------
# CSRF
# --------------------------------------------------

CSRF_TRUSTED_ORIGINS = get_env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
)


# --------------------------------------------------
# Simple JWT
# --------------------------------------------------

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}


# --------------------------------------------------
# Security settings
# --------------------------------------------------

if not DEBUG:
    # Render terminates HTTPS at its proxy.
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

SECURE_SSL_REDIRECT = (
    os.environ.get(
        "SECURE_SSL_REDIRECT",
        "False" if DEBUG else "True",
    ).strip().lower() == "true"
)

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG

# Enable HSTS only after verifying HTTPS for your deployed domain.
SECURE_HSTS_SECONDS = int(
    os.environ.get("SECURE_HSTS_SECONDS", "0")
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    os.environ.get(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS",
        "False",
    ).strip().lower() == "true"
)

SECURE_HSTS_PRELOAD = (
    os.environ.get(
        "SECURE_HSTS_PRELOAD",
        "False",
    ).strip().lower() == "true"
)


# --------------------------------------------------
# Default primary key field type
# --------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"