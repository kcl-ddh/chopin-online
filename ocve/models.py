from django.db import models
from django.conf import settings
from models_generic import *

import hashlib

# Create your models here.


class BarSpine(models.Model):
    label = models.TextField(null=False, default="", blank=True, )
    bar = models.ForeignKey('Bar', blank=False, null=False, default=1 )
    #page = models.ForeignKey('Page', blank=False, null=False, default=1 )
    sourcecomponent = models.ForeignKey('SourceComponent', blank=False, null=False, default=1 )
    orderNo = models.IntegerField(null=True, blank=True,default=0 )
    source = models.ForeignKey('Source', blank=False, null=False, default=1 )
    implied=models.IntegerField(null=True, blank=True,default=0 )


def country_unicode(self):
    return self.country

Country.__unicode__=country_unicode
Country._meta.ordering = ["country"]


def archive_unicode(self):
    return self.name

Archive.__unicode__=archive_unicode
Archive._meta.ordering = ["name"]

def work_unicode(self):
    return self.label

Work.__unicode__=work_unicode
Work._meta.ordering = ["orderno"]

def workComponent_unicode(self):
    return self.label

WorkComponent.__unicode__=workComponent_unicode
WorkComponent._meta.ordering = ["orderno"]

def source_unicode(self):
    return self.label
Source._meta.ordering = ["label"]

Source.__unicode__=source_unicode

def sourcet_unicode(self):
    return self.type

SourceType.__unicode__=sourcet_unicode

def sourcect_unicode(self):
    return self.type

SourceComponentType.__unicode__=sourcect_unicode

def WorkInformation_unicode(self):
    return str(self.id)

WorkInformation.__unicode__=WorkInformation_unicode

def PrintingMethod_unicode(self):
    return self.method

PrintingMethod.__unicode__=PrintingMethod_unicode

def SourceComponent_unicode(self):
    out=''
#    works=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent=self)
#    for w in works:
#        out+=w.label+" "
    out +=self.label
    return out

def getWorkComponentLabel(self):
    label=''
    try:
        wc=WorkComponent.objects.get(sourcecomponent_workcomponent__sourcecomponent=self)
        label=wc.label
    except ObjectDoesNotExist:
        pass
    return label

SourceComponent.getWorkComponentLabel=getWorkComponentLabel
SourceComponent.__unicode__=SourceComponent_unicode


def page_unicode(self):
    return self.label

#class Page(Page):
 #     class Meta:
  #      ordering = ["orderno"]

Page.__unicode__=page_unicode
Page._meta.ordering = ["orderno"]






#PageImage._meta.order_with_respect_to='page'

def barregion_unicode(self):
    label=''
    for b in self.bar.all():
        label+=b.barlabel
    return label

#class BarRegion(BarRegion):
 #     class Meta:
  #      ordering = ["bar.barnumber"]

BarRegion.__unicode__=barregion_unicode
#BarRegion._meta.ordering = ["bar.barnumber"]

def opus_unicode(self):
    return str(self.opusno)

Opus.__unicode__=opus_unicode
Opus._meta.ordering = ["opusno"]

def keyPitch_unicode(self):
    return self.keypitch

keyPitch.__unicode__=keyPitch_unicode
keyPitch._meta.ordering = ["orderno"]

#class toneNote(toneNote):

def keyMode_unicode(self):
    return self.keymode

keyMode.__unicode__=keyMode_unicode
keyMode._meta.ordering = ["keymode"]

def bar_unicode(self):
    return self.barlabel

#class Bar(Bar):

Bar.__unicode__=bar_unicode
Bar._meta.ordering = ["barnumber","barlabel"]

def pub_unicode(self):
    return self.publisher
Publisher.__unicode__=pub_unicode
Publisher._meta.ordering=["publisher"]

def ins_unicode(self):
    return self.instrument

Instrument.__unicode__=ins_unicode
Instrument._meta.ordering=["instrument"]

def genre_unicode(self):
    return self.genre
Genre.__unicode__=genre_unicode
Genre._meta.ordering = ["genre"]

def workc_unicode(self):
    return self.label
WorkCollection.__unicode__=workc_unicode


#Tree._meta.ordering=["level","orderNo"]

def treetype_unicode(self):
    return self.type
TreeType.__unicode__=treetype_unicode

def ac_unicode(self):
    return self.accode

AcCode.__unicode__=ac_unicode

def save(self, *args, **kwargs):
    self.accode_hash = hashlib.md5(self.accode.encode('UTF-8')).hexdigest()
    super(AcCode, self).save(*args, **kwargs)

AcCode.save = save


def dedicatee_unicode(self):
    return self.dedicatee

Dedicatee.__unicode__=dedicatee_unicode

class EditStatus(models.Model):
    status = models.CharField(max_length=255, null=False, default="NONE", blank=True, )

def sourcestatus_unicode(self):
    return self.status

EditStatus.__unicode__=sourcestatus_unicode
EditStatus._meta.ordering = ["id"]

class SourceLegacy(models.Model):
     cfeoKey = models.IntegerField(null=True, blank=True,default=0 )
     witnessKey = models.IntegerField(null=True, blank=True,default=0 )
     source = models.ForeignKey('Source', blank=False, null=False, default=1 )
     sourceDesc = models.TextField(null=False, default="", blank=True, )
     editstatus =  models.ForeignKey('EditStatus', blank=False, null=False, default=1, )
     mellon = models.BooleanField(default=False, null=False, blank=False)
     needsBarLines = models.BooleanField(default=False, null=False, blank=False)

class PageLegacy(models.Model):
    ocveKey = models.IntegerField(null=True, blank=True, )
    cfeoKey = models.IntegerField(null=True, blank=True, )
    filename = models.TextField(null=False, default="", blank=True, )
    storageStructure = models.TextField(null=False, default="", blank=True, )
    pageimage = models.ForeignKey('PageImage', blank=False, null=False, default=1, )
    cropCorrected = models.IntegerField(null=True, blank=True, default=0)
    editstatus =  models.ForeignKey('EditStatus', blank=False, null=False, default=1, )
    jp2=models.CharField(max_length=255, null=False, default="UNVERIFIED", blank=True, )

    class Meta:
        verbose_name = 'Page Legacy'
        verbose_name_plural = 'Page Legacy'

#For brand new images for brand new sources
#Moved to normal structure after audit

class NewPageImage(models.Model):
    surrogate = models.IntegerField(null=True, blank=True, )
    versionnumber = models.IntegerField(null=True, blank=True, )
    permission = models.BooleanField(default=False, null=False, blank=False, )
    permissionnote = models.CharField(max_length=255, null=False, default="", blank=True, )
    height = models.IntegerField(null=True, blank=True, )
    width = models.IntegerField(null=True, blank=True, )
    filename = models.CharField(max_length=255, null=False, default="", blank=True, )
    startbar = models.CharField(max_length=255, null=False, default="", blank=True, )
    endbar = models.CharField(max_length=255, null=False, default="", blank=True, )
    corrected = models.IntegerField(null=True, blank=True, default=0)
    linked = models.IntegerField(null=True, blank=True, default=0) #>0 if it is saved in pages/page images
    source = models.ForeignKey('NewSource', blank=False, null=False, default=1, )
    barsequences = generic.GenericRelation(BarSequence, null=True, blank=True)

    class Meta:
        verbose_name = 'NewPageImage'
        verbose_name_plural = 'NewPageImages'

class NewSource(models.Model):
    label = models.TextField(null=False, default="", blank=True, )
    library = models.TextField(null=False, default="", blank=True, )
    copyright = models.TextField(null=False, default="", blank=True, )
    sourcecode=models.CharField(max_length=255, null=False, default="", blank=True, )
    sourcecreated = models.IntegerField(null=False, blank=False,default=0 )

def newSource_unicode(self):
    label="no library given"
    if self.library is not None:
        label=self.library
    if self.sourcecode is not None:
        label=label+" - "+self.sourcecode
    return label

NewSource.__unicode__= newSource_unicode


class NewSourceInformation(models.Model):
    platenumber = models.CharField(max_length=255, null=False, default="", blank=True, )
    locationsimilarcopies = models.TextField(null=False, default="", blank=True, )
    reprints = models.TextField(null=False, default="", blank=True, )
    seriestitle = models.CharField(max_length=255, null=False, default="", blank=True, )
    copyright = models.CharField(max_length=255, null=False, default="", blank=True, )
    contentssummary = models.CharField(max_length=255, null=False, default="", blank=True, )
    contents = models.TextField(null=False, default="", blank=True, help_text=ur'''Edition text''', )
    shelfmark = models.CharField(max_length=255, null=False, default="", blank=True, )
    notes = models.TextField(null=False, default="", blank=True, )
    datepublication = models.CharField(max_length=255, null=False, default="", blank=True, )
    leaves = models.IntegerField(null=True, blank=True, )
    sourcecode = models.CharField(max_length=255, null=False, default="", blank=True, )
    title = models.TextField(null=False, default="", blank=True, )
    publicationtitle = models.TextField(null=False, default="", blank=True, )
    imagesource = models.CharField(max_length=255, null=False, default="", blank=True, )
    platenumber = models.CharField(max_length=255, null=False, default="", blank=True, )
    additionalInformation=models.TextField(null=False, default="", blank=True, )
    keyFeatures=models.TextField(null=False, default="", blank=True, )
    volume = models.CharField(max_length=255, null=False, default="", blank=True, )
    source = models.ForeignKey('NewSource', blank=False, null=False, default=1, )
    publisher = models.ForeignKey('Publisher', blank=False, null=False, default=1, )
    archive = models.ForeignKey('Archive', blank=False, null=False, default=1, )
    dedicatee = models.ForeignKey('Dedicatee', blank=False, null=False, default=1, )
    accode = models.ForeignKey('AcCode', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'SourceInformation'
        verbose_name_plural = 'SourceInformations'



def getEditStatus(self):
    try:
        sl=SourceLegacy.objects.get(source=self)
        return sl.editstatus
    except ObjectDoesNotExist:
        return ""

def getLegacy(self):
    try:
        sl=SourceLegacy.objects.get(source=self)
        return sl
    except ObjectDoesNotExist:
        return ""

Source.getEditStatus=getEditStatus
Source.getLegacy=getLegacy

def getYears(self):
    return Year.objects.filter(sourceinformation_year__sourceinformation=self)

SourceInformation.getYears=getYears

def getJP2Path(self):
    pl = PageLegacy.objects.get(pageimage=self)
    jp2 = pl.jp2
    if str(jp2).startswith('jp2/') is False:
        jp2='jp2/'+jp2
    return jp2


    #TODO: Simplify this once image name rationalisation complete
def getZoomifyPath(self):
    fullurl = settings.IIP_URL+'?zoomify='
    #pl = PageLegacy.objects.get(pageimage=self)
    jp2=self.getJP2Path()
    fullurl = fullurl + jp2 +'/'
    return fullurl

PageImage.getJP2Path=getJP2Path
PageImage.getZoomifyPath=getZoomifyPath

def annotationType_unicode(self):
    return self.annotationType
AnnotationType.__unicode__=annotationType_unicode

def year_unicode(self):
    return str(self.year)
Year.__unicode__=year_unicode
