# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings 

urlpatterns = patterns('ghostserver.garbage.views',
                       url(r'^$' , 'login_mobile', name="login_mobile"),
                       )
