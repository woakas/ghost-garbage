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



@login_required
def position_mobile(request,lon,lat):
    p=request.user.personas_set.all()
    if p>0:
        p=p[0]
        j=p.jugador_set.get(juego=garbageModels.Juego.objects.get(name='GhostGarbage'),persona=p)
        if j.updatePosition(lon,lat):
            return HttpResponse(str({'status':'OK'}))

    return HttpResponse(str({'status':'ERROR'}))





