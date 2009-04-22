import os, sys


sys.path.append('/home/ghost/www/trunk/src/')
sys.path.append('/home/ghost/www/trunk/src/ghostserver/')
f=open("/tmp/ss","w")
f.write(str(sys.path))
f.close()


os.environ['DJANGO_SETTINGS_MODULE'] = 'ghostserver.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


