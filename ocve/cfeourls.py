__author__ = 'Elliot'
from views import *
from django.conf.urls import *

#URLS for the CFEO skin of the UI

urlpatterns = patterns('',
                       (r'^ui/$', cfeoBrowse),
                       (r'^ui/acview/(?P<acHash>[\d|\w]+)/$', cfeoacview),
                       (r'^ui/pageview/(?P<id>\d+)/$', cfeoPageImageview),
                       (r'^ui/comparepageview/(?P<compareleft>\d*)/(?P<compareright>\d*)/$', comparePageImageview),
                       (r'^ui/comparepageview/(?P<compareleft>\d*)/$', comparePageImageview),
                       (r'^ui/comparepageview/$', comparePageImageview),
                       (r'^ui/sourceinformation/(?P<id>\d+)/$', cfeoSourceInformation),
                       (r'^ui/workinformation/(?P<id>\d+)/$', cfeoWorkInformation),
)

