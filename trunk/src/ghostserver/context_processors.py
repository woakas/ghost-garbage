# -*- coding: utf-8 -*-
from django.conf import settings

def cfg(request):
    """
    Adds configuration context variable to the context.

    """
    return {'MEDIA_URL': settings.MEDIA_URL , 'URL_PREFIX': settings.URL_PREFIX }

