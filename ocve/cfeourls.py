__author__ = 'Elliot'
from django.conf.urls import patterns, url
from views import *

#URLS for the CFEO skin of the UI

urlpatterns = patterns('',
                       url(r'^browse/$', cfeoBrowse, name='cfeo_browse'),
                       (r'^browse/acview/(?P<acHash>[\d|\w]+)/$', cfeoacview),
                       (r'^browse/pageview/(?P<id>\d+)/$', cfeoPageImageview),
                       (r'^browse/comparepageview/(?P<compareleft>\d*)/(?P<compareright>\d*)/$', comparePageImageview),
                       (r'^browse/comparepageview/(?P<compareleft>\d*)/$', comparePageImageview),
                       (r'^browse/comparepageview/$', comparePageImageview),
                       (r'^browse/sourceinformation/(?P<id>\d+)/$', cfeoSourceInformation),
                       (r'^browse/workinformation/(?P<id>\d+)/$', cfeoWorkInformation),
)
