from pathlib import Path
import os, environ, base64
from dotenv import load_dotenv
from decouple import config
import pprint
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from static.exceptions import DebugException
from django.contrib.messages import constants as messages

class DebugMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, DebugException):
            response_content = ""
            for arg in exception.args:
                response_content += "<pre>" + pprint.pformat(arg) + "</pre>\n"
            return HttpResponse(response_content, content_type="text/html")

MIDDLEWARE = [
    # Otros middlewares
    'tu_proyecto.settings.DebugMiddleware',
]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

env = environ.Env()
environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS', default=[]))

if not DEBUG:
    # Configura el static para permitir --insecure
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

MESSAGE_TAGS = {
    messages.ERROR: "Error",
    messages.SUCCESS: 'Éxito',
    messages.WARNING: 'Alerta',
    messages.INFO: 'Info'
}

CUSTOM_MESSAGE_ICONS = {
    'debug': 'info',
    'Info': 'info',
    'Éxito': 'success',
    'Alerta': 'warning',
    'Error': 'error',
}

SESSION_COOKIE_HTTPONLY = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'session_security',
    'import_export',
    "django_htmx",

    # Mis APPS
    'almacen.apps.AlmacenConfig',
    'login.apps.LoginConfig',
    'inicio.apps.InicioConfig',
    'estadias.apps.EstadiasConfig',
    'sistema.apps.SistemaConfig',
    'sito.apps.SitoConfig',
    'usuario.apps.UsuarioConfig',
    'catalogo.apps.CatalogoConfig'

    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

CSRF_TRUSTED_ORIGINS = [
    "http://0.0.0.0:8004",
    "http://127.0.0.1:8004",
    "http://localhost:8004",
    "https://biblioteca.utsalamanca.edu.mx",
    # Otros orígenes permitidos aquí si es necesario
]


# Configuraciones de session security
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # O SESSION_SECURITY_INSECURE = True

SESSION_SECURITY_WARN_AFTER = 50  # Número de segundos antes de mostrar una advertencia de inactividad

SESSION_SECURITY_EXPIRE_AFTER = 1200  # Número de segundos antes de expirar la sesión por inactividad 1200

ROOT_URLCONF = 'biblioteca.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR / 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'static.context_processors.persona',
                'static.context_processors.iniciales_nombre',
                'static.context_processors.user_permissions_and_groups',
                'static.context_processors.group_permission',
                'static.context_processors.get_alumnos_clase',
                'static.context_processors.grupo_alumno',
            ],
        },
    },
]

WSGI_APPLICATION = 'biblioteca.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'HOST': os.environ.get('DB_HOST_BIBLIOTECA'),
        'NAME': os.environ.get('DB_NAME_BIBLIOTECA'),
        'USER': os.environ.get('DB_USER_BIBLIOTECA'),
        'PASSWORD': os.environ.get('DB_PASS_BIBLIOTECA'),
        'PORT': os.environ.get('DB_PORT_BIBLIOTECA'),
        'OPTIONS':  {
            'driver': 'FreeTDS',
            'unicode_results': True,
            'host_is_server': True,
            'driver_supports_utf8': True,
            'extra_params': 'tds_version=7.4',
        }
    },
      'sito': {
        'ENGINE': 'mssql',
        'HOST': os.environ.get('DB_HOST_SITO'),
        'NAME': os.environ.get('DB_NAME_SITO'),
        'USER': os.environ.get('DB_USER_SITO'),
        'PASSWORD': os.environ.get('DB_PASS_SITO'),
        'PORT': os.environ.get('DB_PORT_SITO'),
        'OPTIONS':  {
            'driver': 'FreeTDS',
            'unicode_results': True,
            'host_is_server': True,
            'driver_supports_utf8': True,
            'extra_params': 'tds_version=7.4',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-mx'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'sistema.UsuarioAcceso'

DATABASE_ROUTERS = ['routers.db_routers.AuthRouter']

X_FRAME_OPTIONS = 'SAMEORIGIN'

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # Deshabilita el límite
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

LOGIN_URL = '/login/' # Cambia a la URL de tu vista personalizada.
LOGIN_REDIRECT_URL = '/inicio/'  # Define a dónde redirigir tras un login exitoso.
# LOGOUT_REDIRECT_URL = '/usuario/login/'  # Define a dónde redirigir tras cerrar sesión (opcional).

# SMTP OFFICE 365
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_TIMEOUT = os.getenv("APP_EMAIL_TIMEOUT", 60)

# Configuración del cache usando Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://biblioteca-redis:6379/1",  # El nombre del servicio en docker-compose
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Redis como backend de sesiones
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 900  # 15 minutos
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    IINTERNAL_IPS = [
        "127.0.0.1",
    ]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True,  # Muestra siempre la barra
    }