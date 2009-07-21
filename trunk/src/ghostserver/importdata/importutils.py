#!/usr/bin/python -*- coding: utf-8 -*-
import csv
dir_data="../../data/csv/"
dir_data_shapes="../data/shapes/"
funcs = []



def genFromCsv(filler):
    """
    """
    reader = csv.reader(open(dir_data+filler[1], "rb"),delimiter="|")
    print "#Filling %s with info from file %s" % (filler[0],filler[1]),
    print """\ndef %s():""" % filler[1].replace(".csv","").replace("/","_")

    if len(filler)==4:
        print "\t%s" % filler[2]
    for row in reader:
        
        if len(filler)==4:
            #Type one of tuple preprocessing of fixed data
            a="\tnewdata="+(filler[3] % tuple([i.strip() for i in row])) + ";newdata.save()"
        else :
            #Type two, it has an additional argument that states the
            fromind=0
            if len(filler)>5:
                #Type trhee, it has six arguments, the last one tells where to start the args to INSERT
                fromind=filler[5]
            a="\t"+(filler[2] % tuple([row[i] for i in filler[4]]))+"\n\tnewdata="+(filler[3] % tuple([row[i].strip() for i in range(fromind,len(row))])) + ";newdata.save()"
        print a
    print "\n"



def genFromRaw(filler):
    """Genera una fución e inserta el texto tal cual se necesitó para la inserción.
    """
    print "\ndef %s():" % filler[1]
    print "\t%s"% filler[2]
    print "\n"


def genFromShp(filler):
    """Genera la función para la creación y la inserción de datos desde un shape con LayerMapping
    """
    print "\ndef %s():" % filler[1].replace(".shp","")
    print "\tmapping={'georef':'POLYGON'}"
    print "\tmapp=%s" % (filler[3])
    if len(filler)>4:
        print "\taddShape(mapp,%s,\'%s\', mapping,source_srs='%s')"% (filler[2],dir_data_shapes+filler[1],filler[4])
    else:
        print "\taddShape(mapp,%s,\'%s\', mapping)"% (filler[2],dir_data_shapes+filler[1])

    print "\n"



def createimport(mydict):
    """Gets an array with the structure of converter, please see above and throws
    to standard output the info gathered from files on my dict, according to the
    code of python put on mydict.
    Converter is an array that must be filled with tuples of the form :
    Name of the class, file containing the info , preprocessing , structure of constructor
    This is the simplest.
    The second form of the tuple has a fifth argument that states the preprocessing of the information to look for example in other tables.
    Take a look at Lugares, ciudades.csv
    The third form of the tuple has a sixth argument that states from which column the data is to be inserted as a new record.
    Take a look at tiposfasecolda.csv
    """
    
    global funcs

    for filler in mydict :
        funcs.append (filler[1])
        if filler[0].startswith("shape") :
            genFromShp(filler)
        elif filler[0].startswith("raw") :
            genFromRaw(filler)
        else:
            genFromCsv(filler)


def theperms(groups,funname="g1") :
    """Gets an array of arrays, each one contains as first parameter the name
    of the group, and the permissions it has as the other parameters

    """
    print "def %s():" % funname
    for group in groups:
        a="\tg=Group(name='%s')\n\tg.save()" % group[0]
        #for i in group[1]:
        #    a+="\n\tg.permissions.add(Permission.objects.get(codename='%s'))" % i
        if len(group[2]):
            a+="\n\tperf=Perfiles(grupo=g,descripcion='%s');perf.save()" % group[0]
            for i in group[2]:
                tp=tuple(i.split("|"))
                if len(tp)==1:
                    a+="\n\tperf.menus.add(Menu.objects.get(padre=None,name='%s'))" % tp
                else:
                    a+="\n\tperf.menus.add(Menu.objects.get(padre=Menu.objects.get(name='%s'),name='%s'))" % tp
        print a




def complete(data,permissions,additionallibs="""from ghost.models import *
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group, Permission
from django.contrib.gis.utils import LayerMapping
import datetime
"""):
    """data is a list of list of tuples described on createimport
    permissions is a list of lists described on the perms
    additonallibs is the python code necessary for your importer to work, for
    example add "from ghost.models import *"...
    http://code.djangoproject.com/wiki/InitialSQLDataDiangoORMWay
    Adding the data with python install.py"""
    print """#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *

"""+additionallibs+"""
def addShape(mapp, *args, **kwargs):
    lm=LayerMapping(*args,**kwargs)
    for i in lm.layer:
        lm.save(fid_range=(i.fid,i.fid+1))
        ll=lm.model.objects.latest('id')
        kw={}
        for key, value in mapp.items():
            if isinstance(value,dict):
                rel_model=Lugares._meta.get_field(key).rel.to
                kk={}
                for ky, vy in value.items():
                    kk[ky]=vy.startswith('__') and vy.replace('__','') or i.get(vy)
                kw[key]=rel_model.objects.get(**kk)
            else:
                kw[key]=i.get(value)
        ll.lugares.create(**kw)

"""

    global funcs
    for i in data :
        createimport(i)
    theperms(permissions)
    print "def makeitall ():"
    for i in funcs :
        print "\t%s()"%i.replace(".csv","").replace(".shp","").replace("/","_")




        


def createMain():
    print """\n\nif __name__ == '__main__':
    makeitall()
    g1()
"""
                
    
    
