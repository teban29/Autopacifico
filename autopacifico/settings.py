from pathlib import Path
import os
import dj_database_url

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

# Entorno: Render (Producción) o Local (Desarrollo)
IS_PRODUCTION = 'RENDER' in os.environ

# Debug
DEBUG = not IS_PRODUCTION

# Hosts permitidos
if IS_PRODUCTION:
    ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
if IS_PRODUCTION:
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://postgres:postgres@localhost:5432/mysite',
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

INSTALLED_APPS = [
    'django_extensions',
    'ruleta',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

if IS_PRODUCTION:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

# Static files
STATIC_URL = 'static/'

if IS_PRODUCTION:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Otros ajustes
ROOT_URLCONF = 'autopacifico.urls'
WSGI_APPLICATION = 'autopacifico.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sesiones
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True

# Login y Logout
LOGIN_REDIRECT_URL = '/dashboard/'  # Después del login
LOGIN_URL = '/admin/login/'  # URL de login
LOGOUT_REDIRECT_URL = '/'  # Después del logout

# Configuración SSL en Producción
if IS_PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
