# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.urlresolvers import reverse

import settings

#Importes de garbage
from garbage import forms
from garbage import models as garbageModels
from garbage.constsappli import *

import simplejson


@login_required
def position_mobile(request,lon,lat):
    p=request.user.personas_set.all()
    if p>0:
        p=p[0]
        j=p.jugador_set.get(juego=garbageModels.Juego.objects.get(name='GhostGarbage'),persona=p)
        
        msT=j.updatePosition(lon,lat)
        if msT.get('position_update'):
            msT.update({'status':'OK','lon':j.position.georef.x,'lat':j.position.georef.y})
            return HttpResponse(simplejson.dumps(msT))
        else:
            msT.update({'status':'NOUPDATE','lon':j.position.georef.x,'lat':j.position.georef.y,'messagAlert':'Error Posicion no permitida','iconAlert':'cerrar.png'})
            return HttpResponse(simplejson.dumps(msT))

    return HttpResponse(simplejson.dumps({'status':'ERROR'}))





@login_required
def getPuntaje(request):
    p=request.user.personas_set.all()
    if p>0:
        p=p[0]
        j=p.jugador_set.get(juego=garbageModels.Juego.objects.get(name='GhostGarbage'),persona=p)
        
        fsp=j.getFeaturePlay('Puntaje')
        if fsp:
            return HttpResponse(simplejson.dumps({'status':'OK','puntaje':fsp.getValue()}))
    return HttpResponse(simplejson.dumps({'status':'ERROR'}))





@login_required
def getEstado(request):
    p=request.user.personas_set.all()
    if p>0:
        p=p[0]
        j=p.jugador_set.get(juego=garbageModels.Juego.objects.get(name='GhostGarbage'),persona=p)   
        return HttpResponse(simplejson.dumps({'status':'OK','estado':j.get_status_display()}))
    return HttpResponse(simplejson.dumps({'status':'ERROR'}))



@login_required
def identifyServices(request):
    p=request.user.personas_set.all()
    if p>0:
        p=p[0]
        j=p.jugador_set.get(juego=garbageModels.Juego.objects.get(name='GhostGarbage'),persona=p)
        return HttpResponse(simplejson.dumps({'status':'OK','services':['casa a 3 metros ','pepe este a 50 metros']}))
    return HttpResponse(simplejson.dumps({'status':'ERROR'}))

