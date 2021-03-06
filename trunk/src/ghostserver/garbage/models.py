# -*- coding: utf-8 -*-
from django.db import models
from ghost import models as ghostModels
from geolbs import models as geolbsModels
from django.contrib.contenttypes import generic



CHOICES_STATUS=[(1,'Vivo'),(2,'Muerto'),(3,'Off Line')]
CHOICES_STATUS_SERVICE_PLAY=[(1,'Activo'),(2,'Inactivo')]
DISTANCE_MIN=40

class Juego(models.Model):
    """Juego que posee los diferentes Jugadores y Servicios
    
    """
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural='Juegos'
    
    def __unicode__(self):
        return u"%s" % (self.name)




class JugadorManager(models.Manager):
    """ Manager para Jugador
    """
    def getJugadores(self,point,distance=0,**kargs):
        """ Retorna los jugadores dados en un rango de distancia 
            un punto
        """
        rgs={}
        rgs['georef__distance_lte']=(point,geolbsModels.D(m=distance))
        rgs['jugador__isnull']=False
        rgs.update(kargs)
        j_ids=geolbsModels.Punto.objects.filter(**rgs).values_list("id",flat=True)
        
        return self.filter(position__id__in=list(j_ids))



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

    objects=JugadorManager()


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
            msT={}
            msT['position_update']=self.position.updateGeoref(gp)
            msT.update(self.updateServiceLbs())
            return msT
        
        return {'position_update':False}
        

    def updateServiceLbs(self):
        """ Actualiza los servicios y realiza los triggers respectivos para los
            servicios
        """
        ms={}
        for sp in self.getServicesVisibles():
            ms.update(sp.triggerService(self) or {})
        ms.update(self.updateJugadores() or {})
        return ms



    def updateJugadores(self):
        """ Actualiza los servicios y realiza los triggers respectivos para los
            servicios
        """
        ms={}
        for jj in self.getJugadoresVisibles().exclude(id=self.id):
            for fsp in jj.featureserviceplay_set.filter():
                ms.update(fsp.triggerFeature(self) or {})
        return ms


    def getFeaturePlay(self,feature=None,list=False,all=False):
        """ Retorna el Feature o Features que el jugador tiene
            si se envia el parámetro list retornará todos los features
            que posea este jugador con dicho nombre
        """
        if not all:
            try:
                ft=Features.objects.get(nombre=feature)
            except:
                if list:
                    return []
                return None
            fs=FeatureServicePlay.objects.filter(jugador=self,feature=ft)
        else:
            fs=FeatureServicePlay.objects.filter(jugador=self)
            list=True
        
        if len(fs)>0 and list==False:
            return fs[0]
        elif list==False:
            return None
        return fs


    def getValue(self,feature,default=None):
        """Retorna el valor de un feature dado si este no existe 
           se retorna lo que se tenga por default
        """
        value=self.getFeaturePlay(feature)
        if value:
            return value.getValue()
        return default


    def getVariable(self,variable,feature=None,default=None):
        fsps=self.getFeaturePlay(all=True)
        for fsp in fsps:
            r=fsp.getVariable(variable)
            if r:
                return r
        return default
            

    def getServicesVisibles(self):
        """Retorna los Servicios Visibles para el Jugador
        """
        dis= self.getValue('Vision',Features.objects.get(nombre="Vision").defaultValue())
        return ServicePlay.objects.getServices(self.position.georef,dis).filter(juego=self.juego)


    def getJugadoresVisibles(self):
        """Retorna los Jugadores Visibles para el Jugador
        """
        dis= self.getValue('Vision',Features.objects.get(nombre="Vision").defaultValue())
        return Jugador.objects.getJugadores(self.position.georef,dis).filter(juego=self.juego)


    def getPuntosLte(self,distance):
        """Retorna los puntos cercanos menores a una distacia determinada en metros
        """
        pn=geolbsModels.Punto.objects.filter(georef__distance_lte=(self.position.georef,geolbsModels.D(m=distance)),lugares__isnull=False)
        return pn
    

    def identifyServices(self):
        """Realiza la identificación de los servicios visibles
        """
        ms=[]
        dis= self.getValue('Vision',Features.objects.get(nombre="Vision").defaultValue())
        pn=self.getPuntosLte(dis).distance(self.position.georef)
        
        for i in pn:
            sp=i.lugares.get().serviceplay_set.filter()
            if len(sp)>0 and sp[0].status ==1:
                serv=sp[0].identifyService(jugador=self)
                if serv:
                    ms.append((serv,i.distance,sp[0].service.icon.name))
        return ms



    def getPlaceMarks(self,json=False):
        """ Retorna un diccionario con el atributo nombre, descripcion,
            icon y geo para la generación de KML o algún otro servicio.
        """
        spp=self.getServicesVisibles().filter(status=1)
        attrs=[]
        for sp in spp:
            if sp.identifyService(jugador=self):
                tr={
                    'nombre':sp.service.nombre,
                    'style':sp.service.icon.name.split('/')[-1].replace('.png','').capitalize(),
                    'id':'%s_%d'%(sp.service.nombre.replace(' ',''),sp.id),
                    'status':True,
                    }
                if json:
                    tr['lon']=sp.lugar.content_object.georef.x
                    tr['lat']=sp.lugar.content_object.georef.y
                    tr['icon']=sp.service.icon.name.replace('media','') 
                else:
                    tr['descripcion']=sp.service.descripcion
                    tr['geo']=sp.lugar.content_object.georef
                    tr['icon']=sp.service.icon.name
                    
                attrs.append(tr)

        #fsp_id=FeatureServicePlay.objects.filter(feature=Features.objects.get(nombre="Tipo Jugador"),variables=self.getFeaturePlay('Tipo Jugador').variables).values_list("id",flat=True)
        
        for j in self.getJugadoresVisibles():#.exclude(id=self.id):
            fsp=j.getFeaturePlay('Tipo Jugador')
            tr={
                'nombre':j.nickname,
                'style':fsp.getVariable("icono").split('/')[-1].replace('.png','').capitalize(),
                'id':'%s_%d'%(fsp.getValue(),j.id),
                }
            
            if json:
                rr=fsp.getVariable("icono").replace('media','')
                tr['lon']=j.position.georef.x
                tr['lat']=j.position.georef.y
                tr['icon']=j.status==1 and rr or rr.replace('.png','_disable.png') 
            else:
                tr['descripcion']="Jugador %s"%j.nickname
                tr['geo']=j.position.georef
                tr['icon']=fsp.getVariable("icono")
                tr['status']=j.status==1 and True or False
            attrs.append(tr)        
        return attrs
        

    
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

    def __getVariable__(self,variable=None,**kargs):
        return self.__evalLogica__('out=locals().get("%s",None)'%variable,**kargs)


    def __triggerFeature__(self,jugador,jugAccess,**kargs):
        return self.__evalLogica__('out=triggerFeature(jugador,jugAccess)',jugador=jugador,jugAccess=jugAccess,**kargs)


    def defaultValue(self,**kargs):
        return self.__evalLogica__('out=defaultValue()',**kargs)


    
    def __unicode__(self):
        return u"%s" % (self.nombre)
    

class ServicePlayManager(models.Manager):
    """ Manager para Servicios en Juego
    """

    def getServices(self,geo,distance=0):
        l_ids=geolbsModels.Lugares.objects.getLugares(geo,distance).values_list("id",flat=True)
        return self.filter(lugar__id__in=list(l_ids))
    

class ServicePlay(models.Model):
    """Servicios en Juego 

    """
    service = models.ForeignKey(geolbsModels.Service)
    juego = models.ForeignKey(Juego)
    lugar =models.ForeignKey(geolbsModels.Lugares)
    variables = models.TextField(blank=True,null=True)
    status = models.IntegerField(choices=CHOICES_STATUS_SERVICE_PLAY, default=1)
    
    objects =ServicePlayManager()

    class Meta:
        verbose_name_plural='Servicios en Juego'
        
    def __func_services__(self,func,**kargs):
        """ Función que llama a la función dada de Service
            y retorna su contenido aplicando las variables
        """
        try:
            exec self.variables.replace('\r','')
        except:
            pass
        servicePlay=self
        r=locals()
        r.update(kargs)
        del(r['self'])
        return geolbsModels.Service.__dict__[func].__call__(self.service,**r)


    
    def triggerService(self,jugador,**kargs):
        """ Llama el trigger del servicio asociado asociado a un jugador
        """
        return self.__func_services__('triggerService',jugador=jugador,**kargs)


    def identifyService(self,**kargs):
        """ Retorna el identify Del servicio en juego
        """
        return self.__func_services__('identifyService',**kargs)


    def getService(self,jugador,feature=None,attr=None,**kargs):
        """ Retorna el identify Del servicio en juego
        """
        return self.__func_services__('getService',jugador=jugador,feature=feature,attr=attr,**kargs)


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


    def getVariable(self,variable):
        return self.__func_features__('__getVariable__',variable=variable)


    def setValue(self,pnt):
        return self.__func_features__('__setValue__',pnt=pnt)


    def triggerFeature(self,jugador,**kargs):
        """ Llama el trigger del servicio asociado asociado a un jugador
        """
        return self.__func_features__('__triggerFeature__',jugador=self.jugador,jugAccess=jugador,**kargs)


  
    
    def __unicode__(self):
        return u"%s" % (self.feature)
    

