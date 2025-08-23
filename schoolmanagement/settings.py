"""
Django settings for schoolmanagement project (Render-ready).
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# -----------------------------------------------------------------------------
# Core security & debug
# -----------------------------------------------------------------------------
# Secret key comes from env in production
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")

# Default False for production; you can temporarily set True when debugging locally
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Set your Render URL after the service is created, e.g. myapp.onrender.com
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # Render sets this automatically
if RENDER_HOST:
    ALLOWED_HOSTS = [RENDER_HOST]
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_HOST}"]
else:
    # Local/dev fallback
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = []

# -----------------------------------------------------------------------------
# Installed apps
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "school",
    "widget_tweaks",
]

# -----------------------------------------------------------------------------
# Middleware (WhiteNoise added for static files on Render)
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",        # <-- add this
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "schoolmanagement.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
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

WSGI_APPLICATION = "schoolmanagement.wsgi.application"

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
# Uses Render's DATABASE_URL if present; falls back to local sqlite for dev
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR/'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=os.getenv("DATABASE_URL", "").startswith("postgres://")
        or os.getenv("DATABASE_URL", "").startswith("postgresql://"),
    )
}

# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------------------------
# I18N / TZ
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"   # your local TZ
USE_I18N = USE_L10N = USE_TZ = True

# -----------------------------------------------------------------------------
# Static files (WhiteNoise)
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [STATIC_DIR]  # keep your existing /static for dev

# WhiteNoise compressed manifest storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -----------------------------------------------------------------------------
# Auth & redirects
# -----------------------------------------------------------------------------
LOGIN_REDIRECT_URL = "/afterlogin"

# -----------------------------------------------------------------------------
# Email (moved to environment variables)
# -----------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_RECEIVING_USER = os.getenv("EMAIL_RECEIVING_USER", "").split(",") if os.getenv("EMAIL_RECEIVING_USER") else []

# -----------------------------------------------------------------------------
# Production security hardening (enabled automatically on Render)
# -----------------------------------------------------------------------------
if RENDER_HOST and not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS (safe defaults)
    SECURE_HSTS_SECONDS = 60 * 60 * 24
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
