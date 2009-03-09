# -*- coding: utf-8 -*-
from django.conf import settings

from ghost import models as modelsGhost
from ghost import constsappli



def menu(request):
    """
    menu_stt = Nombre del menú donde el usuario se encuentra 
    submenu_stt = Nombre del submenú donde el usuario se encuentra
    menus = Menús asociados al usuario
    submenus = Submenús asociados al usuario.
    return: 
    """
    
    menu_stt=None
    submenu_stt=None
    menus=set()
    submenus=set()
    print request.user
    
    path=request.get_full_path().strip("/")
    a=modelsGhost.Menu.objects.filter(url=path,padre__isnull=True)
    if a.count()>0:
        menu_stt=a[0]
        submenu_stt=None
    else:
        a=modelsGhost.Menu.objects.filter(url=path,padre__isnull=False)
        if a.count()>0:
            menu_stt=a[0].padre
            submenu_stt=a[0]
        else:
            menu_stt=None
            submenu_stt=None
            
    #print menu_stt
    #print submenu_stt

    if request.user.is_superuser :
        menus=modelsGhost.Menu.objects.filter(padre__isnull=True)
        if menu_stt:
            submenus=modelsGhost.Menu.objects.filter(padre__isnull=False, padre=menu_stt)
        menus_user=[]
        submenus_user=[]
    elif request.user.is_anonymous()==False:
        #Se adicionas los menús y submenús asociados a los grupos en donde pertenezca el usuario
        menus_user=[i for i in modelsGhost.Menu.objects.filter(perfiles__grupo__user=request.user,padre__isnull=True)]
        submenus_user=[i for i in modelsGhost.Menu.objects.filter(perfiles__grupo__user=request.user,padre__isnull=False)]
        
        #Adicionar los menus y submenus asociados directamente a un usuario
        pers=request.user.personas_set.filter()
        if pers.count() >0:
            menus_user=menus_user+[i for i in pers[0].menus.filter(padre__isnull=True)]
            submenus_user=submenus_user+[i for i in pers[0].menus.filter(padre__isnull=False)]
    else:
        #if request.user.is_anonymous()==True:
        #When the user is not logged, there is no menu to show
        menus_user=[i for i in modelsGhost.Menu.objects.filter(perfiles__grupo__name=constsappli.GROUPANONYMUS,padre__isnull=True)]
        submenus_user=[i for i in modelsGhost.Menu.objects.filter(perfiles__grupo__name=constsappli.GROUPANONYMUS,padre__isnull=False)]
        #print menus_user
        #print submenus_user
        #return {'menu':[], 'submenu':[]}
    
    for i in menus_user:
        menus.add(i)
    if menu_stt in menus_user:
        for i in modelsGhost.Menu.objects.filter(padre=menu_stt): 
            submenus.add(i)
    for i in submenus_user:
        if i.padre==menu_stt:
            submenus.add(i)
        menus.add(i.padre)
   
    try:
        menus.add(modelsGhost.Menu.objects.filter(padre__isnull=True,url=constsappli.DEFAULTLOGON.strip('/'))[0])
    except:pass
        
    
    men=[(i==menu_stt and "activo" or "",i) for i in sorted(menus,lambda x,y : x.posicion-y.posicion)]# Organiza los menús y los adiciona en una lista de tuplas 
    sub_men=[(i==submenu_stt and "activo" or "",i) for i in sorted(submenus,lambda x,y : x.posicion-y.posicion)]# Organiza los submenús y los adiciona en una lista de tuplas 
    if submenu_stt==None:
        sub_men.insert(0,("activo",menu_stt))
    else:
        sub_men.insert(0,("",menu_stt))
    
    print men,sub_men
    return {'menus':men, 'submenus':sub_men }




def cfg(request):
    """
    Adds configuration context variable to the context.

    """
    return {'MEDIA_URL': settings.MEDIA_URL , 'URL_PREFIX': settings.URL_PREFIX }

