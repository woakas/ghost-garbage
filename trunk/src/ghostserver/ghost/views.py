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
        return render_to_response('user.html',context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('auth_login'))
    





def login_mobile(request):
    response = HttpResponse()
    if not request.user.is_authenticated():
        response.status_code = 401
        return response
    
    response.status_code = 200
    return response
