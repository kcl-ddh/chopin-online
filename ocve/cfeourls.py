__author__ = 'Elliot'
from django.conf.urls import patterns, url
from views import *

#URLS for the CFEO skin of the UI

urlpatterns = patterns('',
                       url(r'^browse/$', cfeoBrowse, name='cfeo_browse'),
                       (r'^browse/acview/(?P<acHash>[\d|\w]+)/$', cfeoacview),
                       url(r'^browse/pageview/(?P<id>\d+)/$', cfeoPageImageview, name='cfeo_pageview'),
                       url(r'^browse/comparepageview/(?P<compareleft>\d*)/(?P<compareright>\d*)/$', comparePageImageview,name='cfeo_comparepageview'),
                       url(r'^browse/comparepageview/(?P<compareleft>\d*)/$', comparePageImageview,name='cfeo_compareleftpageview'),
                       (r'^browse/comparepageview/$', comparePageImageview),
                       url(r'^browse/sourceinformation/(?P<id>\d+)/$', cfeoSourceInformation,name='cfeo_sourceinformation'),
                       url(r'^browse/workinformation/(?P<id>\d+)/$', cfeoWorkInformation,name='cfeo_workinformation'),
)
