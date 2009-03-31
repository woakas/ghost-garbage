# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('ghostserver.geolbs.views',
                       (r'^$' , 'index'),
                       (r'^addAtributo$' , 'addAtributo'),
                       )
