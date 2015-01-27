__author__ = 'Elliot'
from editviews import *
from django.conf.urls import *
from ocve.views import *
from sourceeditor import *
from bareditor import *
from datatools import correctSourceInformation
# URLS for the CFEO skin of the UI

urlpatterns = patterns('', (r'^source/(?P<id>\d+)/$', source),
                       #Source and source information
                       (r'^sourceviews/(?P<m>\d+)/$', sourceView),
                       (r'^sourceview/(?P<id>\d+)/$', uncorrectedSource),
                       (r'^sourceeditor/(?P<id>\d+)/$', existingsourceeditor),
                       (r'^sourceeditor/new/(?P<id>\d+)/$', newsourceeditor),
                       (r'^sourceeditor/$', sourceeditor),
                       (r'^saveSource/(?P<id>\d+)/$', saveSource),
                       (r'^saveSourceInformation/(?P<id>\d+)/$', saveSourceInformation),

                       #Source/work components
                       (r'^sourcecomp/(?P<id>\d+)/$', sourceComp),
                       (r'^editsourcecomponent/(?P<id>\d+)/$', editsourcecomponent),
                       (r'^deletesourcecomponent/(?P<id>\d+)/$', deletesourcecomponent),
                       (r'^savesourcecomponent/(?P<id>\d+)/$', savesourcecomponent),
                       (r'^updatecomponentorder/$', updateComponentOrder),
                       (r'createSourceComponent/(?P<id>\d+)/$', createSourceComponent),
                       (r'^updatesc/$', updateSourceComponent),

                       #Pages and bars
                       (r'^page/(?P<id>\d+)/$', loadEditPage),
                       (r'^correctCropping/', correctCrop),
                       url(r'^editbars/(?P<id>\d+)/$', editBars, name="edit-bars"),
                       (r'^cropCorrect/(?P<id>\d+)/$', cropCorrectView),
                       (r'^reorderBars/$', reorderBarNumbers),
                       (r'^deletepage/(?P<id>\d+)/$', deletepage),
                       (r'^savePage/$', savePage),
                       (r'^updatePageIndex/$', updatepageindex),

                       #Misc

                       (r'^fixbarrange/$', findmeta),
                       (r'^structure/(?P<id>\d+)/$', sourceStructureView),
                       (r'^updateStatus/$', updateStatus),
                       (r'^editPages/$', editPageView),
                       (r'^dbmi/$', dbmiView),
                       (r'^findunverified/$', findUnverifiedImages),
                       (r'^sourcesbywork/$', sourcesbywork),

                       #upload
                       (r'^upload/selectsource/', selectSource),
                       (r'^upload/addsource/', addSource),
                       (r'^upload/addpage/', addPages),
                       (r'^upload/page/(?P<id>\d+)/$', iipPage),
                       (r'^upload/addtosource/(?P<id>\d+)/$', addToSource),
                       (r'^upload/modifypage/$', modifyPage),
                       (r'^updateBarRegions/$', updateBarRegion),
                       (r'^updateBarNumber/$', updateBarNumber),
                       (r'^convertfolder/(?P<folderName>.*?)/$', convertFolder),
                       (r'^convertimage/$', convertimage),


                       #Spine URLS
                       #List of works
                       (r'^spines/$', worksforspine),
                       #Spines for a single work
                       (r'^editspine/(?P<id>\d+)/$', workspine),
                       (r'^posthumousspine/$', posthumousSpines),
                       #A single part of a spine
                       (r'^spine$', spine),
                       (r'^importspine/$', importXLS),
                       #Export/import in CSV for editing
                       (r'^exportspine/(?P<id>\d+)/$', exportXLS),
                       (r'^deletesourcespines/(?P<id>\d+)/$', deleteSourceSpines),
                       (r'^fix/$', fix),
)