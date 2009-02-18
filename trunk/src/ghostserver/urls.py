# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.gis import admin
import settings 


admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^'+settings.ROOT_PREFIX+'lbs/', include('ghostserver.ghost_lbs.urls')),
    (r'^'+settings.ROOT_PREFIX+'', include('ghostserver.ghost.urls')),


    # Uncomment the next line to enable the admin:
    (r'^'+settings.ROOT_PREFIX+'admin/(.*)', admin.site.root),
)




#Permite servir desde el servidor de django imágenes y archivos 
#No se debe realizar esto en un servidor en producción
if settings.STATIC_MEDIA:
    urlpatterns += patterns('',
     ## Servir Archivos Media, css y JS
     (r'^'+settings.ROOT_PREFIX+'static/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT , 'show_indexes': True}),
     (r'^'+settings.ROOT_PREFIX+'static/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_ROOT , 'show_indexes': True}),
     (r'^'+settings.ROOT_PREFIX+'static/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_ROOT , 'show_indexes': True}),
    )
