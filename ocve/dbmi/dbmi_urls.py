__author__ = 'Elliot'
from dbmiviews import *
from django.conf.urls import *
from ocve.views import *
from sourceeditor import *
from bareditor import *
from datatools import correctSourceInformation
from uploader import convertFolder,convertimage
from spine import *

urlpatterns = patterns('', (r'^source/(?P<id>\d+)/$', source),
                       #Source and source information
                       (r'^sourceviews/(?P<m>\d+)/$', sourceView),
                       (r'^sourceview/(?P<id>\d+)/$', uncorrectedSource),
                       (r'^sourceeditor/(?P<id>\d+)/$', existingsourceeditor),
                       (r'^sourceeditor/new/(?P<id>\d+)/$', newsourceeditor),
                       (r'^sourceeditor/$', sourceeditor),
                       (r'^saveSource/(?P<id>\d+)/$', saveSource),
                       (r'^saveSourceInformation/(?P<id>\d+)/$', saveSourceInformation),
                       (r'^clonesource/(?P<id>\d+)/$', clonesource),

                       #Source/work components
                       #(r'^sourcecomp/(?P<id>\d+)/$', sourceComp),
                       (r'^editsourcecomponent/(?P<id>\d+)/$', editexistingsourcecomponent),
                       (r'^deletesourcecomponent/(?P<id>\d+)/$', deletesourcecomponent),
                       (r'^savesourcecomponent/(?P<id>\d+)/$', savesourcecomponent),
                       (r'^updatecomponentorder/$', updateComponentOrder),
                       (r'^createsourcecomponent/(?P<sourceid>\d+)/$', createsourcecomponent),
                       (r'^createfrontmatter/(?P<sourceid>\d+)/$', createfrontmatter),
                       (r'^createendmatter/(?P<sourceid>\d+)/$', createendmatter),
                       (r'^updatesc/$', updateSourceComponent),
                       (r'^deletesource/(?P<id>\d+)/$', deletesource),

                       #Pages and bars
                       (r'^page/(?P<id>\d+)/$', loadEditPage),
                       (r'^correctCropping/', correctCrop),
                       url(r'^editbars/(?P<id>\d+)/$', editBars, name="edit-bars"),
                       (r'^cropCorrect/(?P<id>\d+)/$', cropCorrectView),
                       (r'^reorderBars/$', reorderBarNumbers),
                       (r'^deletepage/(?P<id>\d+)/$', deletepage),
                       (r'^savePage/$', savePage),
                       (r'^updatePageIndex/$', updatepageindex),
                       (r'^defaultpageorder/(?P<id>\d+)/$', defaultpageorder),
                       (r'^updatepagetype/(?P<id>\d+)/$', updatepagetype),


                       #Misc

                       (r'^fixbarrange/$', findmeta),
                       #(r'^structure/(?P<id>\d+)/$', sourceStructureView),
                       (r'^updateStatus/$', updateStatus),
                       (r'^dbmi/$', dbmiView),
                       (r'^findunverified/$', findUnverifiedImages),
                       (r'^sourcesbywork/$', sourcesbywork),
                       (r'^generatethumbnails/$', generateAllThumbnails),

                       #upload
                       (r'^upload/selectsource/', selectSource),
                       (r'^upload/addsource/', addSource),
                       (r'^upload/addpage/', addPages),
                       (r'^upload/page/(?P<id>\d+)/$', iipPage),
                       (r'^upload/addtosource/(?P<id>\d+)/$', addToSource),
                       (r'^upload/modifypage/$', modifyPage),
                       (r'^updateBarRegions/$', updateBarRegion),
                       (r'^updateBarNumber/$', updateBarNumber),
                       (r'^convertfolder/(?P<folderName>.*)/$', convertFolder),
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
                        (r'^work/(?P<id>\d+)/$', work),
                        (r'^workadmin/(?P<id>\d+)/$', workadmin),
                        (r'^savework/(?P<id>\d+)/$', savework),
                        (r'^saveworkinformation/(?P<id>\d+)/$', saveworkinformation),
                        (r'^saveworkcomponents/(?P<id>\d+)/$', saveworkcomponents),
                       (r'^works/', worksview),


)