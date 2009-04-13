# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required

import settings
from geolbs import models as geolbsModels


@login_required
def index(request):
    """
       Información sobre el Juego
    """

    return render_to_response('geolbs.html',context_instance=RequestContext(request))
    


@permission_required('geolbs.addAtributo')
def addAtributo(request):
    """
       Permite adicionar un Atributo
    """

    return render_to_response('geolbs.html',context_instance=RequestContext(request))
    


