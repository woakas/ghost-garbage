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
]



addons=[
('rawOSMBeta',"osm_add_postgis",'from django.contrib.gis.gdal import SpatialReference\n\tfrom django.contrib.gis.utils import add_postgis_srs\n\tadd_postgis_srs(SpatialReference(900913)) '),
]


#User's Grants first the name of the group, second an array with the permissions, third
#an array with the actual urls that make the menu entries be visible.
permissions=[
	     #["instaladorMig",["instalar"],["Instalación|Realizar una Instalación"]],
             #["supervisorInstalacionesMig",["instalar", "modificar_instalacion","eliminar_instalacion","reporte_instalacion"],["Instalación"]]
             ]

if __name__ == '__main__':
    data=[converter, addons]
    complete(data,permissions)
