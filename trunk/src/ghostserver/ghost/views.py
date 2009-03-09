# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

import settings
from ghost import forms
from ghost import models as ghostModels
from ghost.constsappli import *



def entry(request):
    """Vista para Autenticación de usuarios si el usuario es valido se determina la pagina de entrada para su preferencias"""
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['usuario'], password=form.cleaned_data['clave'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.GET.keys() :
                        return HttpResponseRedirect(settings.URL_PREFIX+request.GET['next'][1:])
                    a=ghostModels.PreferenciasUsuarios.objects.filter(preferencia=ghostModels.Preferencias.objects.get(nombre='paginaentrada'),usuario=user)
                    if a.count()==0:
                        logon=DEFAULTLOGON
                    else:
                        logon=a[0].valor
                
                    return HttpResponseRedirect(settings.URL_PREFIX+logon)
                else :
                    return render_to_response('entry.html', {'form': form },context_instance=RequestContext(request))
            else:
                return render_to_response('entry.html', {'form': form },context_instance=RequestContext(request))
    else:
        if request.user.is_authenticated():
            #If the user is authenticated we won't show the login form, we redirect to the preferences homepage
            print DEFAULTLOGON
            a=ghostModels.PreferenciasUsuarios.objects.filter(preferencia=ghostModels.Preferencias.objects.get(nombre='paginaentrada'),usuario=request.user)
            if a.count()==0:
                logon=DEFAULTLOGON
            else:
                logon=a[0].valor
            return HttpResponseRedirect(settings.URL_PREFIX+logon)
        form = forms.LoginForm()
    return render_to_response('entry.html', {'form': form},context_instance=RequestContext(request))



def index(request):
    """
       Información sobre el Juego
    """
    form = forms.LoginForm()

    return render_to_response('index.html',{'form': form},context_instance=RequestContext(request))
    
