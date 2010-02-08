# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.urlresolvers import reverse

import settings

#Importes de ghost
from ghost import forms
from ghost import models as ghostModels
from ghost.constsappli import *

#Importes otros
from garbage import models as garbageModels
from geolbs import models as geolbsModels

#Importación de Registration
from registration.models import RegistrationProfile




def activate_user(request,activation_key):
    """Activate a User with Profile.
    """
    if len(RegistrationProfile.objects.filter(activation_key=activation_key))<1:
        return render_to_response('error.html',context_instance=RequestContext(request))
    
    if request.method == 'POST':
        form=forms.ActiveUserForm(request.POST)
        if form.is_valid():
            activation_key = activation_key.lower() # Normalize before trying anything with it.
            account = RegistrationProfile.objects.activate_user(activation_key)
            ff=form.cleaned_data
            user=ghostModels.Personas.objects.create(nombre=ff['nombre'],apellidos=ff['apellido'],movil=ff['movil'],telefono=ff['telefono'],url=ff['url'],sexo=ff['sexo'],user=account)
            user.user.groups.add(ghostModels.Group.objects.get_or_create(name=GROUPDEFAULT)[0])
            return render_to_response('registration/activate.html',{ 'account': account,'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },context_instance=RequestContext(request))

        else:   
            return render_to_response('activate_user.html', {'form': form },context_instance=RequestContext(request))
    form=forms.ActiveUserForm()
    
    return render_to_response('activate_user.html',{'form': form }, context_instance=RequestContext(request))

  



def profile(request):
    """Opciones de Usuario
    """
    if request.user.is_authenticated():
        p=request.user.personas_set.all()
        if len(p)>0:
            p=p[0]
            j=p.jugador_set.filter(juego=garbageModels.Juego.objects.get(name='GhostGarbage'),persona=p)
            
            if len(j)>0:
                j=j[0]
            else:
                pp=geolbsModels.Punto(georef="POINT(0 0)");
                pp.save()
                j=p.jugador_set.create(juego=garbageModels.Juego.objects.get(name='GhostGarbage'),persona=p,position=pp,nickname=request.user.username)
        else:
            p=None
            j=None
        if request.method=='POST':
            form=forms.UserForm(request.POST)
            if form.is_valid():
                pass
        else:
            form=forms.UserForm()

        return render_to_response('user.html',{'user':request.user,'persona':p,'jugador':j,'form':form},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('auth_login'))
    





def login_mobile(request):
    response = HttpResponse()
    #print request
    if not request.user.is_authenticated():
        response.status_code = 401
        return response
    
    response.status_code = 200
    return response
