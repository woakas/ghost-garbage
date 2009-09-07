import os, sys


sys.path.append('/home/ghost/www/trunk/src/')
sys.path.append('/home/ghost/www/trunk/src/ghostserver/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ghostserver.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


