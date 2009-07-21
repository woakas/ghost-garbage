
import os
DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'ghostBD'             # Or path to database file if using sqlite3.
DATABASE_USER = 'ghost'             # Not used with sqlite3.
DATABASE_PASSWORD = 'pepito'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.




ROOT_ROOT='/home/woakas/Tesis/svn/trunk/data/static'
MEDIA_ROOT =  ROOT_ROOT+'/media'
CSS_ROOT = ROOT_ROOT+'/css'
JS_ROOT = ROOT_ROOT+'/js'
MEDIA_URL =   '/static/'
LOG_FILE = "/tmp/djangoGhost.log"
STATIC_MEDIA=True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.gis',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.databrowse',
    'django.contrib.flatpages',
    'ghostserver.geolbs',
    'ghostserver.ghost',
    'ghostserver.registration',
#    'django.contrib.admindocs',
#    'django.contrib.contenttypes',


)
URL_PREFIX = '/'

#prefijo donde se va a encontrar el aplicativo
ROOT_PREFIX=""

DEFAULT_FROM_EMAIL="woakas@alpha.miginternacional.com"
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ghost@ghost.webhop.org'
EMAIL_HOST_PASSWORD = 'g4rb4g3!'
EMAIL_PORT = 587
ACCOUNT_ACTIVATION_DAYS=2

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),
		 os.path.join(os.path.dirname(__file__), 'ghost/templates'),
		 os.path.join(os.path.dirname(__file__), 'geolbs/templates'),
		 os.path.join(os.path.dirname(__file__), 'registration/templates'),
		)
ADMINS=ADMINS = (
		('Andres Angulo', 
		'woakas@gmail.com'),
		('Diego Cordero',
                 'draco770@hotmail.com'),
                )

APPEND_SLASH=True


DEBUG = True
TEMPLATE_DEBUG = DEBUG

