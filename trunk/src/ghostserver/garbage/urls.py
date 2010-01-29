# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings 

urlpatterns = patterns('ghostserver.garbage.views',
                       url(r'^mobile/position/(?P<lon>[0-9.-]+)/(?P<lat>[0-9.-]+)/$' , 'position_mobile', name="position_mobile"),
                       )
