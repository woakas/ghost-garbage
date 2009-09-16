# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class TiposLugar(models.Model) :
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True )
    
    class Meta:
        verbose_name_plural='Tipos de lugar'

    def __unicode__(self):
        return u"%s" % (self.nombre)


class Lugares(models.Model) :
    nombre = models.CharField(max_length=80)
    tipolugar = models.ForeignKey(TiposLugar)
    dentrode = models.ForeignKey('self',null=True,blank=True)
    #fotos = models.ManyToManyField(Fotos, null=True, blank=True)

    content_type = models.ForeignKey(ContentType,null=True,blank=True)
    object_id = models.PositiveIntegerField(null=True,blank=True)
    content_object = generic.GenericForeignKey()

    class Meta:
        verbose_name_plural='Lugares'

 
    def __unicode__(self):
        if self.dentrode is None:
            return u"%s" % (self.nombre)
        return u"%s(%s)" % (self.nombre,self.dentrode.nombre)


class Punto(models.Model):
    georef = models.PointField(srid=4326)
    lugares = generic.GenericRelation(Lugares)
    objects =models.GeoManager()

    class Meta:
        verbose_name_plural='Lugares con Punto'


    def __unicode__(self):
        lug=self.lugares.filter()
        if len(lug)==0:
            return u"Punto sin Lugar especificado"
        else:
            return u"%s" % (', '.join(map(lambda x: x.__unicode__(), lug)))
        
    
class Poligono(models.Model):
    georef = models.MultiPolygonField(srid=4326)
    lugares = generic.GenericRelation(Lugares)
    objects =models.GeoManager()


    class Meta:
        verbose_name_plural='Lugares con Poligonos'


    def __unicode__(self):
        lug=self.lugares.filter()
        if len(lug)==0:
            return u"Poligono sin Lugar especificado"
        else:
            return u"%s" % (', '.join(map(lambda x: x.__unicode__(), lug)))

        
class Linea(models.Model):
    georef = models.MultiLineStringField(srid=4326)
    lugares = generic.GenericRelation(Lugares)
    objects =models.GeoManager()


    class Meta:
        verbose_name_plural='Lugares con Lineas'


    def __unicode__(self):
        lug=self.lugares.filter()
        if len(lug)==0:
            return u"Linea sin Lugar especificado"
        else:
            return u"%s" % (', '.join(map(lambda x: x.__unicode__(), lug)))



class TypesService(models.Model):
    """Tipos de Servicio asiciado directamente a la lógica del como
       funciona el servicio
    """
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    logica = models.TextField()
    
    class Meta:
        verbose_name_plural='Tipos de Servicio'

    def __unicode__(self):
        return u"%s" % (self.nombre)


class Service(models.Model):
    tipo =models.ForeignKey(TypesService)
    lugar =models.ForeignKey(Lugares)
    
    class Meta:
        verbose_name_plural='Servicios'

    def __unicode__(self):
        return u"%s en %s" % (self.tipo,self.lugar)
