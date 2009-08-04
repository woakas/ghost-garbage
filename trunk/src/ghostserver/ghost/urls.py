# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings 

urlpatterns = patterns('ghostserver.ghost.views',
                       url(r'^accounts/activate/(?P<activation_key>\w+)/$',
                           'activate_user',
                           name='registration_activate'),
                       url(r'^accounts/$' , 'profile', name="user_settings"),
                       url(r'^mobile/login$' , 'login_mobile', name="login_mobile"),
                       )
