# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from ghost.constsappli import *


from ghost import models as ghostModels



class ActiveUserForm(forms.Form):
    nombre = forms.CharField(label="* Nombre", required=True)
    apellido = forms.CharField(label="* Apellidos", required=True)
    movil= forms.IntegerField(required=False)
    telefono = forms.IntegerField(required=False)
    url= forms.URLField(required=False)
    sexo =forms.IntegerField(widget=forms.Select(choices=CHOICES_TYPE_SEX),initial=1)
    



class UserForm(forms.Form):
    image = forms.ImageField(label="Change Avatar...", required=True)
