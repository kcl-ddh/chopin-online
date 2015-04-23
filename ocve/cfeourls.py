__author__ = 'Elliot'
from views import *
from django.conf.urls import *

#URLS for the CFEO skin of the UI

urlpatterns = patterns('',
                       (r'^browse/$', cfeoBrowse),
                       (r'^browse/acview/(?P<acHash>[\d|\w]+)/$', cfeoacview),
                       (r'^browse/pageview/(?P<id>\d+)/$', cfeoPageImageview),
                       (r'^browse/comparepageview/(?P<compareleft>\d*)/(?P<compareright>\d*)/$', comparePageImageview),
                       (r'^browse/comparepageview/(?P<compareleft>\d*)/$', comparePageImageview),
                       (r'^browse/comparepageview/$', comparePageImageview),
                       (r'^browse/sourceinformation/(?P<id>\d+)/$', cfeoSourceInformation),
                       (r'^browse/workinformation/(?P<id>\d+)/$', cfeoWorkInformation),
)