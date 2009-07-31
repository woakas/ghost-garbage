# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.gis import admin
import settings 




from django.contrib import databrowse
from geolbs.models import Linea, Poligono

databrowse.site.register(Linea)
databrowse.site.register(Poligono)


admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^lbs/', include('ghostserver.geolbs.urls')),
    (r'^', include('ghostserver.ghost.urls')),


    # Descomente la siguiente linea si desea tener documentación sobre el aplicativo
#    (r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    (r'^admin/(.*)', admin.site.root),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^accounts/', include('registration.urls')),

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
