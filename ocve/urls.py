__author__ = 'Elliot'
from django.conf.urls import *
from views import *
from annotationviews import *

urlpatterns = patterns('',

                       #DBMI
                       (r'^', include('ocve.dbmi.dbmi_urls')),

                       #UI URLS
                       (r'^sourceuiprototype/$', sourceprototype),
                       (r'^sourceuiprototype/(?P<id>\d+)/$', getSource),
                       (r'^barview$', barview),
                        #(r'^correctsi/$', correctSourceInformation ),
                        (r'^ui/acview/(?P<acHash>[\d|\w]+)/$', acview),
                       (r'^ui/sourcejs/$', sourcejs),
                       (r'^ui/$', browse),
                       (r'^ui/pageview/(?P<id>\d+)/$', ocvePageImageview),
                       (r'^ui/pageview/(?P<id>\d+)/(?P<barid>\d+)/$', ocveViewInPage),
                       (r'^ui/shelfmarkview/(?P<acHash>[\d|\w]+)/$', shelfmarkview),
                       (r'^ui/sourceinformation/(?P<id>\d+)/$', sourceinformation),
                       (r'^ui/workinformation/(?P<id>\d+)/$', workinformation),
                       (r'^ui/serializeFilter/$', serializeFilter),
                       (r'^ui/resetFilter/$', resetFilter),
                       (r'^ui/saveCollection/$', saveCollection),

                       #User account management
                       #(r'^accounts/', include('registration.backends.default.urls')),

                       (r'^sourcesbyshelfmark/$', sourcesbyshelfmark),
                       (r'^data/verifyImages/', verifyImages),
                       (r'^data/regionImport/', regionTest),
                       (r'^data/uploadOCVE/', uploadOCVE),
                       (r'^data/buildTree/', buildHierarchy),
                       (r'^work/(?P<id>\d+)/$', work),
                       (r'^page/(?P<id>\d+)/$', page),
                       (r'^getBarRegions/(?P<id>\d+)/$', getBarRegions),
                       (r'^getBarRegions/(?P<id>\d+)/(?P<barid>\d+)/$', getViewInPageRegions),
                       (r'^getGroupedBarRegions/(?P<id>\d+)/$', getGroupedBarRegions),
                       (r'^works/', works),

                       #Annotation URLS
                       (r'^saveNote/$', saveNote),
                       (r'^deleteNote/(?P<id>\d+)$', deleteNote),
                       (r'^newsourcefiles/$', newsourcefiles),
                       (r'^getAnnotationRegions/(?P<id>\d+)/$', getAnnotationRegions),
                       (r'^posth/$', posth),


                       # Ajax URLS for inline collections
                       (r'^ajax/inline-collections/$', ajaxInlineCollections),
                       (r'^ajax/change-collection-name/$', ajaxChangeCollectionName),
                       (r'^ajax/add-collection/$', ajaxAddCollection),
                       (r'^ajax/add-image-to-collection-modal/$', ajaxAddImageToCollectionModal),
                       (r'^ajax/add-image-to-collection/$', ajaxAddImageToCollection),
                       (r'^ajax/delete-image-from-collection/$', ajaxDeleteImageFromCollection),
                       (r'^ajax/delete-collection/$', ajaxDeleteCollection),



)
