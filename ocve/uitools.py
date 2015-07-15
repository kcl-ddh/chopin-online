__author__ = 'Elliott Hall'
#Various queries and reusable functions that will be employed in the ui.
#Kept here for the sake of hygiene, and hopefully resuability
from models import *
import json
import os
from unicodedata import normalize as _n
from django.conf import settings
from django.db import connections
from catalogue.templatetags.catalogue_tags import get_impression_exists
import urllib

import hashlib

import gzip
from django.db.models import Q

norm = 'NFKC'

#All instruments in a single opus
def getInstrumentsByOpus(opus):
    return Instrument.objects.filter(
        sourcecomponent_instrument__sourcecomponent__sourcecomponent_workcomponent__workcomponent__opus=opus).distinct()


def getBarBySource(bar, source):
    return Bar.objects.filter(barregion__page__sourcecomponent__source=source)


#Get sources within an opus that have bar
def getSourcesByBar(bar, opus):
    return Source.objects.filter(sourcecomponent__page__pageimage__barregion__bar=bar,
                                 sourcecomponent__sourcecomponent_workcomponent__workcomponent__opus=opus).distinct()



def getRegionsByBarOpus(bar, opus):
    return BarRegion.objects.filter(bar=bar,
                                    pageimage__page__sourcecomponent__sourcecomponent_workcomponent__workcomponent__opus=opus).distinct()


def getAvailableBarsByOpus(opus):
    return Bar.objects.filter(
        barregion__page__sourcecomponent__sourcecomponent_workcomponent__workcomponent__opus=opus).distinct()

#Overwrite source component label with its work components if link exists
def overwritesourcecomponentlabels(source):
    for sc in SourceComponent.objects.filter(source=source):
        wc=WorkComponent.objects.filter(sourcecomponent_workcomponent__sourcecomponent=sc)
        if wc.count() > 0:
            sc.label=wc[0].label
            sc.save()


def setPageImageTextLabel(source):
    pageimages=PageImage.objects.filter(page__sourcecomponent__source=source)
    for pi in pageimages:
        m=re.search("([\[]*[\d|ivx]+[\]]*)(.*)",pi.page.label)
        if m is not None and len(m.group(2)) > 0:
            #Correct page problem Polonaise No. 1,
            page=pi.page
            l=page.label
            l=l.replace(m.group(2),'')
            page.label=l
            page.save()
        textlabel="p. "+pi.page.label
        if pi.page.sourcecomponent.label != 'Score':
            workcomps=WorkComponent.objects.filter(sourcecomponent_workcomponent__sourcecomponent=pi.page.sourcecomponent)
            if workcomps.count() > 0:
                wc=workcomps[0]
                if wc.label != 'Score':
                    textlabel=textlabel+" "+wc.label
                    if pi.endbar != '0':
                        textlabel=textlabel+', '
        if pi.endbar != '0':
            textlabel=textlabel+" bs "+pi.startbar+u'\u2013'+pi.endbar
          #if len(pi.textlabel) == 0:
        pi.textlabel=textlabel
        pi.save()


class SourceComponentItem:
    def __init__(self, sourcecomponent):
        self.id = sourcecomponent.id
        self.label = sourcecomponent.label
        instruments=[]
        for i in Instrument.objects.filter(sourcecomponent_instrument__sourcecomponent=sourcecomponent).distinct():
            instruments.append(int(i.id))
        self.instruments = instruments
        self.source_id = sourcecomponent.source_id
        self.orderno = sourcecomponent.orderno
        #May not be needed
        #w=Work.objects.filter(workcomponent__workcomponent_sourcecomponent__sourcecomponent=sourcecomponent)
        #if w.count() > 0:
        #    self.work=w.id
        #else:
            #Non-music pages
        #    self.work=0

    def toJson(self):
        scjson = "{'id': " + str(self.id) + ", 'label': " + json.dumps(self.label) + ", "
        scjson += "'orderno': " + json.dumps(self.orderno) + ", "
        #scjson += "'work_id': " + json.dumps(self.work) + ", "
        scjson += "'source_id':" + json.dumps(self.source_id) + ','
        scjson += "'instruments':" + json.dumps(self.instruments)
        scjson += "}"
        return scjson

#s.id,s.sourcetype_id,s.label,s.cfeolabel,w.id
class SourceSearchItem:
    def  __init__(self, row, orderno,mode):
        self.orderno = orderno
        self.id = row[0]
        self.mode=mode
        self.accode = _n(norm, row[9])

        if mode == 'OCVE':
            self.label = row[2]
        else:
            self.label = row[3]
        self.label=_n(norm, self.label)
        #Anything not a manuscript is a printed edition
        #Set first edition type to printed edition
        if int(row[1]) == 3:
            self.type=1
        else:
            self.type = row[1]
        genres = []
        #if source.getWork() is not None:
        #    self.work = source.getWork().id
        for g in Genre.objects.filter(work__id=int(row[4])).distinct():
                genres.append(int(g.id))
        achash=row[11]
        if get_impression_exists(achash):
            self.achash=achash
        else:
            self.achash=''
        self.work=row[4]
        self.genres = genres
        self.keypitches =keyPitch.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source_id=self.id).distinct()
        self.keymodes =keyMode.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source_id=self.id).distinct()
        years = []
        self.dedicatee = row[5]
        self.publisher = row[6]
        self.platenumber = row[7]
        for y in Year.objects.filter(sourceinformation_year__sourceinformation_id=int(row[10])):
             years.append(y.year)
        #else:
        #    self.dedicatee = ''
        #    self.publisher = ''
        #    self.platenumber = ''
        self.years = years


    def toJson(self):
        sourcejson =  "{'id': " + str(self.id) + ", 'label': " + json.dumps(self.label) + ", "+" 'achash': " + json.dumps(self.achash) + ", "
        sourcejson += "'accode': " + json.dumps(self.accode) + ", "
        sourcejson += "'Genre': ["
        x = 1
        for g in self.genres:
            sourcejson +=  str(g)
            if x != len(self.genres):
                x += 1
                sourcejson +=  ','
        sourcejson +=  "],"
        sourcejson +=  "'KeyPitch': ["
        x = 1
        for kp in self.keypitches:
            sourcejson +=  str(kp.id)
            if x != len(self.keypitches):
                x += 1
                sourcejson +=  ','
        sourcejson +=  "],"
        sourcejson +=  "'KeyMode': ["
        x = 1
        for kp in self.keymodes:
            sourcejson +=  str(kp.id)
            if x != len(self.keymodes):
                x += 1
                sourcejson +=  ','
        sourcejson +=  "],"
        sourcejson +=  "'Dedicatee': " + str(self.dedicatee) + ", 'Work':" + str(self.work)
        sourcejson +=  ",'Year': " + json.dumps(self.years) + ", "
        sourcejson +=  "'Publisher': " + str(self.publisher) + ","
        sourcejson +=  "'Type': " + str(self.type) + ","
        sourcejson +=  "'Pages': ["
        if self.mode == 'OCVE':
            #Filter out non-musical pages like blanks, title pages etc.
            #musicpage=PageType.objects.get(type='music')
            blank=PageType.objects.get(type='blank')
            #tp=PageType.objects.get(type='title page')
            #nonmusic=SourceComponentType.objects.get(type="Non-music")
            #.exclude(page__sourcecomponent__sourcecomponenttype=blank)
            #.exclude(page__sourcecomponent__sourcecomponenttype=nonmusic)
            pages = PageImage.objects.filter(page__sourcecomponent__source_id=self.id).exclude(page__pagetype_id__lt=2).exclude(page__pagetype=blank).order_by("page__sourcecomponent","page")
        else:
            pages = PageImage.objects.filter(page__sourcecomponent__source_id=self.id).order_by("page__sourcecomponent","page")
        for pi in pages:
            if pi != pages[0]:
                sourcejson +=  ','
            sourcejson +=  PageSearchItem(self.id,self.work, pi,self.dedicatee,self.publisher,self.years).toJson()
        sourcejson +=  "]"
        sourcejson +=  ", 'orderno':" + json.dumps(self.orderno)
        sourcejson +=  "}"
        return sourcejson


#(page no with bar range)
class PageSearchItem:
    def __init__(self, source,work, pageimage,dedicatee,publisher,years):
        self.id = pageimage.id
        self.source_id = source
        self.thumbnail_url = pageimage.getJP2Path()
        self.width = pageimage.width
        self.height = pageimage.height
        self.orderno = pageimage.page.orderno
        self.label = pageimage.textlabel
        self.sourcecomponent_id = pageimage.page.sourcecomponent.id
        self.sourcecomponent_orderno = pageimage.page.sourcecomponent.orderno
        self.type = pageimage.page.pagetype.id
        self.work = 0
        self.keypitch = 0
        self.keymode = 0
        genres = []

        if work > 0:
            wc = WorkComponent.objects.filter(sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pageimage)
            if wc.count() > 0:
                self.keypitch = wc[0].keypitch.id
                self.keymode = wc[0].keymode.id
                self.work = wc[0].work.id
            for g in Genre.objects.filter(work__id=work).distinct():
                genres.append(int(g.id))
        self.genres = genres
        self.dedicatee = dedicatee
        self.publisher = publisher
        self.years = years
        #self.publicationDate=
        #self.key=

    def toJson(self):
        pagejson =  "{'id': " + str(self.id) + ", 'label': " + json.dumps(
            self.label) + ", 'source_id':" + json.dumps(self.source_id) + ','
        pagejson +=  "'sourcecomponent_id': " + json.dumps(self.sourcecomponent_id) + ", "
        pagejson +=  "'sourcecomponent_orderno': " + json.dumps(self.sourcecomponent_orderno) + ", "
        pagejson +=  "'Genre': " + json.dumps(self.genres) + ", "
        pagejson +=  "'Year': " + json.dumps(self.years) + ", "
        pagejson +=  "'Dedicatee': " + json.dumps(self.dedicatee) + ", 'Work':" + json.dumps(self.work)
        pagejson +=  ", 'Publisher': " + json.dumps(self.publisher)
        pagejson +=  ", 'thumbnail_url':" + json.dumps(self.thumbnail_url)
        pagejson +=  ", 'width':" + json.dumps(self.width)
        pagejson +=  ", 'height':" + json.dumps(self.height) + ","
        pagejson +=  "'PageType': " + str(self.type) + ","
        pagejson +=  "'KeyPitch': " + str(self.keypitch) + ","
        pagejson +=  "'KeyMode': " + str(self.keymode)
        pagejson +=  ", 'orderno':" + json.dumps(self.orderno)
        pagejson +=  "}"
        return pagejson

def serializeOCVESourceJson():
    #sources = Source.objects.filter(ocve=True).order_by(
    #    'sourcecomponent__sourcecomponent_workcomponent__workcomponent__work__orderno', 'orderno').distinct()
    sourcecomponents = SourceComponent.objects.filter(source__ocve=True).distinct()
    serializeSourceJson(sourcecomponents,'OCVEsourceJSON','OCVE')

def serializeCFEOSourceJson():
    #sources = Source.objects.filter(cfeo=True).order_by(
    #    'sourcecomponent__sourcecomponent_workcomponent__workcomponent__work__orderno', 'orderno').distinct()
    sourcecomponents = SourceComponent.objects.filter(source__cfeo=True).distinct()
    serializeSourceJson(sourcecomponents,'CFEOsourceJSON','CFEO')

def serializeSourceJson(sourcecomponents,filename,mode):
    #sources=Source.objects.filter(sourcelegacy__witnessKey__gt=0).order_by('sourcecomponent__sourcecomponent_workcomponent__workcomponent__work__orderno','label').distinct()
    #all sources with bar info
    destination = open(settings.SOURCEJSONPATH+'/'+filename+'.js', 'w')
    destination.write('var sourcecomponents = [')
    for idx, sc in enumerate(sourcecomponents):
        if idx != 0:
            destination.write(',\n')
        destination.write(SourceComponentItem(sc).toJson())
    destination.write('];\n\n')
    destination.write('var sources = [')
    orderno = 1
    if mode == 'CFEO':
        modeSQL="s.cfeo=1"
    else:
        modeSQL="s.ocve=1"
    cursor = connections['ocve_db'].cursor()
    sql="select distinct s.id,s.sourcetype_id,s.label,s.cfeolabel,w.id,si.dedicatee_id,si.publisher_id,si.platenumber,si.sourcecode,ac.accode,si.id,ac.accode_hash"
    sql+=" from ocve_source as s,ocve_accode as ac,ocve_sourceinformation as si,ocve_sourcecomponent as sc,ocve_sourcecomponent_workcomponent as scwc, ocve_workcomponent as wc, ocve_work as w"
    sql+=" where "+modeSQL+" and si.accode_id=ac.id and s.id=sc.source_id and s.id=si.source_id and sc.id=scwc.sourcecomponent_id and scwc.workcomponent_id = wc.id and wc.work_id=w.id"
    sql+=" order by w.orderno,s.orderno"
    cursor.execute(sql)
    for row in cursor.fetchall():
        if orderno >1:
            destination.write(',\n')
        destination.write(SourceSearchItem(row, orderno,mode).toJson())
        orderno += 1
    destination.write(']')
    destination.close()
    #Gzip results
    f_in = open(settings.SOURCEJSONPATH+'/'+filename+'.js', 'rb')
    f_out = gzip.open(settings.SOURCEJSONPATH+'/'+filename+'.js.gz', 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()




#
def serializeAcCodeConnector():
    sources=Source.objects.filter(Q(ocve=1)|Q(cfeo=1))
    destination = open(settings.SOURCEJSONPATH+ '/accodeJSON.js', 'wb')
    destination.write('var sources = [')
    first = 0
    for s in sources:
        if s.getSourceInformation() is not None and s.getSourceInformation().accode is not None:
            if s.cfeo ==1 or s.ocve == 1:
                if first > 0:
                    destination.write(',\n')
                accode=s.getSourceInformation().accode.accode
                acHash=s.getSourceInformation().accode.accode_hash
                acjson =  "{'accode':"+json.dumps(accode)+",'achash':"+json.dumps(acHash)+",'id':"+json.dumps(s.id)
                if s.cfeo == 1:
                    acjson  += ",'cfeo':1"
                if s.ocve == 1:
                    acjson  += ",'ocve':1"
                acjson +=  "}"
                destination.write(acjson)
                first=1
    destination.write(']')
    destination.close()


#Get the pageimages from a source, filtered to include only music pages and the title page
#filter(Q(page__pagetype=musicpage)|Q(page__pagetype=tp)).
def getOCVEPageImages(source):
    try:
        blank=PageType.objects.get(type='blank')
        tp=PageType.objects.get(type='title page')
        pi=PageImage.objects.filter(page__sourcecomponent__source=source).exclude(page__pagetype_id__lt=2).exclude(page__pagetype=blank).order_by('page__orderno')
        return pi
    except IndexError:
        return []
    except ObjectDoesNotExist:
        return []


def generateThumbnails(sources):
    log=""
    for s in sources:
        pageimages=PageImage.objects.filter(page__sourcecomponent__source=s)
        log+="\nFor source "+str(s.id)
        for pi in pageimages:
            log+="\n"+generateThumbnail(pi)
    return log

def generateThumbnail(pageimage):
    result=""
    #Get page legacy for jp2 path
    path=pageimage.getJP2Path()
    if len(path) > 0:
        #Query iip server for deepzoom
        path=settings.IMAGE_SERVER_URL+'?DeepZoom='+path+'_files/0/0_0.jpg'
        #Save in thumbnial using pageimage id
        thumb=os.path.join(settings.THUMBNAIL_DIR,str(pageimage.id)+".jpg")
        result="Saving "+path+" at "+thumb
        try:
            urllib.urlretrieve(path, thumb)
        except IOError:
            result=IOError.message
    return result
