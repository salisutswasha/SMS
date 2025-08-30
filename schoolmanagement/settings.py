""" 
Django settings for schoolmanagement project. 
""" 

import os 
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent.parent 
TEMPLATE_DIR = BASE_DIR / "templates" 

STATIC_URL = '/static/' 
STATIC_DIR = BASE_DIR / "staticfiles" 

# ----------------------------------------------------------------------------- 
# Core security & debug 
# ----------------------------------------------------------------------------- 
SECRET_KEY = 'k0ujs9pcw+7qohwas!o7_ept20$c@$)-b=qco8sgviy_f)((bc' # your old dev key 
DEBUG = True 
ALLOWED_HOSTS = [] # Empty means local only 

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
# Middleware 
# ----------------------------------------------------------------------------- 
MIDDLEWARE = [ 
    "django.middleware.security.SecurityMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware", 
    "django.middleware.common.CommonMiddleware", 
    "django.middleware.csrf.CsrfViewMiddleware", 
    "django.contrib.auth.middleware.AuthenticationMiddleware", 
    "django.contrib.messages.middleware.MessageMiddleware", 
    "django.middleware.clickjacking.XFrameOptionsMiddleware", 
    "whitenoise.middleware.WhiteNoiseMiddleware", 
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
# settings.py 
import os 
from pathlib import Path 
BASE_DIR = Path(__file__).resolve().parent.parent 

DATABASES = { 
    "default": { 
        "ENGINE": "django.db.backends.sqlite3", 
        "NAME": BASE_DIR / "db.sqlite3", 
    } 
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
TIME_ZONE = "Africa/Lagos" 
USE_I18N = True 
USE_L10N = True 
USE_TZ = True 

# ----------------------------------------------------------------------------- 
# Static files 
# ----------------------------------------------------------------------------- 
STATIC_URL = "/staticfiles/" 
STATICFILES_DIRS = [STATIC_DIR] 

# ----------------------------------------------------------------------------- 
# Auth & redirects 
# ----------------------------------------------------------------------------- 
LOGIN_REDIRECT_URL = "/afterlogin" 

# ----------------------------------------------------------------------------- 
# Email 
# ----------------------------------------------------------------------------- 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_USE_TLS = True 
EMAIL_PORT = 587 
EMAIL_HOST_USER = 'salisutswasha@gmail.com' 
EMAIL_HOST_PASSWORD = 'lktw zxgw pvjq yxjj' 
EMAIL_RECEIVING_USER = ['salisutswasha@gmail.com'] 
