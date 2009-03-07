# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User,Group
from ghost.constsappli import *

class Menu(models.Model) :
    name = models.CharField(max_length=40)
    url = models.CharField(max_length=100, unique=True)
    desc = models.CharField(max_length=1000, null=True ,blank=True)
    padre = models.ForeignKey('self',null=True, blank=True)
    posicion  = models.IntegerField()

    class Meta:
        verbose_name_plural='Menús'
    
    def __unicode__(self):
        if not self.padre is None:
            return u"%s - %s" % (self.padre.name,self.name)
        return u"%s" % (self.name)


class Personas(models.Model) :
    nombre = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=40)
    docid = models.CharField(max_length=30)
    correo = models.CharField(max_length=100, blank = True )
    movil = models.CharField(max_length=100, blank =True )
    telefono = models.CharField(max_length=50, blank = True )
    user = models.ForeignKey(User,null= True)
    foto = models.ImageField(upload_to='images/people',blank=True)
    sexo = models.IntegerField(choices=CHOICES_TYPE_SEX)
    menus = models.ManyToManyField(Menu,blank=True)

    class Meta:
        verbose_name_plural='Personas'
        

    def __unicode__(self):
        return u"%s %s [%s]" % (self.nombre,self.apellidos,self.docid) 
  

class Perfiles(models.Model) :
    grupo = models.ForeignKey(Group)
    descripcion = models.CharField(max_length=1000)
    menus = models.ManyToManyField(Menu)


    class Meta:
        verbose_name_plural='Perfiles'

    def __unicode__(self):
        return u"%s" % (self.grupo)

class Preferencias(models.Model) :
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural='Preferencias'

    def __unicode__(self):
        return u"%s" % (self.nombre)


class PreferenciasUsuarios(models.Model) :
    usuario = models.ForeignKey(User)
    valor = models.CharField(max_length=200, null=True )
    preferencia = models.ForeignKey(Preferencias)


    class Meta:
        verbose_name_plural='Preferencias de Usuario'

    def __unicode__(self):
        return u"%s : %s" % (self.preferencia,self.valor)


