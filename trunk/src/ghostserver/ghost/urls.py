# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings 

urlpatterns = patterns('ghostserver.ghost.views',
                       url(r'^$' , 'index'),
                       url(r'^index/gallery/$' , 'gallery'),
                       url(r'^index/devel/$' , 'devel'),
                       url(r'^index/$' , 'index'),
                       url(r'^login/$' , 'entry'),
                       url(r'^about/$' , 'about'),
                       url(r'^accounts/$' , 'user', name="user_settings"),
                       )
