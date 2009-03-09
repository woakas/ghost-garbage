# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings 

urlpatterns = patterns('ghostserver.ghost.views',
                       (r'^$' , 'index'),
                       (r'^index$' , 'index'),
                       (r'^login$' , 'entry'),
                       )
