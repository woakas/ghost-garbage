# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.urlresolvers import reverse


import settings
from ghost import forms
from ghost import models as ghostModels
from ghost.constsappli import *







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
