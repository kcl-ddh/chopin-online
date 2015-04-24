# auto generated from an XMI file
# this file can be edit, 
# make sure it is renamed into "admin_custom.py" (without the underscore at the beginning)
from models import *
from admin_generic import *
from django.contrib import admin
 

class WorkComponentInline(admin.TabularInline):
    model=WorkComponent

class SourceInline(admin.TabularInline):
    model=Source

class SourceInformationInline(admin.StackedInline):
    model=SourceInformation

class PageInline(admin.TabularInline):
    model=Page

#class SourceInformation_YearInline(SourceInformation_YearInline):
#	pass
#
##
#class SourceComponent_InstrumentInline(SourceComponent_InstrumentInline):
#	pass
#
##
#class SourceInformation_PrintingMethodInline(SourceInformation_PrintingMethodInline):
#	pass
#
##
#class Genre_WorkInline(Genre_WorkInline):
#	pass
#
##
#class Annotation_BarRegionInline(Annotation_BarRegionInline):
#	pass
#
##
#class WorkComponentAdmin(WorkComponentAdmin):
#    pass
##	inlines=[
##        SourceInline
##    ]
#
##
#class WorkAdmin(WorkAdmin):
#	inlines=[
#        WorkComponentInline
#    ]
#
##
#class OpusAdmin(OpusAdmin):
#	pass
#
##
#class BarRegionAdmin(BarRegionAdmin):
#	pass
#
##
#class BarAdmin(BarAdmin):
#	pass
#
##
#class SourceAdmin(SourceAdmin):
#	pass
#
##
#class GenreAdmin(GenreAdmin):
#	pass
#
##
#class keyPitchAdmin(keyPitchAdmin):
#	pass
#
##
#class InstrumentAdmin(InstrumentAdmin):
#	pass
#
##
#class keyModeAdmin(keyModeAdmin):
#	pass
#
##
#class SourceComponentAdmin(SourceComponentAdmin):
#	pass
#
##
#class PublisherAdmin(PublisherAdmin):
#	pass
#
##
#class WorkComponentTypeAdmin(WorkComponentTypeAdmin):
#	pass
#
##
#class instrumentComponentAdmin(instrumentComponentAdmin):
#	pass
#
##
#class WorkCollectionAdmin(WorkCollectionAdmin):
#	pass
#
##
#class SourceInformationAdmin(SourceInformationAdmin):
#	pass
#
##
#class PageImageAdmin(PageImageAdmin):
#	pass
#
##
#class PageTypeAdmin(PageTypeAdmin):
#	pass
#
##
#class CollectionTypeAdmin(CollectionTypeAdmin):
#	pass
#
##
#class SourceComponentTypeAdmin(SourceComponentTypeAdmin):
#	pass
#
##
#class PageAdmin(PageAdmin):
#	pass
#
##
#class ArchiveAdmin(ArchiveAdmin):
#	pass
#
##
#class CityAdmin(CityAdmin):
#	pass
#
##
#class CountryAdmin(CountryAdmin):
#	pass
#
##
#class SourceTypeAdmin(SourceTypeAdmin):
#	pass
#
##
#class YearAdmin(YearAdmin):
#	pass
#
##
#class DedicateeAdmin(DedicateeAdmin):
#	pass
#
##
#class PrintingMethodAdmin(PrintingMethodAdmin):
#	pass
#
##
#class WorkInformationAdmin(WorkInformationAdmin):
#	pass
#
##
#class AnnotationAdmin(AnnotationAdmin):
#	pass
#
##
#class TreeAdmin(TreeAdmin):
#	pass
#
##
#class TreeTypeAdmin(TreeTypeAdmin):
#	pass
#
##
#class AcCodeAdmin(AcCodeAdmin):
#	pass

