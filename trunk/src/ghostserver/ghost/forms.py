# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    """Lets the user log in
    TO BE done, redirect the user if is already logged in to a proper page"""
    usuario = forms.CharField(max_length=20,error_messages={'required': 'Por favor ingrese el nombre de usuario.'})
    w=forms.PasswordInput(render_value=False)
    clave = forms.CharField(max_length=20,widget=w,error_messages={'required': 'La contraseña es obligatoria'})
    
    def clean_clave (self):
        if self.cleaned_data['usuario'] is None or self.cleaned_data['clave'] is None or len(self.cleaned_data['usuario'])==0  or len(self.cleaned_data['clave'])==0:
            raise forms.ValidationError(u'Error de autenticación, usuario no válido.')
        user = authenticate(username=self.cleaned_data['usuario'], password=self.cleaned_data['clave'])
        if user is None:
            raise forms.ValidationError(u'Error de autenticación, clave no válida.')
        return self.cleaned_data['clave']
