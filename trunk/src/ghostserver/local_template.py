
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
LOG_FILE = "/tmp/djangoMig.log"
STATIC_MEDIA=True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.gis',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.databrowse',
    'ghostserver.geolbs',
    'ghostserver.ghost',
#    'django.contrib.contenttypes',


)
URL_PREFIX = '/'

#prefijo donde se va a encontrar el aplicativo
ROOT_PREFIX=""

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),
		 os.path.join(os.path.dirname(__file__), 'ghost/templates'),
		)
ADMINS=ADMINS = (
		('Andres Angulo', 
		'woakas@gmail.com'),
		('Diego Cordero',
                 'draco770@hotmail.com'),
                )


DEBUG = True
TEMPLATE_DEBUG = DEBUG

