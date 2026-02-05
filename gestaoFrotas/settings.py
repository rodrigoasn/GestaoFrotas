"""
Django settings for Gestão de Frotas project
Django 5.2
Internacionalization: PT-br, en
"""

# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _


# ────────────────────────────────────────────────────────────────────
# NÚCLEO
# ────────────────────────────────────────────────────────────────────
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', '0') == '1'

ENVIRONMENT = os.environ.get("ENVIRONMENT")
ALLOWED_HOSTS = ['*']

# Model de usuário personalizado
AUTH_USER_MODEL = 'accounts.CustomUser'

# Para onde ir depois do login com sucesso (ex: dashboard ou home)
LOGIN_REDIRECT_URL = 'dashboard'  # ou o 'name' da sua url principal
# Para onde ir depois de fazer logout
LOGOUT_REDIRECT_URL = 'login'
# URL para quem tenta acessar uma página restrita sem estar logado
LOGIN_URL = 'login'


# ────────────────────────────────────────────────────────────────────
# APPS
# ────────────────────────────────────────────────────────────────────
TEMPLATES_APPS = [
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MY_APPS = [
    'accounts.apps.AccountsConfig',
    'core.apps.CoreConfig',
]

THIRD_APPS = [
    'django_bootstrap5',
    'django_bootstrap_icons',
]

# Aplicativos instalados 
INSTALLED_APPS = TEMPLATES_APPS + DJANGO_APPS + MY_APPS + THIRD_APPS


# ────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# ────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # internacionalização
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.SessionTimeoutMiddleware', # Middleware para tempo de sessão
]

# URL de configuração
ROOT_URLCONF = 'gestaoFrotas.urls'


# ────────────────────────────────────────────────────────────────────
# TEMPLATES
# ────────────────────────────────────────────────────────────────────
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
                'core.context_processors.session_expiry',
                'core.context_processors.system_configuration',
            ],
        },
    },
]

WSGI_APPLICATION = 'gestaoFrotas.wsgi.application'


# ────────────────────────────────────────────────────────────────────
# BANCO DE DADOS
# ────────────────────────────────────────────────────────────────────
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}


# ────────────────────────────────────────────────────────────────────
# AUTH
# ────────────────────────────────────────────────────────────────────
# Validação de senha
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ────────────────────────────────────────────────────────────────────
# i18n / timezone
# ────────────────────────────────────────────────────────────────────
# Internacionalização
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Idiomas disponíveis
LANGUAGES = [
    ('pt-br', 'Português'),
    ('en', 'English'),
]

# Caminho dos arquivos .po/.mo
LOCALE_PATHS = [BASE_DIR / "locale"]


# ────────────────────────────────────────────────────────────────────
# ARQUIVOS ESTÁTICOS / MÍDIA
# ────────────────────────────────────────────────────────────────────
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL  = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
X_FRAME_OPTIONS = "SAMEORIGIN"


# ────────────────────────────────────────────────────────────────────
# SESSÕES
# ────────────────────────────────────────────────────────────────────
# Tempo de sessão em segundos (ex: 30 minutos = 1800)
SESSION_COOKIE_AGE = 1800

# Para encerrar sessão no navegador fechado (opcional)
# importante: False aqui, usamos .modified manualmente no middleware
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# ────────────────────────────────────────────────────────────────────
# EMAIL
# ────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ["true", "1", "yes"]
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# ────────────────────────────────────────────────────────────────────
# BOOTSTRAP ICONS
# ────────────────────────────────────────────────────────────────────
BS_ICONS_BASE_URL = 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/' # URL base para o download inicial
BS_ICONS_CACHE = os.path.join(STATIC_ROOT, 'icon_cache') # Onde ele vai salvar