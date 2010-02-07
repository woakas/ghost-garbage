# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings 

urlpatterns = patterns('ghostserver.garbage.views',
                       url(r'^mobile/position/(?P<lon>[0-9.-]+)/(?P<lat>[0-9.-]+)/$' , 'position_mobile', name="position_mobile"),
                       url(r'^mobile/getPuntaje/$' , 'getPuntaje', name="getPuntaje"),
                       url(r'^mobile/getEstado/$' , 'getEstado', name="getEstado"),
                       url(r'^mobile/getVision/$' , 'getVision', name="getVision"),
                       url(r'^mobile/identifyServices/$' , 'identifyServices', name="identifyServices"),
                       url(r'^mobile/getIdJugador/$' , 'getIdJugador', name="getIdJugador"),
                       url(r'^mobile/services/(?P<field>\w+)/$' , 'services', name="services"),
                       url(r'^mobile/services/$' , 'services', name="services"),
                       url(r'^mobile/inventory/(?P<field>\w+)/$' , 'inventory', name="inventory"),
                       url(r'^mobile/inventory/$' , 'inventory', name="invetory"),
                       url(r'^data/kml/$' , 'getKml', name="getKml"),
                       url(r'^data/json/$' , 'getJson', name="getJson"),
                       url(r'^game/$' , 'game', name="game"),
                       )
