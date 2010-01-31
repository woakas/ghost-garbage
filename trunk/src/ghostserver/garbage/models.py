# -*- coding: utf-8 -*-
from django.db import models
from ghost import models as ghostModels
from geolbs import models as geolbsModels
from django.contrib.contenttypes import generic



CHOICES_STATUS=[(1,'Vivo'),(2,'Muerto'),(3,'Off Line')]
DISTANCE_MIN=40


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
        """ Actualiza la posición de un jugador, si la posición se
            encuentra en un rango menor a DISTANCE_MIN la posición es
            actualizada de lo contrario no acutalizará la posición ni
            los servicios asociados.
        
        """
        gp=geolbsModels.geos.Point(float(lon),float(lat))
        dd=geolbsModels.Punto.objects.distance(gp).get(id=self.position.id)
        if dd.distance.m<=DISTANCE_MIN or self.position.georef.coords==(0,0):
            msT=self.updateServiceLbs()
            msT['position_update']=self.position.updateGeoref(gp)
            return msT
        
        return {'position_update':False}
        

    def updateServiceLbs(self):
        """ Actualiza los servicios y realiza los triggers respectivos para los
            servicios
        """
        ms={}
        pp=geolbsModels.Punto.objects.filter(georef__distance_lte=(self.position.georef,geolbsModels.D(m=500)),lugares__isnull=False).values_list('id',flat=True)
        for sp in  ServicePlay.objects.filter(lugar__punto__id__in=list(pp)):
            ms.update(sp.triggerService(self))
        return ms


    def getFeaturePlay(self,feature,list=False):
        """ Retorna el Feature o Features que el jugador tiene
            si se envia el parámetro list retornará todos los features
            que posea este jugador con dicho nombre
        """
        try:
            ft=Features.objects.get(nombre=feature)
        except:
            if list:
                return []
            return None
        
        fs=FeatureServicePlay.objects.filter(jugador=self,feature=ft)
        
        if len(fs)>0 and list==False:
            return fs[0]
        return fs
        

    
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
    nombre = models.CharField(max_length=30,unique=True)
    descripcion = models.CharField(max_length=50)
    clase = models.ForeignKey(TypesFeatures)
    logica = models.TextField()


    class Meta:
        verbose_name_plural='Features'


    def __evalLogica__(self,body='',**kargs):
        vr=locals() # Variables Locales que se encuentran dentro de la función
        vr.update(kargs)
        vr.update(globals()) # Variables Globales y se agregan a vr


        logic=self.logica.replace('\r','')
        logic+='\n%s'%body
        exec logic in vr # Se ejecuta body con exec y se pasan como parametro vr para tener consistencia con todas las variables.

        return out
        

        try:
            logic=self.logica.replace('\r','')
            logic+='\n%s'%body
            exec logic in vr # Se ejecuta body con exec y se pasan como parametro vr para tener consistencia con todas las variables.
            return out
        except:
            return None


    def __getValue__(self,**kargs):
        return self.__evalLogica__('out=getValue()',**kargs)

    def __setValue__(self,pnt=0,**kargs):
        return self.__evalLogica__('out=setValue(%d)'%pnt,**kargs)


    
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
        
    def __evalLogica__(self,body=''):
        try:
            exec self.variables
        except:
            pass
        vr=locals()
        del(vr['body'])
        del(vr['self'])
        return self.service.__evalLogica__(body,**vr)


    def identifyService(self):
        return self.service.identifyService()
    
    def triggerService(self,jugador=None):
        try:
            exec self.variables.replace('\r','')
        except:
            pass
        r=locals()
        del(r['jugador'])
        del(r['self'])
        return self.service.triggerService(jugador,**r)
    
    
    def __unicode__(self):
        return u"%s en %s para el juego %s" % (self.service,self.lugar, self.juego)





class FeatureServicePlay(models.Model):
    """
    
    """
    feature = models.ForeignKey(Features,blank=True,null=True)
    jugador = models.ForeignKey(Jugador,blank=True,null=True)
    service = models.ForeignKey(ServicePlay,blank=True,null=True)
    variables = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name_plural='Feature Service del Juego'


    def __func_features__(self,func,**kargs):
        """ Función que llama a la función dada de Feature
            y retorna su contenido aplicando las variables
        """
        try:
            exec self.variables.replace('\r','')
        except:
            pass
        featurePlay=self
        r=locals()
        r.update(kargs)
        del(r['self'])
        return  Features.__dict__[func].__call__(self.feature,**r)


    def getValue(self):
        return self.__func_features__('__getValue__')


    def setValue(self,pnt):
        return self.__func_features__('__setValue__',pnt=pnt)
  
    
    def __unicode__(self):
        return u"%s" % (self.feature)
    


