__author__ = 'Elliot'
from django.conf.urls import *
from views import *
from annotationviews import *
from dbmi.uploader import newsourcefiles,posth

urlpatterns = patterns('',

                       #DBMI
                       (r'^', include('ocve.dbmi.dbmi_urls')),

                       #UI URLS
                       (r'^browse/barview$', barview),
                        #(r'^correctsi/$', correctSourceInformation ),
                        (r'^browse/acview/(?P<acHash>[\d|\w]+)/$', acview),
                       (r'^browse/sourcejs/$', sourcejs),
                       (r'^browse/$', browse),
                       (r'^browse/pageview/(?P<id>\d+)/$', ocvePageImageview),
                       (r'^browse/pageview/(?P<id>\d+)/(?P<barid>\d+)/$', ocveViewInPage),
                       (r'^browse/shelfmarkview/(?P<acHash>[\d|\w]+)/$', shelfmarkview),
                       (r'^browse/sourceinformation/(?P<id>\d+)/$', sourceinformation),
                       (r'^browse/workinformation/(?P<id>\d+)/$', workinformation),
                       (r'^browse/serializeFilter/$', serializeFilter),
                       (r'^browse/resetFilter/$', resetFilter),
                       #Ajax url for annotation fetch
                       (r'^browse/getAnnotations/(?P<id>\d+)/$', getAnnotations),

                       #User account management
                       #(r'^accounts/', include('registration.backends.default.urls')),



                       (r'^data/verifyImages/', verifyImages),

                       (r'^data/uploadOCVE/', uploadOCVE),



                       (r'^getBarRegions/(?P<id>\d+)/$', getBarRegions),
                       (r'^getBarRegions/(?P<id>\d+)/(?P<barid>\d+)/$', getViewInPageRegions),
                       (r'^getGroupedBarRegions/(?P<id>\d+)/$', getGroupedBarRegions),


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