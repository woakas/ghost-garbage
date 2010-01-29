# -*- coding: utf-8 -*-
from django.db import models
from ghost import models as ghostModels
from geolbs import models as geolbsModels
from django.contrib.contenttypes import generic


CHOICES_STATUS=[(1,'On Line'),(2,'Off Line')]

class Juego(models.Model):
    """Juego que posee los diferentes Jugadores y Servicios
    
    """
    name = models.CharField(max_length=30)
    

    class Meta:
        verbose_name_plural='Juegos'
    
    def __unicode__(self):
        return u"%s" % (self.name)



class Jugador(models.Model) :
    """Posee todos los atributos y las especificaciones del jugador
       dentro de un juego específico esto permitirá tener varios juegos
       y en cada uno de ellos puede tener un roll diferente.
    """
    nickname = models.CharField(max_length=40)
    persona = models.ForeignKey(ghostModels.Personas)
    juego = models.ForeignKey(Juego)
    status = models.IntegerField(choices=CHOICES_STATUS, default=2)
    position = models.ForeignKey(geolbsModels.Punto)
    

    class Meta:
        verbose_name_plural='Jugador'



    def updatePosition(self,lon,lat):
        return self.position.updateGeoref(lon,lat)
    
    def __unicode__(self):
        return u"%s" % (self.nickname or self.persona.user.username)

    




class TypesFeatures(models.Model):
    """Tipos de Caracteristicas que se pueden adicionar
       estas clases son stats poderes 

    """
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(blank=True,null=True)
    
    class Meta:
        verbose_name_plural='Tipos de Features'
    
    def __unicode__(self):
        return u"%s" % (self.nombre)
    

    

class Features(models.Model):
    """Caracteristicas son las caracteristicas que puede tener el jugador y que representan
    
    """
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50)
    clase = models.ForeignKey(TypesFeatures)
    logica = models.TextField()


    class Meta:
        verbose_name_plural='Features'
    
    def __unicode__(self):
        return u"%s" % (self.nombre)
    




class ServicePlay(models.Model):
    """Servicios en Juego 

    """
    service = models.ForeignKey(geolbsModels.Service)
    juego = models.ForeignKey(Juego)
    lugar =models.ForeignKey(geolbsModels.Lugares)
    variables = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name_plural='Servicios del Juego'
    
    def __unicode__(self):
        return u"%s" % (self.service)





class FeatureServicePlay(models.Model):
    """
    
    """
    feature = models.ForeignKey(Features,blank=True,null=True)
    jugador = models.ForeignKey(Jugador,blank=True,null=True)
    service = models.ForeignKey(ServicePlay,blank=True,null=True)
    variables = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name_plural='Feature Service del Juego'
    
    def __unicode__(self):
        return u"%s" % (self.feature)
    


