#!/usr/bin/python
# -*- coding: utf-8 -*-
from importutils import  *
from sys import argv

#Converter is an array that must be filled with tuples of the form :
#Name of the class, file containing the info , preprocessing , structure of constructor
#This is the simplest.
#The second form of the tuple has a fifth argument that states the preprocessing of the information to look for example in other tables.
#Take a look at Lugares, ciudades.csv
#The third form of the tuple has a sixth argument that states from which column the data is to be inserted as a new record.
#Take a look at tiposfasecolda.csv

#General Data
converter=[
("MenuPrincipal","menuppal.csv","","Menu(name='%s',url='%s',desc='%s',posicion=%s)"),
("SubMenus","submenus.csv","pa=Menu.objects.get(name='%s')","Menu(name='%s',url='%s',desc='%s',padre=pa,posicion=%s)",[0],1),
("Preferencias","preferencias.csv","","Preferencias(nombre='%s',descripcion='%s')"),
("FlatPages","flatpages.csv","s=Site.objects.get(id=SITE_ID)","s.flatpage_set.create(url='%s',title='%s',template_name='%s',registration_required=%s)"),
("TypesFeatures","typesfeatures.csv","","TypesFeatures(nombre='%s',descripcion='%s')"),
("TypesServices","typesservices.csv","","TypesService(nombre='%s',descripcion='%s',logica='%s')"),
#("shape","country.shp","Poligono","{'nombre':'CNTRY_NAME','tipolugar':{'nombre':'TIPOLUGAR'},'dentrode':{'nombre':'PLANETA'}}"),
]



addons=[
('rawOSMBeta',"osm_add_postgis",'from django.contrib.gis.gdal import SpatialReference\n\tfrom django.contrib.gis.utils import add_postgis_srs\n\tadd_postgis_srs(SpatialReference(900913)) '),
]


#User's Grants first the name of the group, second an array with the permissions, third
#an array with the actual urls that make the menu entries be visible.
permissions=[
    ["Anonymus",["anonymus"],["Index","Sobre","Usuario|Registrar","Usuario|Entrar","Usuario|Nueva Contraseña"]],
    ["Jugador",["jugador"],["Index","Sobre","Usuario|Cambiar Contraseña","Usuario|Salida","Juego"]],
    #["supervisorInstalacionesMig",["instalar", "modificar_instalacion","eliminar_instalacion","reporte_instalacion"],["Instalación"]]
    ]

if __name__ == '__main__':
    data=[converter, addons]
    complete(data,permissions)
    createMain()
