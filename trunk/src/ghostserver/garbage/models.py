# -*- coding: utf-8 -*-
fr django.db import models
from ghost import models as ghostModels
from geolbs import models as geolbsModels
from django.contrib.contenttypes import generic




class Juego(models.Model):
    """Juego que posee los diferentes Jugadores y Servicios
    
    """
    name = models.CharField(max_length=30)
    

    class Meta:
        verbose_name_plural='Features del Juego'
    
    def __unicode__(self):
        return u"%s" % (self.nombre)



class Jugador(models.Model) :
    """Posee todos los atributos y las especificaciones del jugador
       dentro de un juego específico esto permitirá tener varios juegos
       y en cada uno de ellos puede tener un roll diferente.
    """
    nickname = models.CharField(max_length=40,blank=True,null=True)
    persona = models.ForeignKey(ghostModels.Personas)
    juego = models.ForeignKey(Juego)
    

    class Meta:
        verbose_name_plural='Jugador'
    
    def __unicode__(self):
        return u"%s" % (self.nickname or self.persona.user.username)

    




class TypesFeatures(models.Model):
    """Tipos de Caracteristicas que se pueden adicionar
       estas clases son stats poderes 

    """
    nombre = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural='Tipos de Features'
    
    def __unicode__(self):
        return u"%s" % (self.nombre)
    

    

class Features(models.Model):
    """Caracteristicas son las caracteristicas que puede tener el jugador y que representan
    
    """
    nombre = models.CharField(max_length=30)
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


    class Meta:
        verbose_name_plural='Servicios del Juego'
    
    def __unicode__(self):
        return u"%s" % (self.service)







class FeaturesPlay(models.Model):
    """Caracteristicas son las caracteristicas que puede tener el jugador y que representan
    
    """
    feature = models.ForeignKey(Features)
    jugador = models.ForeignKey(Jugador)
    service = models.ForeignKey(ServicePlay)

    class Meta:
        verbose_name_plural='Features del Juego'
    
    def __unicode__(self):
        return u"%s" % (self.feature)
    


