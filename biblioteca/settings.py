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
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-i-quay)0vi@ofqo!o*js^01l_p7s+sh^c7!mdydd53y0x5lb3w'
SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)
# DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']  # O tu dominio si es necesario

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
]


# Configuraciones de session security
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # O SESSION_SECURITY_INSECURE = True

SESSION_SECURITY_WARN_AFTER = 50  # Número de segundos antes de mostrar una advertencia de inactividad

SESSION_SECURITY_EXPIRE_AFTER = 1800  # Número de segundos antes de expirar la sesión por inactividad 1200

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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
      'sito': {
        'ENGINE': 'mssql',
        'HOST': os.environ.get('DB_HOST_SITO'),
        'NAME': os.environ.get('DB_NAME_SITO'),
        'USER': os.environ.get('DB_USER_SITO'),
        'PASSWORD': os.environ.get('DB_PASS_SITO'),
        'PORT': os.environ.get('DB_PORT_SITO'),
        'OPTIONS':  {
            'driver': 'ODBC Driver 17 for SQL Server'
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
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'sistema.UsuarioAcceso'

DATABASE_ROUTERS = ['routers.db_routers.AuthRouter']

STATIC_ROOT = BASE_DIR / 'staticfiles'
# Configuración archivos Media, para guardado de documentos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

X_FRAME_OPTIONS = 'SAMEORIGIN'

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # Deshabilita el límite
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

LOGIN_URL = '/login/' # Cambia a la URL de tu vista personalizada.
LOGIN_REDIRECT_URL = '/inicio/'  # Define a dónde redirigir tras un login exitoso.
# LOGOUT_REDIRECT_URL = '/usuario/login/'  # Define a dónde redirigir tras cerrar sesión (opcional).

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.office365.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'tu_correo@outlook.com'
# EMAIL_HOST_PASSWORD = 'tu_contraseña'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER