__author__ = 'Elliot'
#Template context processors used by OCVE
from django.conf import settings



def ocve_constants(request):
    return {'STATIC_URL':settings.STATIC_URL
            ,'THUMBNAIL_WIDTH':settings.THUMBNAIL_WIDTH
            ,'IIP_URL':settings.IIP_URL}

  