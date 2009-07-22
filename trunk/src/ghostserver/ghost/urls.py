# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings 

urlpatterns = patterns('ghostserver.ghost.views',
                       url(r'^accounts/profile/$' , 'profile'),
                       url(r'^accounts/$' , 'profile', name="user_settings"),
                       url(r'^mobile/login$' , 'login_mobile', name="login_mobile"),
                       )
