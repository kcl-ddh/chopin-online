# Auto generated from an XMI file
# Do not edit this file
# Edit admin_custom.py instead
from models import *
from django.contrib import admin
from admin_custom import *

#
class SourceInformation_YearInline(admin.TabularInline):

	model = SourceInformation_Year
	extra = 1

#
class SourceComponent_InstrumentInline(admin.TabularInline):

	model = SourceComponent_Instrument
	extra = 1

#
class SourceInformation_PrintingMethodInline(admin.TabularInline):

	model = SourceInformation_PrintingMethod
	extra = 1

#
class Genre_WorkInline(admin.TabularInline):

	model = Genre_Work
	extra = 1

#
class Annotation_BarRegionInline(admin.TabularInline):

	model = Annotation_BarRegion
	extra = 1

#
class WorkAdmin(admin.ModelAdmin):
	model = Work

	verbose_name = 'Work'
	verbose_name_plural = 'Works'

	#inlines = (Genre_WorkInline, )


#
class OpusAdmin(admin.ModelAdmin):
	model = Opus

	verbose_name = 'Opus'
	verbose_name_plural = 'Opuses'

	inlines = ()


#
class BarRegionAdmin(admin.ModelAdmin):
	model = BarRegion

	verbose_name = 'BarRegion'
	verbose_name_plural = 'BarRegions'

	inlines = (Annotation_BarRegionInline, )


#
class BarAdmin(admin.ModelAdmin):
	model = Bar

	verbose_name = 'Bar'
	verbose_name_plural = 'Bars'

	inlines = ()


#
class SourceAdmin(admin.ModelAdmin):
	model = Source
	verbose_name = 'Source'
	verbose_name_plural = 'Sources'
	inlines = (SourceInformationInline,)
#
class GenreAdmin(admin.ModelAdmin):
	model = Genre

	verbose_name = 'Genre'
	verbose_name_plural = 'Genres'

	inlines = (Genre_WorkInline, )


#
class keyPitchAdmin(admin.ModelAdmin):
	model = keyPitch

	verbose_name = 'keyPitch'
	verbose_name_plural = 'keyPitchs'

	inlines = ()


#
class InstrumentAdmin(admin.ModelAdmin):
	model = Instrument

	verbose_name = 'Instrument'
	verbose_name_plural = 'Instruments'

	inlines = (SourceComponent_InstrumentInline, )


#
class keyModeAdmin(admin.ModelAdmin):
	model = keyMode

	verbose_name = 'keyMode'
	verbose_name_plural = 'keyModes'

	inlines = ()
#
class SourceComponentAdmin(admin.ModelAdmin):
	model = SourceComponent

	verbose_name = 'SourceComponent'
	verbose_name_plural = 'SourceComponents'

	inlines = (SourceComponent_InstrumentInline, )
#
class WorkComponentAdmin(admin.ModelAdmin):
    model = WorkComponent
    verbose_name = 'WorkComponent'
    verbose_name_plural = 'WorkComponents'
    list_display = ('label', 'work',)
    raw_id_fields = ('work',)
#
class SourceComponent_WorkComponentAdmin(admin.ModelAdmin):
    model = SourceComponent_WorkComponent
    list_display = ( 'id', 'workcomponent', 'workcomp_id', 'sourcecomponent', 'workcomponent_work', 'sourcecomponent_work', 'sourcecomponent_source',  'sourcecomponent_cfeolabel' )
    raw_id_fields = ('sourcecomponent', 'workcomponent',)


    def workcomp_id(self, instance):
        return instance.workcomponent.id

    def workcomponent_work(self, instance):
        return "%s (%s)" % ( instance.workcomponent.work, instance.workcomponent.work.id )

    def sourcecomponent_work(self, instance):
        return "%s (%s)" % ( instance.sourcecomponent.source.getWork(), instance.sourcecomponent.source.getWork().id,)

    def sourcecomponent_source(self, instance):
        return "%s" % (instance.sourcecomponent.source,)

    def sourcecomponent_cfeolabel(self, instance):
        return "%s" % (instance.sourcecomponent.source.cfeolabel,)

    def same_work(self, instance):
        if (instance.workcomponent.work.id == instance.sourcecomponent.source.getWork().id):
            return "True"
        else:
            return "False"
#
class PublisherAdmin(admin.ModelAdmin):
	model = Publisher

	verbose_name = 'Publisher'
	verbose_name_plural = 'Publishers'

	inlines = ()


#
class WorkComponentTypeAdmin(admin.ModelAdmin):
	model = WorkComponentType

	verbose_name = 'WorkComponentType'
	verbose_name_plural = 'WorkComponentTypes'

	inlines = ()


#
class instrumentComponentAdmin(admin.ModelAdmin):
	model = instrumentComponent

	verbose_name = 'instrumentComponent'
	verbose_name_plural = 'instrumentComponents'

	inlines = ()


#
class WorkCollectionAdmin(admin.ModelAdmin):
	model = WorkCollection

	verbose_name = 'WorkCollection'
	verbose_name_plural = 'WorkCollections'

	inlines = ()


#
class SourceInformationAdmin(admin.ModelAdmin):
	model = SourceInformation

	verbose_name = 'SourceInformation'
	verbose_name_plural = 'SourceInformations'

	inlines = (SourceInformation_YearInline, SourceInformation_PrintingMethodInline, )


#
class PageImageAdmin(admin.ModelAdmin):
	model = PageImage

	verbose_name = 'PageImage'
	verbose_name_plural = 'PageImages'

	inlines = ()


#
class PageTypeAdmin(admin.ModelAdmin):
	model = PageType

	verbose_name = 'PageType'
	verbose_name_plural = 'PageTypes'

	inlines = ()


#
class CollectionTypeAdmin(admin.ModelAdmin):
	model = CollectionType

	verbose_name = 'CollectionType'
	verbose_name_plural = 'CollectionTypes'

	inlines = ()


#
class SourceComponentTypeAdmin(admin.ModelAdmin):
	model = SourceComponentType

	verbose_name = 'SourceComponentType'
	verbose_name_plural = 'SourceComponentTypes'

	inlines = ()


#
class PageAdmin(admin.ModelAdmin):
	model = Page

	verbose_name = 'Page'
	verbose_name_plural = 'Pages'

	inlines = ()

class PageLegacyAdmin(admin.ModelAdmin):
	model = PageLegacy

	verbose_name = 'PageLegacy'
	verbose_name_plural = 'Pagelegacy'

	inlines = ()


#
class ArchiveAdmin(admin.ModelAdmin):
	model = Archive

	verbose_name = 'Archive'
	verbose_name_plural = 'Archives'

	inlines = ()


#
class CityAdmin(admin.ModelAdmin):
	model = City

	verbose_name = 'City'
	verbose_name_plural = 'Cities'

	inlines = ()


#
class CountryAdmin(admin.ModelAdmin):
	model = Country

	verbose_name = 'Country'
	verbose_name_plural = 'Countries'

	inlines = ()


#
class SourceTypeAdmin(admin.ModelAdmin):
	model = SourceType

	verbose_name = 'SourceType'
	verbose_name_plural = 'SourceTypes'

	inlines = ()


#
class YearAdmin(admin.ModelAdmin):
	model = Year

	verbose_name = 'Year'
	verbose_name_plural = 'Years'

	inlines = (SourceInformation_YearInline, )


#
class DedicateeAdmin(admin.ModelAdmin):
	model = Dedicatee

	verbose_name = 'Dedicatee'
	verbose_name_plural = 'Dedicatees'

	inlines = ()


#
class PrintingMethodAdmin(admin.ModelAdmin):
	model = PrintingMethod

	verbose_name = 'PrintingMethod'
	verbose_name_plural = 'PrintingMethods'

	inlines = (SourceInformation_PrintingMethodInline, )


#
class WorkInformationAdmin(admin.ModelAdmin):
	model = WorkInformation

	verbose_name = 'WorkInformation'
	verbose_name_plural = 'WorkInformations'

	inlines = ()


#
class AnnotationAdmin(admin.ModelAdmin):
	model = Annotation

	verbose_name = 'Annotation'
	verbose_name_plural = 'Annotations'

	inlines = (Annotation_BarRegionInline, )

class AnnotationTypeAdmin(admin.ModelAdmin):
    model = AnnotationType

    verbose_name = 'Annotation'
    verbose_name_plural = 'Annotations'


#
class AcCodeAdmin(admin.ModelAdmin):
	model = AcCode

	verbose_name = 'AcCode'
	verbose_name_plural = 'AcCodes'

	inlines = ()


#
