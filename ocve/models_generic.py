# -*- coding: utf-8 -*-
# auto generated from an XMI file
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.utils.encoding import force_unicode
from django.contrib.auth.models import User
import re




def getUnicode(object):
    if (object == None):
        return u""
    else:
        return force_unicode(object)


#
class WorkComponent(models.Model):
    orderno = models.IntegerField(null=True, blank=True, )
    label = models.TextField(null=False, default="", blank=True, )
    music = models.IntegerField(null=True, blank=True, )
    work = models.ForeignKey('Work', blank=False, null=False, default=1, )
    keymode = models.ForeignKey('keyMode', blank=False, null=False, default=1, )
    keypitch = models.ForeignKey('keyPitch', blank=False, null=False, default=1, )
    opus = models.ForeignKey('Opus', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'WorkComponent'
        verbose_name_plural = 'WorkComponents'


    table_group = ''


#
class Work(models.Model):
    complete = models.BooleanField(default=False, null=False, blank=False, )
    label = models.TextField(null=False, default="", blank=True, )
    genre = models.ManyToManyField('Genre', blank=False, null=False, default=1, through='Genre_Work', )
    workinformation = models.ForeignKey('WorkInformation', blank=False, null=False, default=1, )
    workcollection = models.ForeignKey('WorkCollection', blank=False, null=False, default=2, )
    orderno = models.IntegerField(null=True, blank=True, )
    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Works'
        ordering=['orderno']


    table_group = ''
    def getSources(self):
        sources = Source.objects.filter(sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=self).distinct()
        return sources

#
class Opus(models.Model):
    opusno = models.IntegerField(null=True, blank=True, )

    class Meta:
        verbose_name = 'Opus'
        verbose_name_plural = 'Opuses'

Opus._meta.ordering = ["opusno"]



#
class BarRegion(models.Model):
    x = models.IntegerField(null=True, blank=True, )
    y = models.IntegerField(null=True, blank=True, )
    width = models.IntegerField(null=True, blank=True, )
    height = models.IntegerField(null=True, blank=True, )
    anomaly = models.IntegerField(null=False, blank=True,default=0 )
    annotation = models.ManyToManyField('Annotation', blank=True, null=True, through='Annotation_BarRegion', )
    pageimage = models.ForeignKey('PageImage', blank=False, null=False, default=1, )
    page = models.ForeignKey('Page', blank=False, null=False, default=1, related_name='barRegions', )
    barid_old = models.IntegerField(null=True, blank=True, )
    bar = models.ManyToManyField('Bar', blank=True, null=True,
        through='Bar_BarRegion', )

    def getHighestBarNumber(self):
        num=0
        for b in self.bar.all():
            num=b.barnumber
        return num

    def getLowestBarNumber(self):
        num=0
        bars=self.bar.all().order_by('barnumber')
        if bars.count() >0:
            return bars[0].barnumber
        return 0

    def getHighestBar(self):
        bar=None
        for b in self.bar.all():
            bar=b
        return bar

    class Meta:
        verbose_name = 'BarRegion'
        verbose_name_plural = 'BarRegions'


    table_group = ''

#Initial population with:  insert into ocve2real.ocve_bar_barregion (bar_id,barregion_id) SELECT bar_id,id FROM ocve2real.ocve_barregion o;
class Bar_BarRegion(models.Model):
    bar = models.ForeignKey('Bar', blank=False, null=False, default=1, )
    barregion = models.ForeignKey('BarRegion', blank=False, null=False, default=1, )


#
class Bar(models.Model):
    barnumber = models.IntegerField(null=True, blank=True, )
    barlabel = models.TextField(null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'Bar'
        verbose_name_plural = 'Bars'


    table_group = ''


#
class Source(models.Model):
    label = models.TextField(null=False, default="", blank=True, )
    cfeolabel = models.TextField(null=False, default="", blank=True, )
    sourcetype = models.ForeignKey('SourceType', blank=False, null=False, default=1, )
    ocve=models.BooleanField(default=False)
    cfeo=models.BooleanField(default=False)
    orderno=models.IntegerField(blank=False, null=False, default=999)

    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'
        ordering = ["orderno"]

    def setWork(self):
        pass

    def getWork(self):
        works=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source=self).distinct()
        if works is not None and works.__len__()>0:
            return works[0]
        else:
            return None

    def getOpusLabel(self):
        w = self.getWork()
        if w is not None:
            return w.label+" "+self.label
        else:
            return self.label

    def getAcCode(self):
        try:
            si=SourceInformation.objects.get(source=self)
            if self.ocve ==1 and len(si.sourcecode) > 0:
                return si.sourcecode
            if si.accode.id > 2:
                return si.accode.accode
        except ObjectDoesNotExist:
            return ""
        except MultipleObjectsReturned:
            si=SourceInformation.objects.filter(source=self)
            return ""

    def getSourceComponents(self):
        try:
            comps=SourceComponent.objects.filter(source=self)
            return comps
        except ObjectDoesNotExist:
            pass

    def getSourceInformation(self):
        si=SourceInformation.objects.filter(source=self)
        if si.count() >0:
            return si[0]
        else:
            return None

    #All instruments attached to a particular source
    def getInstruments(self):
        return Instrument.objects.filter(sourcecomponent_instrument__sourcecomponent__source=self).distinct()

    def getPrimaryPageImages(self):
        pi=PageImage.objects.filter(page__sourcecomponent__source=self,versionnumber=1).order_by("page")
        return pi

    def getPages(self):
        return Page.objects.filter(sourcecomponent__source=self)
    table_group = ''

    def getFirstBarRegion(self):
        try:
            return BarRegion.objects.filter(pageimage__page__sourcecomponent__source=self).order_by('pageimage__page','bar')[0]
        except ObjectDoesNotExist:
            return None
        except IndexError:
            return None
    #May be moved later
#    def getBarRegionAtSpine(self,x):
#
#        try:
#            region=regions[x]
#        except IndexError:
#            region=None
#        return region


#
class Genre(models.Model):
    genre = models.CharField(max_length=255, null=False, default="", blank=True, )
    pluralname = models.CharField(max_length=255, null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


    table_group = ''


#
class keyPitch(models.Model):
    keypitch = models.CharField(max_length=255, null=False, default="", blank=True, )
    orderno = models.IntegerField(null=False, default=0, )
    class Meta:
        ordering=['orderno']
        verbose_name = 'keyPitch'
        verbose_name_plural = 'keyPitches'


    table_group = ''


#
class Instrument(models.Model):
    instrument = models.CharField(max_length=255, null=False, default="", blank=True, )
    instrumentabbrev = models.CharField(max_length=128, null=False, default="", blank=True, )
    sourcecomponent = models.ManyToManyField('SourceComponent', blank=True, null=True,
                                             through='SourceComponent_Instrument', )

    class Meta:
        verbose_name = 'Instrument'
        verbose_name_plural = 'Instruments'


    table_group = ''


#
class keyMode(models.Model):
    keymode = models.CharField(max_length=255, null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'keyMode'
        verbose_name_plural = 'keyModes'


    table_group = ''


#
class SourceComponent(models.Model):
    orderno = models.IntegerField(null=True, blank=True, )
    label = models.TextField(null=False, default="", blank=True, )
    instrumentnumber = models.IntegerField(null=True, blank=True, )
    instrumentkey = models.CharField(max_length=128, null=False, default="", blank=True, )
    overridelabel = models.TextField(null=False, default="", blank=True, )
    sourcecomponenttitle = models.CharField(max_length=255, null=False, default="", blank=True,
                                            help_text=ur'''e.g song titles like "Wojack"''', )
    source = models.ForeignKey('Source', blank=False, null=False, default=1, )
    sourcecomponenttype = models.ForeignKey('SourceComponentType', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'SourceComponent'
        verbose_name_plural = 'SourceComponents'
        ordering = ["orderno"]


    table_group = ''

    def getPages(self):
        try:
            pages = Page.objects.filter(sourcecomponent=self)
            return pages
        except ObjectDoesNotExist:
            pass


#
class Publisher(models.Model):
    publisher = models.TextField(null=False, default="", blank=True, )
    notes = models.TextField(null=False, default="", blank=True, )
    publisherAbbrev = models.CharField(max_length=45, null=False, default="", blank=True)

class Meta:
    ordering = ['publisher']
    verbose_name = 'Publisher'
    verbose_name_plural = 'Publishers'

    def __unicode__(self):
        return u'%s' % (self.publisher)


table_group = ''


#
class WorkComponentType(models.Model):
    type = models.CharField(max_length=255, null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'WorkComponentType'
        verbose_name_plural = 'WorkComponentTypes'


    table_group = ''


#
class instrumentComponent(models.Model):
    instrument = models.ForeignKey('Instrument', blank=False, null=False, default=1, )
    sourcecomponent = models.ForeignKey('SourceComponent', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'instrumentComponent'
        verbose_name_plural = 'instrumentComponents'


    table_group = ''


#
class WorkCollection(models.Model):
    label = models.TextField(null=False, default="", blank=True, )
    overridelabel = models.TextField(null=False, default="", blank=True, )
    collectiontype = models.ForeignKey('CollectionType', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'WorkCollection'
        verbose_name_plural = 'WorkCollections'


    table_group = ''


#
class SourceInformation(models.Model):
    platenumber = models.CharField(max_length=255, null=False, default="", blank=True, )
    locationsimilarcopies = models.TextField(null=False, default="", blank=True, )
    reprints = models.TextField(null=False, default="", blank=True, )
    seriestitle = models.CharField(max_length=255, null=False, default="", blank=True, )
    copyright = models.CharField(max_length=255, null=False, default="", blank=True, )
    contentssummary = models.CharField(max_length=255, null=False, default="", blank=True, )
    contents = models.TextField(null=False, default="", blank=True,)# help_text=ur'''Edition text''', )
    shelfmark = models.CharField(max_length=255, null=False, default="", blank=True, )
    notes = models.TextField(null=False, default="", blank=True, )
    datepublication = models.CharField(max_length=255, null=False, default="", blank=True, )
    placepublication = models.ForeignKey('City', null=True, blank=True, )
    leaves = models.CharField(max_length=255, null=False, default="", blank=True, )
    sourcecode = models.CharField(max_length=255, null=False, default="", blank=True, )
    title = models.TextField(null=False, default="", blank=True, )
    publicationtitle = models.TextField(null=False, default="", blank=True, )
    imagesource = models.CharField(max_length=255, null=False, default="", blank=True, )
    additionalInformation=models.TextField(null=False, default="", blank=True, )
    keyFeatures=models.TextField(null=False, default="", blank=True, )
    volume = models.CharField(max_length=255, null=False, default="", blank=True, )
    source = models.ForeignKey('Source', blank=False, null=False, default=1, )
    publisher = models.ForeignKey('Publisher', blank=False, null=False, default=1, )
    archive = models.ForeignKey('Archive', blank=False, null=False, default=1, )
    dedicatee = models.ForeignKey('Dedicatee', blank=False, null=False, default=1, )
    accode = models.ForeignKey('AcCode', blank=False, null=False, default=1, )
    displayedcopy = models.CharField(max_length=255, null=False, default="", blank=True, )
    printingmethod = models.ManyToManyField('PrintingMethod',through='SourceInformation_PrintingMethod',default=1)


    class Meta:
        verbose_name = 'SourceInformation'
        verbose_name_plural = 'SourceInformations'


    table_group = ''

#
class BarSequence(models.Model):
    #pageimage = models.ForeignKey('PageImage', blank=False, null=False,)
    startbar = models.CharField(max_length=255, null=False, default="", blank=True, )
    endbar = models.CharField(max_length=255, null=False, default="", blank=True, )
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

#
class PageImage(models.Model):
    surrogate = models.IntegerField(null=True, blank=True, )
    textlabel = models.TextField(null=False, default="", blank=True, )
    versionnumber = models.IntegerField(null=True, blank=True, )
    permission = models.BooleanField(default=False, null=False, blank=False, )
    permissionnote = models.CharField(max_length=255, null=False, default="", blank=True, )
    height = models.IntegerField(null=True, blank=True, )
    width = models.IntegerField(null=True, blank=True, )
    startbar = models.CharField(max_length=255, null=False, default="", blank=True, )
    endbar = models.CharField(max_length=255, null=False, default="", blank=True, )
    corrected = models.IntegerField(null=True, blank=True, )
    page = models.ForeignKey('Page', blank=False, null=False, default=1, )
    barsequences = generic.GenericRelation(BarSequence, null=True, blank=True)

    def getInstruments(self):
        return Instrument.objects.filter(sourcecomponent_instrument__sourcecomponent__page__pageimage=self).distinct()

    class Meta:
        verbose_name = 'PageImage'
        verbose_name_plural = 'PageImages'

    table_group = ''

#
class PageType(models.Model):
    type = models.CharField(max_length=255, null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'PageType'
        verbose_name_plural = 'PageTypes'

    table_group = ''

#
class CollectionType(models.Model):
    type = models.CharField(max_length=255, null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'CollectionType'
        verbose_name_plural = 'CollectionTypes'


    table_group = ''


#
class SourceComponentType(models.Model):
    type = models.CharField(max_length=255, null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'SourceComponentType'
        verbose_name_plural = 'SourceComponentTypes'


    table_group = ''


#
class Page(models.Model):
    label = models.TextField(null=False, default="", blank=True, )
    orderno = models.IntegerField(null=True, blank=True, )
    preferredversion = models.IntegerField(null=True, blank=True, default=1 )
    sourcecomponent = models.ForeignKey('SourceComponent', blank=False, null=False, default=1, )
    pagetype = models.ForeignKey('PageType', blank=False, null=False, default=1, )

    def getPrimaryPageImage(self):
        pi=PageImage.objects.filter(page=self,versionnumber=1)
        if pi.count() > 0:
            return pi[0]
        return None

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'


    table_group = ''


#
class Archive(models.Model):
    name = models.TextField(null=False, default="", blank=True, )
    siglum = models.CharField(max_length=255, null=False, default="", blank=True, )
    notes = models.TextField(null=False, default="", blank=True, )
    city = models.ForeignKey('City', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'Archive'
        verbose_name_plural = 'Archives'


    table_group = ''


#
class City(models.Model):
    city = models.CharField(max_length=255, null=False, default="", blank=True, )
    country = models.ForeignKey('Country', blank=False, null=False, default=1, related_name='1', )

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __unicode__(self):
        return u'%s' % (self.city)


    table_group = ''


#
class Country(models.Model):
    country = models.CharField(max_length=255, null=False, default="", blank=True, )
    countryabbrev = models.CharField(max_length=128, null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


    table_group = ''


#
class SourceType(models.Model):
    type = models.CharField(max_length=255, null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'SourceType'
        verbose_name_plural = 'SourceTypes'


    table_group = ''


#
class Year(models.Model):
    year = models.IntegerField(null=True, blank=True, )
    sourceinformation = models.ManyToManyField('SourceInformation', blank=False, null=False, default=1,
                                               through='SourceInformation_Year', )

    class Meta:
        ordering = ['year']
        verbose_name = 'Year'
        verbose_name_plural = 'Years'


    table_group = ''


#
class Dedicatee(models.Model):
    dedicatee = models.TextField(null=False, default="", blank=True, )
    alternateOf = models.ForeignKey('Dedicatee', blank=False, null=False, default=1,related_name="alternate" )

    class Meta:
        ordering = ['dedicatee']
        verbose_name = 'Dedicatee'
        verbose_name_plural = 'Dedicatees'



    table_group = ''


#
class PrintingMethod(models.Model):
    method = models.CharField(max_length=255, null=False, default="", blank=True, )


    class Meta:
        verbose_name = 'PrintingMethod'
        verbose_name_plural = 'PrintingMethods'


    table_group = ''


#
class WorkInformation(models.Model):
    generalinfo = models.TextField(null=False, default="", blank=True,
                                   help_text=ur'''Publication History for this work''', )
    relevantmanuscripts = models.TextField(null=False, default="", blank=True, )
    analysis = models.TextField(null=False, default="", blank=True, )
    OCVE= models.TextField(null=False, default="", blank=True,help_text=ur'Only field displayed in OCVE work summary' )
    class Meta:
        verbose_name = 'WorkInformation'
        verbose_name_plural = 'WorkInformations'


    table_group = ''


class AnnotationType(models.Model):
    annotationType = models.CharField(max_length=255, null=False, default="", blank=True, )


class Annotation(models.Model):
    user = models.ForeignKey(User,blank=False, null=False, default=1)
    notetext = models.TextField(null=False, default="", blank=True, )
    noteregions = models.TextField(null=False, default="", blank=True, )
    pageimage = models.ForeignKey('PageImage', blank=False, null=False, default=1 )
    type = models.ForeignKey('AnnotationType', blank=False, null=False, default=1)
    timestamp=models.DateTimeField(auto_now=True)

    def getBarRegions(self):
        return BarRegion.objects.filter(annotation_barregion__annotation=self)


    class Meta:
        verbose_name = 'Annotation'
        verbose_name_plural = 'Annotations'


    table_group = ''

class BarCollection(models.Model):
    user = models.ForeignKey(User,blank=False, null=False, default=1)
    name = models.TextField(null=False, default="", blank=True, )
    xystring = models.TextField(null=False, default="", blank=True, )
    regions = models.ManyToManyField(BarRegion)



class TreeType(models.Model):
    type = models.CharField(max_length=128, null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'TreeType'
        verbose_name_plural = 'TreeTypes'


    table_group = ''


#
class AcCode(models.Model):
    accode = models.CharField(max_length=255, null=False, default="", blank=True, )
    #sourceinformation = models.ForeignKey('SourceInformation', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'AcCode'
        verbose_name_plural = 'AcCodes'


    table_group = ''


# Many To Many Tables

#
class SourceInformation_Year(models.Model):
    sourceinformation = models.ForeignKey('SourceInformation')
    year = models.ForeignKey('Year')

#
class SourceComponent_Instrument(models.Model):
    sourcecomponent = models.ForeignKey('SourceComponent')
    instrument = models.ForeignKey('Instrument')

class SourceComponent_WorkComponent(models.Model):
    sourcecomponent = models.ForeignKey('SourceComponent')
    workcomponent = models.ForeignKey('WorkComponent')
#
class SourceInformation_PrintingMethod(models.Model):
    sourceinformation = models.ForeignKey('SourceInformation')
    printingmethod = models.ForeignKey('PrintingMethod')

#
class Genre_Work(models.Model):
    genre = models.ForeignKey('Genre')
    work = models.ForeignKey('Work')

    class Meta:
        ordering = ['work']

#
class Annotation_BarRegion(models.Model):
    annotation = models.ForeignKey('Annotation')
    barregion = models.ForeignKey('BarRegion')

class Uncertain(models.Model):
    source = models.ForeignKey('Source')
    pageimage = models.ForeignKey('PageImage')


