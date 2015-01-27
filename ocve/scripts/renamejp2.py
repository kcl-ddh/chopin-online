__author__ = 'Elliott'
from django.http import HttpResponse
from models import *


def renamejp2(request):
    log="<html><head></head><body><h1>Successful changes</h1><div>"
    errors="<h1>ERRORS</h1><div>"
    #Get all page legacy records
    pl=PageLegacy.objects.all()
        #Try to get page on server
            #Passed: Copy page to parsed directory, with pageimage id as new filename
            #Failed: write expected filename to error log
    return HttpResponse("")