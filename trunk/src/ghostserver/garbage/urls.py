# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings 

urlpatterns = patterns('ghostserver.garbage.views',
                       url(r'^mobile/position/(?P<lon>[0-9.-]+)/(?P<lat>[0-9.-]+)/$' , 'position_mobile', name="position_mobile"),
                       url(r'^mobile/getPuntaje/$' , 'getPuntaje', name="getPuntaje"),
                       url(r'^mobile/getEstado/$' , 'getEstado', name="getEstado"),
                       url(r'^mobile/identifyServices/$' , 'identifyServices', name="identifyServices"),
                       url(r'^mobile/inventory/$' , 'inventory', name="inventory"),
                       url(r'^mobile/getIdJugador/$' , 'getIdJugador', name="getIdJugador"),
                       url(r'^data/kml/(?P<idJ>[0-9]+)/$' , 'getKml', name="getKml"),
                       url(r'^data/kml/$' , 'getKml', name="getKml"),
                       
                       )
