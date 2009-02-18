# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.gis import admin as admingis
from geolbs.models import *
from django.contrib.contenttypes import generic


class LugaresAdmin(generic.GenericTabularInline):
    model =Lugares
    extra=1



class GeoRefAdmin(admingis.OSMGeoAdmin):
    """Clase para visualizar los elemenmos con geodjango permitiendo colocar un mapa de OSM dentro de la parte de administración
    """
    display_srid = 4326
    inlines = [
        LugaresAdmin
    ]




admin.site.register(TiposLugar)
admin.site.register(Lugares)
admingis.site.register(Punto,GeoRefAdmin)
admingis.site.register(Poligono,GeoRefAdmin)
admingis.site.register(Linea,GeoRefAdmin)
admin.site.register(Atributo)
admin.site.register(ClaseDeServicio)
admin.site.register(Servicio)
