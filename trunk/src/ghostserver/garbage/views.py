# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.urlresolvers import reverse


import settings

#Importes de garbage
from garbage import forms
from garbage.constsappli import *
from garbage import models as garbageModels


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
def getIdJugador(request):
    p=request.user.personas_set.all()
    if p>0:
        p=p[0]
        j=p.jugador_set.get(juego=garbageModels.Juego.objects.get(name='GhostGarbage'),persona=p)
        return HttpResponse(simplejson.dumps({'status':'OK','idJugador':j.id}))
    return HttpResponse(simplejson.dumps({'status':'ERROR',}))


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
        iss=j.identifyServices()
        if len(iss)>0:
            iserv="\n".join(["%s a %.3f metros"%(m,d.m) for m,d in iss])
        else:
            iserv="No existen Servicios Cercanos"
    
        
        return HttpResponse(simplejson.dumps({'status':'OK','services':iserv}))
    return HttpResponse(simplejson.dumps({'status':'ERROR'}))





@login_required
def inventory(request):
    p=request.user.personas_set.all()
    if p>0:
        p=p[0]
        j=p.jugador_set.get(juego=garbageModels.Juego.objects.get(name='GhostGarbage'),persona=p)
        iserv="No tiene nada en el Inventario."
        
        return HttpResponse(simplejson.dumps({'status':'OK','services':iserv}))
    return HttpResponse(simplejson.dumps({'status':'ERROR'}))





def getKml(request,idJ=None):
    try:
        j=garbageModels.Jugador.objects.get(id=idJ)
    except garbageModels.Jugador.DoesNotExist:
        raise Http404
    

    
    return render_to_response('kml.xml',{'SERVER_NAME':'http://%s'%(request.META['HTTP_HOST'])}, context_instance=RequestContext(request),mimetype='text/xml; charset=utf-8')

    if not idJ:
        
        
        iserv="""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0" xmlns:fs="http://featureserver.com/ns" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
<atom:link rel="self" href="http://dev1.ghost.webhop.org/data/kml/5" type="application/vnd.google-earth.kml+xml" /> 
<Style id="PepitaIcon">
<IconStyle>
<Icon>
<href>http://dev1.ghost.webhop.org/static/media/kml/puntos.png</href>
</Icon>
</IconStyle>
</Style>    
</Document>
        </kml>"""
        return HttpResponse(iserv,mimetype='text/xml; charset=utf-8')

    j=garbageModels.Jugador.objects.get(id=idJ)
    
   
    puntos=""
    for i in j.getPuntos():
        puntos+="""
<Placemark>
<styleUrl>#PepitaIcon</styleUrl>
 <Point>
 <coordinates>%f,%f</coordinates>
</Point>
<name>Pepita</name>
<description>TESTES</description>
</Placemark>
"""%(i.georef.x,i.georef.y)

    

    iserv="""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0" xmlns:fs="http://featureserver.com/ns" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
<atom:link rel="self" href="http://dev1.ghost.webhop.org/data/kml/5" type="application/vnd.google-earth.kml+xml" /> 
<Style id="PepitaIcon">
<IconStyle>
<Icon>
<href>http://dev1.ghost.webhop.org/static/media/kml/puntos.png</href>
</Icon>
</IconStyle>
</Style>    
%s
</Document>
        </kml>"""%puntos
            
    return HttpResponse(iserv,mimetype='text/xml; charset=utf-8')
        
    

