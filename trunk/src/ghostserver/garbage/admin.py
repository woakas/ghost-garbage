# -*- coding: utf-8 -*-
from django.contrib import admin
from garbage.models import *

class ServicePlayAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','juego','status')
    list_filter = ('juego', 'status')
    list_editable= ('status',)


class FeatureServicePlayAdmin(admin.ModelAdmin):
    list_display = ('jugador','feature','service')
    list_filter = ('jugador', 'feature')




admin.site.register(Jugador)
admin.site.register(Juego)
admin.site.register(TypesFeatures)
admin.site.register(Features)
admin.site.register(ServicePlay,ServicePlayAdmin)
admin.site.register(FeatureServicePlay,FeatureServicePlayAdmin)
