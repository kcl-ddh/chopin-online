import re
#from django.db.models.sql.aggregates import Max
from django.http import HttpResponse

__author__ = 'Elliot'

from ocve.models import *
from django.db import connections, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from ocve.imagetools import verifyImageDimensions
from django.core.management.base import NoArgsCommand

from unicodedata import normalize as _n


#INSERT INTO ocve_country (country,countryabbrev) SELECT country,countryAbbrev FROM country
#INSERT INTO ocve_city VALUES (1,'unspecified');
#INSERT INTO ocve_city VALUES (2,'none');
#Page_Image.page_imageKey,Page_Image.instrumentKey,Page_Image.witnessKey,Page_Image.filename,Page_Image.pageID,Page_Image.notes,Page_Image.orderNo,Page_Image.CFEOeditionKey,Page_Image.storageStructure,Page_Image.pageNumber,Page_Image.startBar,Page_Image.startBarExt,Page_Image.endBar,Page_Image.endBarExt,Page_Image.sourceHeight,Page_Image.sourceWidth
#PIQ.setFromString("WitnessPage_intersection,BarRegion");
#PIQ.setWhereString("Page_Image.page_imageKey=BarRegion.page_imageKey and WitnessPage_intersection.pageImageKey=Page_Image.page_imageKey and WitnessPage_intersection.witnessKey="+getWitnessKey());
#PIQ.setOrderString("orderNo");

log = '<html><head><title>Upload Log</title></head><body>'

#All dicts store new objects indexed by old OCVE key
cities = {}
countries = {}
archives = {}
sources = {}
witnesses = {}
publishers = {}
sourceEditions = {}
CFEOSourceComponents = {}
worksHash = {}
compHash = {}
pieces = {}
#Work keys of works that are separated for special cases like posthumous
excKeys = "65"

def importAnnotations():
    cType=AnnotationType.objects.get(id=2)
    cuser=User.objects.get(id=12)
    cursor = connections['ocve_db'].cursor()
    cursor.execute("select a.annotationKey,a.text,a.timestamp from annotation as a where a.ocve=-1")
    Annotation.objects.all().delete()
    for row in cursor.fetchall():
        note=Annotation()
        note.type=cType
        note.notetext=row[1]
        note.user=cuser
        aKey=row[0]
        c2=connections['ocve_db'].cursor()
        c2.execute("select b.barNumber,b.barNumberExtra,ba.witnessKey from bar as b,barannotation as ba where ba.annotationKey="+str(aKey)+" and b.barKey=ba.barKey")
        for barRow in c2.fetchall():
            regions=BarRegion.objects.filter(pageimage__page__sourcecomponent__source__sourcelegacy__witnessKey=int(barRow[2]),bar__barnumber=int(barRow[0]))
            for r in regions:
                if note.pageimage_id ==1:
                    note.pageimage=r.pageimage
                    note.save()
                Annotation_BarRegion(annotation=note,barregion=r).save()




#One-time fix for bar range error row[0]
def fixBarRange():
    cursor = connections['ocve_db'].cursor()
    cursor.execute(
        "SELECT pi.id,pi.startbar,pi.endbar,min(b.barnumber),max(b.barnumber) FROM ocve_pageimage as pi , ocve_barregion as br, ocve_bar as b, ocve_bar_barregion as brr where br.pageimage_id=pi.id and br.id=brr.barregion_id and brr.bar_id=b.id group by pi.id")
    log = '<html><head></head><body><ul>'
    for row in cursor.fetchall():
        lowestBarNumber = int(row[3])
        highestBarNumber = int(row[4])
        p = PageImage.objects.get(id=int(row[0]))
        smatch = re.search('(\d+)', row[1])
        if smatch:
            startbar = int(smatch.group(1))
            if lowestBarNumber != startbar:
                p.startbar = lowestBarNumber
                log += '<li>pageimage id:' + str(p.id) + ', startbar:' + str(
                    p.startbar) + ' but first bar number:' + str(lowestBarNumber) + '</li>'
                p.save()
        smatch = re.search('(\d+)', row[2])
        if smatch:
            endbar = int(smatch.group(1))
            if highestBarNumber != endbar:
                p.endbar = highestBarNumber
                log += '<li>pageimage id:' + str(p.id) + ', endbar:' + str(p.endbar) + ' but end bar number:' + str(
                    lowestBarNumber) + '</li>'
                p.save()
    log += '</ul></body></html>'
    return log


#A one-time function to correct problems in the merging of phase 1 OCVE/CFEO databases
def uploadOCVEOpus28():
    #Get all sources for opus 28
    cursor = connections['ocve_db'].cursor()
    log = "<html><head></head><body><table>"
    sourceKey = 0
    #Different order Ocve 1 to 2
    preludes = Work.objects.get(id=6355)
    #preludeSources=Source.objects.filter(sourcecomponent__sourcecomponent_workcomponent__workcomponent__work_id=preludes.id)
    #preludeSources.delete()
    stypes = ['', SourceType.objects.get(id=2), SourceType.objects.get(id=3), SourceType.objects.get(id=1)]
    opus28WorkComponents = WorkComponent.objects.filter(opus_id=6609)
    scType = SourceComponentType.objects.get(type="Piano Score")
    #Witness.witnessKey,Witness.pieceKey,Witness.sourceKey,Witness.CFEOeditionKey,Witness.witnessDescription,,Witness.full_text_c
    cursor.execute(
        "SELECT Witness.sourceKey,Witness.witnessDescription,source.sourceTypeKey,Witness.full_text_c,Witness.publisherAbbrev,Witness.witnessKey FROM witness as Witness,piece as p,source where Witness.pieceKey=p.pieceKey and p.opusNo=28 and Witness.sourceKey=source.sourceKey group by sourceKey")
    for row in cursor.fetchall():
        try:
            si = SourceInformation.objects.get(source__sourcelegacy__witnessKey=int(row[5]))
            s = si.source
        except ObjectDoesNotExist:
            sourceKey = int(row[0])
            label = row[1]
            stype = stypes[int(row[2])]
            witnessKey = row[5]
            #Merge them by source into single sources with multiple components
            #if SourceLegacy.objects.filter(witnessKey=sourceKey).count() ==0:
            s = Source(label=label, cfeolabel='', sourcetype=stype)
            s.save()
            sourceDesc = row[3]
            sl = SourceLegacy(cfeoKey=0, witnessKey=witnessKey, source=s, sourceDesc=sourceDesc)
            sl.save()
            si = None
            if sourceDesc is not None:
                si = parseSourceDesc(s, sourceDesc)
                #Create new source component to hold the score
            if si is None:
                si = SourceInformation(source=s)
            publisher = None
            publisherAbbrev = row[4]
            if publisherAbbrev.__len__ > 0:
                try:
                    publisher = Publisher.objects.get(publisherAbbrev=publisherAbbrev)
                except ObjectDoesNotExist:
                    #New publisher
                    publisher = Publisher(publisherAbbrev=publisherAbbrev, publisher='Unknown')
                    publisher.save()
                except MultipleObjectsReturned:
                    publisher = Publisher.objects.filter(publisherAbbrev=publisherAbbrev)[0]
            si.publisher = publisher
            #Get rest of metadata from old source table (c2 is new cursor)
            c2 = connections['ocve_db'].cursor()
            c2.execute(
                "SELECT ai.shelfmark,a.code from source as s,archive as a,archiveitem as ai where s.archiveItemKey=ai.archiveItemKey and ai.archiveKey=a.archiveKey and s.sourceKey= " + str(
                    row[2]))
            for meta in c2.fetchall():
                si.shelfmark = meta[0]
                try:
                    si.archive = Archive.objects.get(siglum=meta[1])
                except ObjectDoesNotExist:
                    si.archive = Archive.objects.get(id=1)
            if si.leaves is None:
                si.leaves = '0'
            si.save()

            witCursor = connections['ocve_db'].cursor()
            witCursor.execute("SELECT Witness.witnessKey,Witness.pieceKey,Witness.sourceKey,Witness.CFEOeditionKey,"
                              "Witness.witnessDescription,Witness.publisherAbbrev,Witness.full_text_c,Piece.opusPartNo FROM witness as Witness,piece as Piece where Witness.pieceKey=Piece.pieceKey and Witness.sourceKey=" + str(
                sourceKey) + " order by witnessKey")
            orderNo = 1
            for witRow in witCursor.fetchall():
                #For each witness matching the source
                No = witRow[7]
                label = 'Prelude No. ' + str(No)
                #Create new source component
                newSComp = SourceComponent(source=s, orderno=orderNo, label=label, sourcecomponenttype=scType,
                                           overridelabel=label)
                newSComp.save()
                orderNo += 1
                #Attach new source to correct work component
                wc = WorkComponent.objects.get(label=label)
                SourceComponent_WorkComponent(sourcecomponent=newSComp, workcomponent=wc).save()
                #Attach pages from that witness to source component
                importPageImage(newSComp, int(witRow[0]))
            log += "<tr><td>" + str(row[0]) + "</td><td>" + str(row[4]) + "</td></tr>"


def fixKeys():
    cursor = connections['ocve_db'].cursor()
    #cursor.execute("SELECT owc.id,wc.componentKey,ta.tonart,km.id FROM ocve_workcomponent as owc,workcomponent as wc,work as w,ocve_opus as o, ocve_keymode as km,tonart as t,tonartal as ta where owc.orderno=wc.orderNo and owc.opus_id=o.id and o.opusno=w.opusNo and w.workKey=wc.workKey and wc.componentKey=t.componentKey and ta.tonartKey=t.tonartKey and ta.tonart regexp km.keymode order by wc.componentKey ")
    #for row in cursor.fetchall():
    #wc=WorkComponent.objects.get(id=int(row[0]))
    #km=keyMode.objects.get(id=int(row[3]))
    #wc.keymode=km
    #wc.save()

    cursor.execute(
        "SELECT owc.id,wc.componentKey,ta.tonart,kp.id FROM ocve_workcomponent as owc,workcomponent as wc,work as w,ocve_opus as o, ocve_keypitch as kp,tonart as t,tonartal as ta where owc.orderno=wc.orderNo and owc.opus_id=o.id and o.opusno=w.opusNo and w.workKey=wc.workKey and wc.componentKey=t.componentKey and ta.tonartKey=t.tonartKey and ta.tonart regexp concat('^',kp.keypitch,' ') order by wc.componentKey")
    for row in cursor.fetchall():
        wc = WorkComponent.objects.get(id=int(row[0]))
        kp = keyPitch.objects.get(id=int(row[3]))
        wc.keypitch = kp
        wc.save()


def upload(request):
    cursor = connections['ocve_db'].cursor()
    resetTables()
    initialValues()
    importAuthorityLists()
    importArchives()
    uploadOCVE()
    uploadCFEO()
    return log


def uploadOCVE():
    importPiece()
    importWitness()


def uploadCFEO():
    #importCFEOWorks()
    importEditions()
    #importCFEOWorkComponents()


def resetTables():
    Archive.objects.all().delete()
    cursor = connections['ocve_db'].cursor()
    #cursor.execute("INSERT INTO ocve_country (country,countryabbrev) SELECT country,countryAbbrev FROM country")
    cursor.execute("DELETE FROM ocve_sourcecomponent_instrument")
    cursor.execute("DELETE FROM ocve_sourcecomponent_workcomponent")
    cursor.execute("DELETE FROM ocve_genre_work")
    cursor.execute("DELETE FROM ocve3.ocve_workcomponent")
    cursor.execute("DELETE FROM ocve3.ocve_work")
    cursor.execute("DELETE FROM ocve3.ocve_workinformation")
    cursor.execute("DELETE FROM ocve3.ocve_pagelegacy")
    cursor.execute("DELETE FROM ocve3.ocve_pageimage")
    cursor.execute("DELETE FROM ocve3.ocve_page")
    cursor.execute("DELETE FROM ocve3.ocve_sourcecomponent")
    cursor.execute("DELETE FROM ocve3.ocve_sourcelegacy")
    cursor.execute("DELETE FROM ocve3.ocve_source")
    cursor.execute("DELETE FROM ocve3.ocve_sourceinformation")
    cursor.execute("DELETE FROM ocve3.ocve_barregion")
    cursor.execute("DELETE FROM ocve3.ocve_accode")
    cursor.execute("DELETE FROM ocve3.ocve_keypitch")
    transaction.commit_unless_managed()
    Publisher.objects.all().delete()
    #Authority Lists
    Genre.objects.all().delete()
    Instrument.objects.all().delete()
    Dedicatee.objects.all().delete()
    City.objects.all().delete()
    Country.objects.all().delete()
    Opus.objects.all().delete()
    CollectionType.objects.all().delete()
    WorkCollection.objects.all().delete()
    SourceComponentType.objects.all().delete()
    #SourceComponent.objects.all().delete()
    PageType.objects.all().delete()
    #Intersection Sets


#Set up default values for all authority lists
def initialValues():
    uns = "Unspecified"
    none = "None"
    Opus(id=1, opusno=0).save()
    Genre(id=1, genre=uns).save()
    Genre(id=2, genre=none).save()
    Dedicatee(id=1, dedicatee=uns).save()
    Dedicatee(id=2, dedicatee=none).save()
    AcCode(id=1, accode=uns).save()
    AcCode(id=2, accode=none).save()
    Publisher(id=1, publisher=uns, publisherAbbrev='').save()
    Publisher(id=2, publisher=none, publisherAbbrev='0').save()
    PageType(id=1, type=uns).save()
    PageType(id=2, type=none).save()
    PageType(id=3, type='music').save()
    PageType(id=4, type='title page').save()
    PageType(id=5, type='blank').save()
    Country(id=1, country=uns).save()
    noneC = Country(id=2, country=none)
    noneC.save()
    City(id=1, country=noneC, city=uns).save()
    noneCity = City(id=2, country=noneC, city=none)
    noneCity.save()
    Archive(id=1, name=uns, siglum='', notes='', city=noneCity).save()
    Archive(id=2, name=none, siglum='', notes='', city=noneCity).save()
    keyPitch(id=1, keypitch=uns).save()
    keyPitch(id=2, keypitch=none).save()
    Instrument(id=1, instrument=uns).save()
    Instrument(id=2, instrument=none).save()
    unsct = CollectionType(id=1, type=uns)
    unsct.save()
    nonect = CollectionType(id=2, type=none)
    nonect.save()
    ct = CollectionType(id=3, type='Posthumous')
    ct.save()
    addWorkCollection()
    cursor = connections['ocve_db'].cursor()
    #Tone Keys
    keyMode(id=1, keymode=uns).save()
    keyMode(id=2, keymode=none).save()
    keyMode(id=1, keymode='Major').save()
    keyMode(id=1, keymode='Minor').save()
    #SourceComponentType
    cursor.execute("INSERT INTO ocve_sourcecomponenttype (type) VALUES('Unspecified')")
    cursor.execute("INSERT INTO ocve_sourcecomponenttype (type) VALUES('Piano Score')")
    cursor.execute("INSERT INTO ocve_sourcecomponenttype (type) VALUES('Single Instrument')")
    cursor.execute("INSERT INTO ocve_sourcecomponenttype (type) VALUES('Multiple Instrument')")
    cursor.execute("INSERT INTO ocve_sourcecomponenttype (type) VALUES('Orchestral')")
    cursor.execute("INSERT INTO ocve_sourcecomponenttype (type) VALUES('Manuscript')")
    transaction.commit_unless_managed()


#Import authority list values from OCVE and CFEO to new db structure
def importAuthorityLists():
    importGenre()
    importPublisher()
    #importInstrument()
    cursor = connections['ocve_db'].cursor()
    #cursor.execute("INSERT INTO ocve_country (country,countryabbrev) SELECT country,countryAbbrev FROM country")
    cursor.execute("INSERT INTO ocve3.ocve_opus (opusno) SELECT opusNo FROM ocve3.opusal")
    #INSERT INTO ocve_tonenote (toneNote) SELECT REPLACE(tonart,' major','')   FROM ocve3.tonartal t where tonart regexp '.*major.*' order by tonart;
    #INSERT INTO ocve_bar (barnumber,barlabel) SELECT barNumber,barNumber FROM bar;
    transaction.commit_unless_managed()
    importCountries()
    importCities()
    importTonart()


def importCountries():
    global countries
    cursor = connections['ocve_db'].cursor()
    cursor.execute("SELECT countryKey,country,countryAbbrev from Country order by countryKey")
    for row in cursor.fetchall():
        c = Country(country=row[1], countryabbrev=row[2])
        c.save()
        countries[str(row[0])] = c
    transaction.commit_unless_managed()


def importCities():
    global cities
    cursor = connections['ocve_db'].cursor()
    cursor.execute("SELECT cityKey,countryKey,city from City order by cityKey")
    for row in cursor.fetchall():
        c = countries[str(row[1])]
        city = City(country=c, city=row[2])
        city.save()
        cities[str(row[0])] = city
    transaction.commit_unless_managed()


#NOTE:  Imports only the pitch, filtering out mode
def importTonart():
    cursor = connections['ocve_db'].cursor()
    cursor.execute("SELECT tonart,orderNo from tonartal")
    for row in cursor.fetchall():
        pitch = row[0]
        pitch = pitch.replace(' major', '').replace(' minor', '')
        try:
            keyPitch.objects.get(keypitch=pitch)
        except ObjectDoesNotExist:
            k = keyPitch(keypitch=row[0], orderNo=row[1])
            k.save()
    transaction.commit_unless_managed()
    pass


#Import OCVE bar regions and translate to new structure
def importBarRegions(pi, p, ocvePageKey):
    cursor = connections['ocve_db'].cursor()
    barDict = buildBarDict()
    cursor.execute("SELECT barKey,page_imageKey,x1,y1,x2,y2 FROM barregion where page_imageKey=" + str(ocvePageKey))
    #p=Page.objects.get(id=4)
    for row in cursor.fetchall():
        x = row[2]
        y = row[3]
        width = row[4] - x
        height = row[5] - y
        barid = barDict[row[0]]
        try:
            bar = Bar.objects.get(id=int(barid))
        except ObjectDoesNotExist:
            bar = Bar.objects.get(barnumber=0)
        br = BarRegion(x=x, y=y, width=width, height=height, page=p, pageimage=pi)
        br.save()
        Bar_BarRegion(bar=bar, barregion=br).save()
    transaction.commit_unless_managed()


def buildBarDict():
    cursor = connections['ocve_db'].cursor()
    cursor.execute("SELECT barKey,barNumber FROM bar order by barKey ")
    barDict = {}
    for row in cursor.fetchall():
        barDict[row[0]] = row[1]
    transaction.commit_unless_managed()
    return barDict


def importPublisher():
    cursor = connections['ocve_db'].cursor()
    global publishers
    cursor.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    cursor.execute("SELECT publisherKey,publisherAbbrev,publisherName from publisheral ")
    for row in cursor.fetchall():
        p = Publisher(publisher=str(row[2]), publisherAbbrev=str(row[1]), notes='')
        p.save()
        publishers[str(row[0])] = p


def importInstrument():
    cursor = connections['ocve_db'].cursor()
    cursor.execute("SELECT instrumentKey,instrumentName,instrumentAbbrev FROM instrumental ")
    for row in cursor.fetchall():
        Instrument(id=int(row[0]), instrument=str(row[1]), instrumentabbrev=str(row[2])).save()


def importGenre():
    cursor = connections['ocve_db'].cursor()
    #OCVE Genres
    cursor.execute("SELECT genreKey,genreName,pluralName from genreal ")
    for row in cursor.fetchall():
        g = Genre(genre=str(row[1]), pluralname=str(row[2]))
        g.save()
        #CFEO
    cursor.execute("SELECT genreKey,genreName,altName from algenre ")
    for row in cursor.fetchall():
        try:
            Genre.objects.get(genre=str(row[1]))
        except ObjectDoesNotExist:
            g = Genre(genre=str(row[1]), pluralname='')
            g.save()
    transaction.commit_unless_managed()


def lookupGenre(genreKey, CFEO):
    cursor = connections['ocve_db'].cursor()
    row = None
    if CFEO == 1:
        cursor.execute("SELECT genreKey,genreName,altName from algenre where genreKey=" + str(genreKey))
        row = cursor.fetchone()
    else:
        cursor.execute("SELECT genreKey,genreName,pluralName from genreal where genreKey=" + str(genreKey))
        row = cursor.fetchone()
    if row is not None:
        try:
            g = Genre.objects.get(genre=str(row[1]))
            return g
        except ObjectDoesNotExist:
            return None
    return None


def importArchives():
    cursor = connections['ocve_db'].cursor()
    global archives
    cursor.execute("SELECT archiveKey,cityKey,archiveName,archiveSiglum from o_archive ")
    for row in cursor.fetchall():
        city = cities[str(row[1])]
        name = convertEntities(str(row[2]))
        a = Archive(city=city, name=name, siglum=str(row[3]))
        a.save()
        archives[str(row[0])] = a


def parseSourceDesc(s, sourceDesc):
    sourceDesc = convertEntities(sourceDesc)
    codeMatch = re.search("<label>Source code</label>\s*<value>(.*?)</value>", sourceDesc, re.IGNORECASE | re.MULTILINE)
    infoMatch = re.search("<label>Additional information</label>\s*<value>(.*?)</value>", sourceDesc,
                          re.IGNORECASE | re.MULTILINE)
    featuresMatch = re.search("<heading>Key features:</heading>\s*<para>(.*?)</para>", sourceDesc,
                              re.IGNORECASE | re.MULTILINE)
    contentsSummaryMatch = re.search("<label>Contents</label>\s*<value><heading>(.*?)</heading>", sourceDesc,
                                     re.IGNORECASE | re.MULTILINE)
    publicationTitleMatch = re.search("<label>Publication title</label>\s*<value>(.*?)</value>", sourceDesc,
                                      re.IGNORECASE | re.MULTILINE)
    placePublicationMatch = re.search("<label>Place of publication</label>\s*<value>(.*?)</value>", sourceDesc,
                                      re.IGNORECASE | re.MULTILINE)
    publicationDateMatch = re.search("<label>Publication date</label>\s*<value>(.*?)</value>", sourceDesc,
                                     re.IGNORECASE | re.MULTILINE)
    sourceCode = ''
    additionalInformation = ''
    keyFeatures = ''
    contentsSummary = ''
    pubtitle = ''
    datePublication = ''
    if codeMatch is not None:
        sourceCode = codeMatch.group(1)
    if infoMatch is not None:
        additionalInformation = infoMatch.group(1)
    if featuresMatch is not None:
        keyFeatures = featuresMatch.group(1)
    if contentsSummaryMatch is not None:
        contentsSummary = contentsSummaryMatch.group(1)
    if publicationTitleMatch is not None:
        pubtitle = publicationTitleMatch.group(1)
    c = City.objects.get(id=1)
    if placePublicationMatch is not None:
        place = placePublicationMatch.group(1)
        try:
            c = City.objects.get(city__iexact=place)
        except ObjectDoesNotExist:
            pass
    if publicationDateMatch is not None:
        datePublication = publicationDateMatch.group(1)
    dedicateeMatch = re.search("<label>Dedicatee</label>\s*<value>(.*?)</value>", sourceDesc,
                               re.IGNORECASE | re.MULTILINE)
    dedicatee = None
    if dedicateeMatch is not None:
        ded = dedicateeMatch.group(1)
        if len(ded) > 0:
            try:
                dedicatee = Dedicatee.objects.get(dedicatee=ded)
            except ObjectDoesNotExist:
                d = Dedicatee(dedicatee=ded)
                d.save()
    if dedicatee == None:
        dedicatee = Dedicatee.objects.get(id=1)
    publisher = Publisher.objects.get(id=1)
    archive = Archive.objects.get(id=1)
    si = SourceInformation(archive=archive, placepublication=c, datepublication=datePublication, publisher=publisher,
                           dedicatee=dedicatee, publicationtitle=pubtitle, contentssummary=contentsSummary,
                           additionalInformation=additionalInformation, keyFeatures=keyFeatures, sourcecode=sourceCode,
                           source=s, leaves='0')
    si.save()
    return si


#Generate new source table from CFEO, OCVE sources
def importWitness():
    cursor = connections['ocve_db'].cursor()
    #todo: ChristopheTextWitness,Witness.notes,Witness.designation,Witness.designationSuperscript, removed for now due to unicode errors
    cursor.execute(
        "SELECT Witness.witnessKey,Witness.pieceKey,Witness.sourceKey,Witness.CFEOeditionKey,Witness.witnessDescription,Witness.publisherAbbrev,Witness.full_text_c FROM Witness where Witness.pieceKey<3 or Witness.pieceKey>26 order by witnessKey")
    for row in cursor.fetchall():
        #Create new source
        st = getSourceType(row[2])
        CFEOkey = int(row[3])
        publisherAbbrev = row[5]
        sourceDesc = row[6]
        s = None
        witnessKey = int(row[0])
        #Create new components
        stype = SourceType.objects.get(type='Printed Edition')
        label = convertEntities(row[4])
        if '0' in publisherAbbrev:
            stype = SourceType.objects.get(type='Manuscript')
        s = Source(label=label, cfeolabel='', sourcetype=stype)
        s.save()
        sl = SourceLegacy(cfeoKey=CFEOkey, witnessKey=witnessKey, source=s, sourceDesc=sourceDesc)
        sl.save()
        si = None
        if sourceDesc is not None:
            si = parseSourceDesc(s, sourceDesc)
            #Create new source component to hold the score
        if si is None:
            si = SourceInformation(source=s)
        publisher = None
        if publisherAbbrev.__len__ > 0:
            try:
                publisher = Publisher.objects.get(publisherAbbrev=publisherAbbrev)
            except ObjectDoesNotExist:
                #New publisher
                publisher = Publisher(publisherAbbrev=publisherAbbrev, publisher='Unknown')
                publisher.save()
        si.publisher = publisher
        #Get rest of metadata from old source table (c2 is new cursor)
        c2 = connections['ocve_db'].cursor()
        c2.execute(
            "SELECT ai.shelfmark,a.code from Source as s,Archive as a,ArchiveItem as ai where s.archiveItemKey=ai.archiveItemKey and ai.archiveKey=a.archiveKey and s.sourceKey= " + str(
                row[2]))
        for meta in c2.fetchall():
            si.shelfmark = meta[0]
            try:
                si.archive = Archive.objects.get(siglum=meta[1])
            except ObjectDoesNotExist:
                si.archive = Archive.objects.get(id=1)
        if si.leaves is None:
            si.leaves = '0'
        si.save()
        scType = SourceComponentType.objects.get(type="Piano Score")
        label = 'Score'
        newSComp = SourceComponent(source=s, orderno=1, label=label, sourcecomponenttype=scType,
                                   overridelabel=label)
        newSComp.save()
        wc = pieces[int(row[1])]
        SourceComponent_WorkComponent(sourcecomponent=newSComp, workcomponent=wc).save()
        #New Source Information
        #todo Overwrite CFEO source information?
        #import pages in witness
        importPageImage(newSComp, witnessKey)


def importPiece():
    #Piece = WorkComponent (almost)
    global pieces
    wc = WorkCollection.objects.get(label__iexact='None')
    km = keyMode.objects.get(id=2)
    kp = keyPitch.objects.get(id=2)
    cursor = connections['ocve_db'].cursor()
    cursor.execute(
        "SELECT Piece.pieceKey,Piece.opusNo,Piece.genreKey,Piece.tonartKey,Piece.opusPartNo,Piece.ChristopheTextPiece,Piece.pieceDescription FROM Piece where Piece.opusNo!=28 order by orderNo")
    for row in cursor.fetchall():
        g = lookupGenre(int(row[2]), 0)
        opus = getOpus(int(row[1]))
        label = row[6]
        christophetextpiece = row[5]
        wi = WorkInformation(generalinfo='', relevantmanuscripts='', analysis='', OCVE=christophetextpiece)
        wi.save()
        #Work
        w = Work(label=label, workcollection=wc, workinformation=wi, orderno=99)
        w.save()
        Genre_Work(work=w, genre=g).save()
        #Create Workcomponent
        newWComp = WorkComponent(music=1, label='Music', orderno=1, work=w, keymode=km, keypitch=kp,
                                 opus=opus)
        newWComp.save()
        pieces[int(row[0])] = newWComp
        #Use opusno to find work component for music , create one if it doesn't exist
        #Add workinfo to work information for opus
        #get witnesses for piece
        #tKey = int(row[3])
        #if tKey > 0:
        #    attachTonart(wc, tKey)


def getSourceType(oldKey):
    if oldKey == 1:
        return SourceType.objects.get(id=2)
    elif oldKey == 2:
        return SourceType.objects.get(id=3)
    elif oldKey == 3:
        return SourceType.objects.get(id=1)
    return None


#Generate new page and pageimage from OCVE sources
def importPageImage(sc, witnessKey):
    cursor = connections['ocve_db'].cursor()
    #
    cursor.execute(
        "SELECT p.pageID,p.orderNo,p.startBar,p.endBar,p.sourceWidth,p.sourceHeight,p.page_imageKey,p.filename,p.storageStructure FROM page_image as p,witnesspage_intersection as wp WHERE wp.pageImageKey=p.page_imageKey and wp.witnessKey=" + str(
            witnessKey) + " order by p.orderNo")
    pt = PageType.objects.get(id=3)
    for row in cursor.fetchall():
        p = Page(label=str(row[0]), orderno=int(row[1]), pagetype=pt,
                 sourcecomponent=sc, preferredversion=1)
        p.save()
        pi = PageImage(surrogate=0, versionnumber=1, startbar=str(row[2]), endbar=str(row[3]), permission=1,
                       permissionnote='', width=int(row[4]),
                       height=int(row[5]), page=p)
        pi.save()
        #Page Legacy is for tying images to pages, temporary until full renaming complete
        filename = ''
        if row[7] is not None:
            filename = row[7]
        storageStructure = ''
        if row[8] is not None:
            storageStructure = row[8]
        prefix = 'jp2/ocvejp2-proc/'
        dimensions = verifyImageDimensions(pi, prefix + storageStructure + '.jp2')
        pl = PageLegacy(pageimage=pi, cfeoKey=0, filename=filename, storageStructure=storageStructure,
                        ocveKey=int(row[6]))
        if dimensions == 1:
            pl.jp2 = prefix + storageStructure + '.jp2'
        pl.save()
        importBarRegions(pi, p, row[6])


#todo: Compare OCVe/CFEO publishers
def getPublisher(key):
    cursor = connections['ocve_db'].cursor()
    cursor.execute("SELECT publisherKey,publisherAbbrev,publisherName from publisheral where publisherKey=" + str(key))
    for row in cursor.fetchall():
        abbrev = row[1]
        try:
            p = Publisher.objects.get(publisherAbbrev=abbrev)
            return p
        except ObjectDoesNotExist:
            notfound = 0
    return Publisher.objects.get(id=1)

    #cursor.execute("select "


def addWorkCollection():
    WorkCollection(id=1, label="Unspecified", overridelabel="Unspecified").save()
    WorkCollection(id=2, label="None", overridelabel="None").save()
    WorkCollection(id=3, label="Posthumous", overridelabel="Posthumous").save()


def getDedicatee(ded):
    d = Dedicatee.objects.get(id=2)
    if ded is not None and len(ded) > 1:
        try:
            d = Dedicatee.objects.get(dedicatee=ded)
        except ObjectDoesNotExist:
            d = Dedicatee(dedicatee=ded)
            d.save()
    return d


def getPrintintMethod(pM):
    d = None
    try:
        d = PrintingMethod.objects.get(method=pM)
    except ObjectDoesNotExist:
        d = PrintingMethod(method=pM)
        d.save()
    return d


def convertEntities(chunk):
    entPattern = '(&#(\d+);)'
    entity = ''
    m = re.search(entPattern, chunk, re.IGNORECASE | re.MULTILINE)
    while m is not None:
        entity = m.group(1)
        code = m.group(2)
        newChar = unichr(int(code))
        chunk = chunk.replace(entity, newChar)
        m = re.search(entPattern, chunk, re.IGNORECASE | re.MULTILINE)
    return chunk


def verifySourceComponent(comp, volumeKey, workcomp):
    #Create Source Component
    cursor = connections['ocve_db'].cursor()
    cursor.execute("SELECT textID from volume where volumeKey=" + str(volumeKey))
    #Get volume
    for row in cursor.fetchall():
        #If description not blank
        label = str(row[0])
        if row[0] is not None and label.__len__() > 0:
            if (str(row[0]) == 'Violin 2'):
                stop = 0
            m = re.search("([\w|\&]+)\s*(\d*)", label, re.IGNORECASE | re.MULTILINE)
            if m is not None:
                ins = m.group(1)
                instrument = getInstrument(ins)
                num = 1
                if m.group(2) is not None:
                    inum = str(m.group(2))
                    if inum.__len__() > 0:
                        num = int(m.group(2))
                curIns = None
                #Check instrument against current sc
                try:
                    curIns = Instrument.objects.get(sourcecomponent_instrument__sourcecomponent=comp)
                except ObjectDoesNotExist:
                    curIns = None
                if curIns is None or instrument != curIns or comp.instrumentnumber != num:
                    try:
                        sc = SourceComponent.objects.get(source=comp.source,
                                                         sourcecomponent_workcomponent__workcomponent=workcomp,
                                                         sourcecomponent_instrument__instrument=instrument,
                                                         instrumentnumber=int(num))
                    except ObjectDoesNotExist:
                        #different instrument
                        #create new sc linked to same wc, return
                        #order = SourceComponent.objects.filter(sourcecomponent_workcomponent__workcomponent=workcomp).aggregate(Max('orderno'))
                        #orderno=order['orderno__max']+1
                        orderno = comp.orderno + 1
                        sc = SourceComponent(label=row[0], instrumentnumber=num, orderno=orderno, source=comp.source,
                                             sourcecomponenttype=comp.sourcecomponenttype)
                        sc.save()
                        SourceComponent_WorkComponent(sourcecomponent=sc, workcomponent=workcomp).save()
                        SourceComponent_Instrument(sourcecomponent=sc, instrument=instrument).save()
                    return sc
                else:
                    return comp
        return comp


def importCFEOPages(comp, compKey, editionKey):
    cursor = connections['ocve_db'].cursor()
    global log
    global compHash
    ptm = PageType.objects.get(type='music')
    ptb = PageType.objects.get(type='blank')
    ptt = PageType.objects.get(type='title page')
    cursor.execute("select Page.pageKey,Page.pageID,Page.orderNo,Page.editionKey,Page.volumeKey,Page.notes, " +  #5
                   "PageBars.comVolKey,PageBars.pageKey,PageBars.barRangeDispl,PageBars.startBar,PageBars.startBarExt,PageBars.endBar,PageBars.endBarExt,PageBars.componentKey,PageBars.pageBarsKey,Image.fileName"
                   " from WorkComponent,PageBars,Page,Edition,image WHERE WorkComponent.componentKey=" + str(
        compKey) + " and Edition.editionKey=" + str(editionKey) +
                   " AND WorkComponent.componentKey=PageBars.componentKey and Page.editionKey=Edition.editionKey and PageBars.pageKey=Page.pageKey and image.pageKey=Page.pageKey order by Page.orderNo")
    for row in cursor.fetchall():
        label = convertEntities(row[1])
        notes = str(row[5])
        filename = row[15]
        pt = ptm
        if re.search("score", notes, re.IGNORECASE | re.MULTILINE) is not None:
            pt = ptm
        elif re.search("blank", notes, re.IGNORECASE | re.MULTILINE) is not None:
            pt = ptb
        elif re.search("title", notes, re.IGNORECASE | re.MULTILINE) is not None:
            pt = ptt
            #Check if instruments are involved, and more sourcecomponents need to be created
        workcomps = WorkComponent.objects.filter(sourcecomponent_workcomponent__sourcecomponent=comp)
        if workcomps is not None and workcomps.__len__() > 0:
            workcomp = workcomps[0]
            comp = verifySourceComponent(comp, int(row[4]), workcomp)
        p = Page(label=label, orderno=int(row[2]), sourcecomponent=comp, pagetype=pt)
        p.save()
        startbar = 0
        if row[9] is not None:
            startbar = row[9]
        endbar = 0
        if row[11] is not None:
            endbar = row[11]
        height = 0
        width = 0
        pi = PageImage(page=p, surrogate=0, versionnumber=1, permission=True, permissionnote='', corrected=0,
                       startbar=startbar, endbar=endbar, height=height, width=width)
        pi.save()
        PageLegacy(ocveKey=0, cfeoKey=int(row[0]), filename=filename, storageStructure='', pageimage=pi).save()
        logmsg = " <br/> Page " + label + ":" + str(row[0]) + " uploaded"
        print "\n" + logmsg
        log = log + logmsg
    transaction.commit_unless_managed()


def addAcCode(acCode, si):
    ac = None
    try:
        ac = AcCode.objects.get(accode=acCode)
    except ObjectDoesNotExist:
        ac = AcCode(accode=acCode)
        ac.save()
    si.accode = ac
    si.save()


def safeGet(data):
    if data is not None and str(data) != 'None':
        return data
    else:
        return ""


def importEditions():
    cursor = connections['ocve_db'].cursor()
    #Convert editions to sources
    a = Archive.objects.get(id=1)
    global sourceEditions
    stype = SourceType.objects.get(id=3)
    pianotype = SourceComponentType.objects.get(type__iexact='Piano Score')
    insNone = Instrument.objects.get(id=1)
    cursor.execute(
        "SELECT Edition.editionKey,Edition.publisherKey,Edition.title,Edition.orderNumb,Edition.notes,Edition.platenumber,Edition.placepublication,Edition.datepublication,Edition.locationSimilarCopies,Edition.infoSubsequentReprints,Edition.dedicatee,Edition.printingmethod," +
        "Edition.acOpus,Edition.acSubOpus,Edition.acImpression,Edition.acPublisher,Edition.series,Edition.copyright,Edition.contentsSummary,Edition.copyrightOverride,Edition.shelfmark,Edition.year1,Edition.year2,Edition.contents,Edition.acCode,WorkComponent.workKey " +
        " from WorkComponent,PageBars,Page,Edition WHERE  WorkComponent.componentKey=PageBars.componentKey and Page.editionKey=Edition.editionKey and PageBars.pageKey=Page.pageKey group by Edition.editionKey")
    for row in cursor.fetchall():
        #Split edition information into source/sourceinformation
        label = convertEntities(str(row[2]))
        cfeolabel = convertEntities(str(row[2]))
        s = None
        sc = None
        si = None
        inOCVE = 0
        CFEOkey = int(row[0])
        try:
            #Linked to OCVE source uploaded already
            s = Source.objects.get(sourcelegacy__cfeoKey=CFEOkey)
            s.cfeolabel = cfeolabel
            s.save()
            scType = SourceComponentType.objects.get(type="Piano Score")
            sc = SourceComponent.objects.get(sourcecomponenttype=scType, source=s)
            si = SourceInformation.objects.get(source=s)
            inOCVE = 1
        except ObjectDoesNotExist:
            #New Source
            s = Source(label=label, cfeolabel=cfeolabel, sourcetype=stype)
            s.save()
            sl = SourceLegacy(cfeoKey=CFEOkey, witnessKey=0, source=s, sourceDesc='')
            sl.save()
            #sourceEditions[row[0]] = s
        d = getDedicatee(row[10])
        p = getPublisher(row[1])
        method = getPrintintMethod(row[11])
        plate = safeGet(row[5])
        contents = safeGet(row[23])
        contentssummary = safeGet(row[18])
        if len(contentssummary) > 254:
            contentssummary = contentssummary[0:254]
        shelfmark = safeGet(row[20])
        copyright = safeGet(row[17])
        reprints = safeGet(row[9])
        locationsimilarcopies = safeGet(row[8])
        seriestitle = safeGet(row[16])
        acCode = safeGet(row[24])
        workKey = int(row[25])
        datepublication = ''
        if row[7] is not None and row[7] != 'None':
            datepublication = row[7]
        notes = ''
        if row[4] is not None and row[4] != 'None':
            notes = str(row[4])
        if seriestitle is None:
            seriestitle = ''
        if si is not None:
            #Update existing source information
            si.title = cfeolabel
            si.publisher = p
            #si.archive = a
            si.dedicatee = d
            si.platenumber = plate
            si.locationsimilarcopies = locationsimilarcopies
            si.reprints = reprints
            si.seriestitle = seriestitle
            si.copyright = copyright
            si.contents = contents
            si.leaves = contentssummary
            si.shelfmark = shelfmark
            si.notes = notes
            si.datepublication = datepublication
            if si.keyFeatures is None:
                si.keyFeatures = ""
            if si.additionalInformation is None:
                si.additionalInformation = ''
            if si.sourcecode is None:
                si.sourcecode = ''
            si.save()

        else:
            si = SourceInformation(source=s, publisher=p, archive=a, dedicatee=d, platenumber=plate,
                                   locationsimilarcopies=locationsimilarcopies, reprints=reprints,
                                   seriestitle=seriestitle, title=cfeolabel,
                                   copyright=copyright, contents=contents, leaves=contentssummary,
                                   datepublication=datepublication,
                                   shelfmark=shelfmark, notes=notes, additionalInformation='')
            si.save()
        if acCode is not None:
            addAcCode(acCode, si)
        SourceInformation_PrintingMethod(sourceinformation=si, printingmethod=method).save()
        #Work
        w = None
        if sc is not None:
            #Work already imported, add CFEO orderno
            w = Work.objects.get(workcomponent__sourcecomponent_workcomponent__sourcecomponent=sc)
            w.orderno = getWorkOrder(workKey)
            w.save()
        else:
            w = importCFEOWork(workKey)
            #Get Work components
        importCFEOWorkComponent(s, w, int(row[0]), inOCVE)
        #if sc found above, use its work
        done = 0
        #If music
        #If sc found above, use that
        #todo import music pages?  OCVE overwrite?
        #if actually sourcecomponent, front matter, create and link to source
        #Import Pages

    #Remove any 'orphan' source components, usually caused by multiple instruments
    comps = SourceComponent.objects.all()
    for c in comps:
        pages = Page.objects.filter(sourcecomponent=c)
        if pages is None or pages.__len__() == 0:
            #No pages attached, delete component
            links = SourceComponent_WorkComponent.objects.filter(sourcecomponent=c)
            for l in links:
                l.delete()
            c.delete()


#Get CFEo order number to create unified work order with OCVE
def getWorkOrder(workKey):
    cursor = connections['ocve_db'].cursor()
    cursor.execute("SELECT Work.orderNo from Work where Work.workKey=" + str(workKey))
    orderNo = 99
    for row in cursor.fetchall():
        orderNo = row[0]
    return orderNo


#Another oneoff to re-import CFEO histories missed by old DB
def fixHistory():
    cursor = connections['ocve_db'].cursor()
    cursor.execute(
        "SELECT Work.workKey,Work.title,Work.numbID,Work.opusNo,Work.orderNo,Work.notes,Work.posthumous,Work.history " +
        " FROM work as Work  order by orderNo")
    #308: 0, 310: 0, 317: 0, 318: 0, ,319: 0, 320: 0, 321: 0,65: 0
    workKeyDict = {1: 6338, 2: 6339, 3: 6340, 4: 6341, 6: 6342, 7: 6343, 8: 6344, 9: 6345, 10: 6346, 11: 6347, 12: 6348,
                   13: 6396,
                   14: 6327, 15: 6349, 16: 6350, 17: 6328, 18: 6351, 19: 6352, 20: 6353, 21: 6354, 22: 6355, 23: 6356
        , 24: 6357, 25: 6358, 26: 6329, 27: 6359, 28: 6360, 29: 6361, 30: 6362, 31: 6363, 32: 6364, 33: 6337
        , 34: 6330, 35: 6365, 36: 6366, 37: 6367, 38: 6368, 39: 6369, 40: 6370, 41: 6331, 42: 6371, 43: 6332, 44: 6372
        , 45: 6333, 46: 6373, 47: 6374, 48: 6375, 49: 6334, 50: 6376, 51: 6335, 52: 6377, 53: 6378, 54: 6379, 55: 6380,
                   56: 6381, 57: 6382, 58: 6383, 59: 6336, 60: 6384, 61: 6385, 62: 6386, 63: 6387, 64: 6388, 66: 6389,
                   67: 6390, 68: 6391, 69: 6392, 70: 6393, 71: 6394, 72: 6412, 73: 6395, 74: 6408, 75: 6418, 77: 6406,
                   78: 6414, 79: 6409, 80: 6419, 81: 6411, 82: 6420, 83: 6413, 84: 6421, 85: 6422, 303: 6410, 304: 6415,
                   312: 6392, 316: 6407}
    for row in cursor.fetchall():
        try:
            opusNo = int(row[2])
            label = convertEntities(row[1])
            orderno = int(row[4])
            if row[3] is not None and len(row[3]) > 0 and row[3] is not '0':
                label = label + " Op. " + row[3]
            work = Work.objects.get(id=workKeyDict[row[0]])
            #workKeyDict[row[0]]=int(work.id)
            history = row[7]
            if history != "None":
                [relevant, analysis, generalinfo] = parseHistory(history)
                if work.workinformation.id == 6338 and work.id != 6327:
                    wi = WorkInformation()
                else:
                    wi = WorkInformation.objects.get(work=work)
                wi.generalinfo = generalinfo
                wi.relevantmanuscripts = relevant
                wi.analysis = analysis
                wi.save()
                if work.workinformation.id == 6338 and work.id != 6327:
                    work.workinformation = wi
                    work.save()
        except ObjectDoesNotExist:
            label = convertEntities(row[1])
            #workKeyDict[row[0]]=0
        except KeyError:
            len(workKeyDict)


def parseHistory(history):
    generalPattern = "<p>General introduction.*?</p>"
    relevantPattern = "<p>Manuscripts relevant.*?</p>"
    analysisPattern = "<p>Analysis of printed sources.*?</p>"
    relevant = ''
    analysis = ''
    generalinfo = ''
    #Split history into sections
    if re.search(relevantPattern, history, re.IGNORECASE | re.MULTILINE) is not None:
        m = re.search(generalPattern + "(.*?)" + relevantPattern + "(.*)", history, re.IGNORECASE | re.MULTILINE)
        if m is not None:
            generalinfo = m.group(1)
            if m.group(2) is not None:
                relevant = m.group(2)
                m = re.search("(.*)" + analysisPattern + "(.*)", relevant, re.IGNORECASE | re.MULTILINE)
                if m is not None:
                    relevant = m.group(1)
                    if m.group(2) is not None:
                        analysis = m.group(2)
    elif len(history) > 1 and history != 'None':
        m = re.search(generalPattern + "(.*)", history, re.IGNORECASE | re.MULTILINE)
        generalinfo = m.group(1)
    return [relevant, analysis, generalinfo]


#Import standard CFEO works, ignoring posthumous and special cases
#<p>General introduction</p><p>Not only are Chopin's mazurkas his most original compositions, but they are also the most abundant of any genre in his output, amounting to fifty-eight works in total. Two of them &#150; in G major and B-flat major &#150; were published in Warsaw before he left his native Poland. The other mazurkas that appeared during his lifetime include Opp. 6, 7, 17, 24, 30, 33, 41, 50, 56, 59 and 63, the Mazurka dedicated to Emile Gaillard, and the Mazurka from La France Musicale, while Opp. 68 and 69 were brought out in the posthumous edition prepared by Julian Fontana in 1855. The first editions of the mazurkas inscribed by Chopin in the albums of Vaclav Hanka, Alexandrine Wo&#322;owska and Maria Szymanowska appeared in 1879, 1909 and 1930 respectively. The authenticity of the Mazurka in C major (published by Kaufmann in 1869) and D major (Leitgeber, 1875) is doubtful, while the Mazurka in F-sharp minor &#150; formerly attributed to Chopin &#150; has been identified as the work of Charles Mayer. </p><p>In these compositions inspired by Polish folklore, Chopin masterfully achieves both an artistic synthesis of three dances &#150; mazur, kujawiak and oberek &#150; and a rich and varied expressive palette ranging from innocent joy to profound feelings of nostalgia, despair and the celebrated '&#380;al'. These darker emotions are conveyed with particular potency in the Mazurka in E minor Op. 41 No. 1.</p><p>Manuscripts relevant to published editions: Autograph, serving as <em>Stichvorlage</em> for <strong>G</strong>: PL-Wn: Mus. 221. Copy by Fontana, serving as <em>Stichvorlage</em> for <strong>F</strong>: Lvov: Historical Museum (Op. 33 No. 1); Tokyo, private collection (Op. 33 No. 2); Torino, Radio (Op. 33 No. 3); US-Wc (Op. 33 No. 4).</p><p>Analysis of printed sources and the publication process</p><p>The layouts of <strong>F</strong> and <strong>G</strong> have very little in common, and those few similarities that do exist are entirely coincidental (e.g. Mazurka in C major: systems 1, 2, 5, 6; Mazurka in D major: p. 6 system 5, p. 7 system 1&#150;3; Mazurka in B minor: p. 10/11 system 1). In <strong>G</strong>, the Mazurka in C major is placed after the Mazurka in D major &#150; an initiative of the publisher rather than the composer since a different ordering of these works is found in the Stichvorlage and indeed the other two first editions. Considerable differences also exist between the layouts of <strong>F</strong> and <strong>E</strong>, despite which certain commonalities may also be observed: systems 3&#150;6 on p. 4; systems 4 & 5 on p. 5; systems 1 & 2 on p. 6; systems 2 & 5 on p. 8; pp. 9 & 16 in toto; final system on pp. 11 & 13. The engraver of <strong>E</strong> also chose to distribute the text more spaciously, with as many as six systems on pp. 3&#150;5, 10&#150;13 & 15, whereas in <strong>F</strong> six systems appear only on pp. 4 & 5. Notwithstanding the various differences, it is certain that <strong>E</strong> was based on <strong>F</strong>, in view of the numerous similarities. As for <strong>G</strong>, it seems to have been based on an autograph post-dating the one used to prepare <strong>F</strong>. </p><p>The copy of <strong>F</strong> reproduced in CFEO was produced by means of lithographic transfer for distribution as a supplement to the <em>Revue et Gazette musicale de Paris</em> before the engraved version was released. As a result of this production method, the score contains numerous errors: for example, the rhythmic value of LH note 3 in the final bar of Op. 33 No. 2 is transformed into a minim, similarly that of LH note 2 and the lowest note in LH chord 3 of the final bar of Op. 3 No. 4. The plate number on p. 6 (i.e. within Op. 33 No. 3) is also missing for this reason. <strong>F</strong> contains many other flaws which escaped Chopin's attention while correcting the proofs. Some of these originated with the engraver, for example the following: </p><ul><li>Op. 33 No. 1: tempo indication misinterpreted ('Presto' instead of 'Mesto')</li><li>Op. 33 No. 3: ties added over barline to lowest notes of LH chords at bs 8&#150;9, 24&#150;25 et seq.; essential ledger lines missing to LH note 1 in bs 20 & 80 and to a-flat<sup>2</sup> in RH chord 3 in b. 60; double flats before LH note 4 in b. 63 replaced by single flat</li><li>Op. 33 No. 4: sharp added to LH notes 3 & 4 in b. 63 (and by extension in b. 103).</li></ul><p>Numerous essential accidentals are also missing from <strong>F</strong> (as they are in the <em>Stichvorlage</em> used by the French publisher): </p><ul><li>Op. 33 No. 1: sharp to a1 in RH chord 3 b. 5; sharp to a in LH chord 2 bs 27, 33 & 35 </li><li>Op. 33 No. 2: flat to d(-natural)1 in RH chord 3 b. 26</li><li>Op. 33 No. 4: natural to RH note 4 bs 19, 43, 83, 107 & 211; flat to LH note 3 bs 62 & 64.</li></ul><p>The accidentals missing in Fontana's copy and in <strong>F</strong> are also missing in the autograph used to prepare <strong>G</strong>, but they were all restored by the proofreader in Leipzig. Oddly enough, <strong>G</strong> makes two erroneous corrections in the Mazurka in D major which are also found in <strong>F</strong>: i.e. a tie is added over the barline between the lowest notes of the LH chords in bs 8&#150;9 & 24&#150;25 <em>et seq</em>., and the double flats to LH note 4 in b. 63 are replaced by a single flat. As there is no evidence that Chopin had any role in the preparation of <strong>G</strong>, these correspondences are surely coincidental. Moreover, a few bars earlier at b. 54, the flat sign to LH note 4 is also missing from <strong>G</strong>. </p><p>Certain corrections can nevertheless be found in <strong>G</strong> which do not appear in <strong>F</strong> and which were entered by the composer on the <em>Stichvorlage</em> dispatched to Leipzig (see LH in bs 29&#150;30, 34&#150;36 of Op. 33 No. 1). <strong>G</strong> also contains the original version with mordents of RH note 1 in bs 11, 35, 79 & 203 of Op. 33 No. 4, which Chopin eliminated when correcting <strong>F</strong>. </p><p>Changes unique to <strong>G</strong> include the following : </p><ul><li>Op. 33 No. 1: rest added to middle LH voice on beat 1 of b. 2</li><li>Op. 33 No. 2 (i.e. Mazurka in D major): most staccato dots omitted, except for bs 62&#150;64 (RH chord 1) and b. 134 (RH notes 1&#150;6)</li><li>Op. 33 No. 3 (i.e. Mazurka in C major): sharp added to f1 in RH chord 1 b. 13.</li></ul><p><strong>E</strong> reproduces <strong>F</strong>'s text but with numerous modifications. It corrects all of the errors in <strong>F</strong> caused by lithographic transfer, then restores the accidentals missing from its <em>Stichvorlage</em> apart from the one in b. 26 of Op. 33 No. 2. It also does not restore the double flat sign to LH note 4 in b. 63 of Op. 33 No. 3. In b. 8 of Op. 33 No. 2, <strong>E</strong> separates RH chord 3 into two voices and then introduces the indication 'Dolce' in bs 16&#150;17. It also restores the copious LH staccato dots (e.g. LH note 1 in bs 7&#150;9, 15, 16, 19&#150;21), as well as the dynamic indications '<strong><em>f</strong></em>' in b. 73 and '<strong><em>pp</strong></em>' in b. 97 of Op. 33 No. 3. The English proofreader apparently considered the lowest note of RH chords 1 & 2 in b. 56 of Op. 33 No. 3 (b(-flat)<sup>1</sup> in <strong>F</strong>) to be incorrect; changing it to a<sup>1</sup> reestablished the symmetry while restoring the text to the version found in Chopin's manuscript and Fontana's copy. <strong>E</strong> also adds accidentals whose omission was obvious (e.g. Op. 33 No. 3: flat to d<sup>3</sup> in RH chord 4 b. 60; flat to LH note 4 b. 64), and it changes the notation of the appoggiaturas into semiquavers (e.g. Op. 33 No. 1: bs 6, 10 RH note 1).</p><p>The later evolution of the first editions can be inferred from the 'Information on subsequent reprints'. The <em>Annotated Catalogue</em> provides full details of these sources and where they are located.</p><p></p></p>
def importCFEOWork(workKey):
    cursor = connections['ocve_db'].cursor()
    global worksHash
    cursor.execute(
        "SELECT Work.workKey,Work.title,Work.numbID,Work.opusNo,Work.orderNo,Work.notes,Work.posthumous,Work.history " +
        " FROM Work where Work.workKey=" + str(workKey) + " order by orderNo")

    wc = WorkCollection.objects.get(label__iexact='None')
    for row in cursor.fetchall():
        km = keyMode.objects.get(id=2)
        kp = keyPitch.objects.get(id=2)
        label = convertEntities(row[1])
        orderno = int(row[4])
        if row[3] is not None:
            label = label + " Op. " + row[3]
        history = str(row[7])
        [relevant, analysis, generalinfo] = parseHistory(history)
        opusNo = int(row[2])
        w = None
        try:
            #work added by ocve, update
            w = Work.objects.filter(workcomponent__opus__opusno=opusNo)[0]
            w.orderno = orderno
            w.save()
            if history != "None":
                wi = WorkInformation.objects.get(work=w)
                wi.generalinfo = generalinfo
                wi.relevantmanuscripts = relevant
                wi.analysis = analysis
                wi.OCVE = ''
                wi.save()
        except IndexError:
            #new work
            if history != "None":
                wi = WorkInformation(generalinfo=generalinfo, relevantmanuscripts=relevant, analysis=analysis, OCVE='')
                wi.save()
                #Work
            else:
                wi = WorkInformation(generalinfo='', relevantmanuscripts='', analysis='', OCVE='')
                wi.save()
            w = Work(label=label, workcollection=wc, workinformation=wi, orderno=orderno)
            w.save()
            #Genres
            cursor.execute(
                "SELECT workKey,genreKey from genrework where workKey=" + str(workKey) + "")
            for row in cursor.fetchall():
                g = lookupGenre(row[1], 1)
                if w is not None and g is not None:
                    Genre_Work(work=w, genre=g).save()
    return w


def importCFEOWorkComponent(source, work, editionKey, inOCVE):
    cursor = connections['ocve_db'].cursor()
    global worksHash
    global sourceEditions
    global compHash
    global CFEOSourceComponents
    w = work
    s = source
    #Order manually set to allow creation of new components i.e. instruments
    orderno = 100
    cursor.execute(
        "SELECT wc.componentKey,wc.componentTitle,wc.componentTypeKey,wc.sequenceNo,wc.componentName,wc.genreKey,wc.orderNo,wc.workKey,w.numbID,w.numbID,p.editionKey " +
        " FROM ocve3.workcomponent as wc,PageBars as pb,Page as p,ocve3.work as w where p.editionKey=" + str(
            editionKey) + " and w.workKey=wc.workKey " +
        "   and wc.componentKey=pb.componentKey and pb.pageKey=p.pageKey group by wc.componentKey order by wc.componentKey")
    for row in cursor.fetchall():
        #vtext=str(row[11])
        #if vtext is not None and vtext!='NONE':
        #Parse text for instruments
        #    pass
        opusNo = int(row[9])
        o = getOpus(opusNo)
        type = int(row[2])
        music = 1
        if type > 5 and type < 11:
            music = 0
        km = keyMode.objects.get(id=2)
        kp = keyPitch.objects.get(id=2)
        label = convertEntities(str(row[4]))
        if label is None or label == 'None':
            label = 'Score'
        if int(row[10]) == 231:
            stop = 0
        newSComp = None
        if music == 1:
            #Only do if no OCVE data, latter takes precedence
            if inOCVE == 0:
                #Have we already made this workcomponent?
                newWComp = None
                try:
                    newWComp = WorkComponent.objects.get(label=label, work=work)
                except ObjectDoesNotExist:
                    #Create Workcomponent
                    newWComp = WorkComponent(music=music, label=label, orderno=int(row[6]), work=w, keymode=km,
                                             keypitch=kp,
                                             opus=o)
                    newWComp.save()
                    #compHash[str(row[0])] = newWComp

                scType = SourceComponentType.objects.get(type="Piano Score")
                newSComp = SourceComponent(source=s, orderno=orderno, label=label, sourcecomponenttype=scType,
                                           overridelabel=label, instrumentnumber=1)
                newSComp.save()
                #Hashed with old WorkComponent it mirrors so we can link to pages
                #CFEOSourceComponents[str(row[0])] = newSComp
                #Link source and work
                SourceComponent_WorkComponent(sourcecomponent=newSComp, workcomponent=newWComp).save()
                #Import pages linked to component
                importCFEOPages(newSComp, int(row[0]), editionKey)
        else:
            #This is actually a source component like front matter
            scType = SourceComponentType.objects.get(type="Manuscript")
            newSComp = SourceComponent(source=s, orderno=int(row[6]), label=label, sourcecomponenttype=scType,
                                       overridelabel=label, instrumentnumber=1)
            newSComp.save()
            #Hashed with old WorkComponent it mirrors so we can link to pages
            CFEOSourceComponents[str(row[0])] = newSComp
            #Import pages linked to component
            importCFEOPages(newSComp, int(row[0]), editionKey)
        orderno = orderno + 100


def getInstrument(label):
    d = None
    try:
        d = Instrument.objects.get(instrument=label)
    except ObjectDoesNotExist:
        d = Instrument(instrument=label, instrumentabbrev='')
        d.save()
    return d


#A special case for the Posthumous that need to be re-worked for new structure
def importPosthumous():
    cursor = connections['ocve_db'].cursor()
    #Posthumous work collection
    wc = WorkCollection.objects.get(id=3)


    #Stores old/new component keys for proper linking
    compHash = {}
    importEditions()
    cursor.execute("SELECT history from Work where workKey=65")
    f = cursor.fetchone()
    history = str(f[0])

    cursor.execute(
        "SELECT componentKey,componentTypeKey,sequenceNo,componentName,genreKey,orderNo FROM ocve3.workcomponent w where workKey=65 order by orderNo")
    for row in cursor.fetchall():
        #None for front Matter
        o = Opus.objects.get(id=1)
        g = Genre.objects.get(id=2)
        km = keyMode.objects.get(id=2)
        kp = keyPitch.objects.get(id=2)
        label = str(row[3])
        if int(row[4]) > 1:
            g = lookupGenre(int(row[4]), 1)
        if int(row[2]) > 0:
            #todo Work information separate or together?
            wi = WorkInformation(generalinfo=history, relevantmanuscripts='', analysis='')
            wi.save()
            #Work
            #todo Complete?
            w = Work(label=label, workcollection=wc, workinformation=wi)
            w.save()
            Genre_Work(work=w, genre=g).save()
            o = getOpus(int(row[2]))
            #Create Workcomponent
            newWComp = WorkComponent(music=1, label=label, orderno=int(row[5]), work=w, keymode=km, keypitch=kp, opus=o)
            newWComp.save()
            compHash[str(row[0])] = newWComp.id
        else:
            #Text matter Only
            pass
    pass


def getOpus(opusNo):
    o = None
    try:
        o = Opus.objects.get(opusno=int(opusNo))
    except ObjectDoesNotExist:
        o = Opus(opusno=int(opusNo))
        o.save()
    return o


def addLog(line):
    global log
    log = log + "" + line


def handle_uploaded_file(f, fname):
    destination = open(settings.IMAGE_UPLOAD_PATH + fname, 'wb')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def correctYear():
    infos = SourceInformation.objects.all()
    for si in infos:
        date = si.datepublication
        m = re.search('(18[0-9]+)', date)
        if m is not None:
            year = m.group(1)
            try:
                y = Year.objects.get(year=year)
            except ObjectDoesNotExist:
                y = Year(year=year)
                y.save()
            SourceInformation_Year(sourceinformation=si, year=y).save()


def renameimages(request):
    log = ''
    #Get all sources
    #For each source
    #Create folder with source id
    #Get all page image records for source
    #Get image path
    #copy jp2 to new location with pi key filename
    #Print manifest
    return HttpResponse(log)


def findmeta(request):
    cursor = connections['ocve_db'].cursor()
    cursor.execute(
        "SELECT si.source_id,sl.sourceDesc,sl.cfeoKey,sl.witnessKey FROM ocve2real.ocve_sourceinformation as si,ocve2real.ocve_sourcelegacy as sl where si.source_id=sl.source_id and (si.datepublication='' or si.placepublication_id=1 or si.displayedcopy='')")
    for row in cursor.fetchall():
        info = SourceInformation.objects.filter(source_id=int(row[0]))
        cfeoKey = int(row[2])
        witnessKey = int(row[3])
        if info.count() > 0:
            si = info[0]
            sourceDesc = row[1]
            if len(si.displayedcopy) < 1:
                if witnessKey > 0:
                    displayMatch = re.search("<label>Displayed copy</label>\s*<value>(.*?)</value>", sourceDesc,
                                             re.IGNORECASE | re.MULTILINE)
                    if displayMatch is not None:
                        display = displayMatch.group(1)
                        if len(display) > 0:
                            si.displayedcopy = display
                            si.save()
                elif cfeoKey > 0:
                    cursor2 = connections['ocve_db'].cursor()
                    cursor2.execute("SELECT shelfmark FROM ocve2real.edition where editionKey=" + str(cfeoKey))
                    for row2 in cursor2.fetchall():
                        si.displayedcopy = str(row2[0])
                        si.save()
            displayMatch = re.search("<label>Publication date</label>\s*<value>(.*?)</value>", sourceDesc,
                                     re.IGNORECASE | re.MULTILINE)
            if len(si.datepublication) < 1:
                if displayMatch is not None:
                    display = displayMatch.group(1)
                    if len(display) > 0:
                        si.datepublication = display
                        si.save()
            if si.placepublication_id < 2:
                if cfeoKey > 0:
                    cursor2 = connections['ocve_db'].cursor()
                    cursor2.execute("SELECT placepublication FROM ocve2real.edition where editionKey=" + str(cfeoKey))
                    for row2 in cursor2.fetchall():
                        city = str(row2[0])
                    try:
                        c = City.objects.get(city=city)
                    except ObjectDoesNotExist:
                        c = City(city=city)
                        c.save()
                    si.placepublication = c
                    si.save()


def correctSourceInformation(request):
    cursor = connections['ocve_db'].cursor()
    infos = SourceInformation.objects.filter(source__sourcelegacy__witnessKey__gt=0)
    #todo: ChristopheTextWitness,Witness.notes,Witness.designation,Witness.designationSuperscript, removed for now due to unicode errors
    emptyDedicatee = Dedicatee.objects.get(id=1)
    emptyPublisher = Publisher.objects.get(id=1)
    emptyArchive = Archive.objects.get(id=1)
    emptyCity = City.objects.get(id=1)
    for si in infos:
        witnessKey = SourceLegacy.objects.get(source_id=si.source_id).witnessKey
        s = si.source
        cursor.execute(
            "SELECT Witness.witnessKey,Witness.pieceKey,Witness.sourceKey,Witness.CFEOeditionKey,Witness.witnessDescription,Witness.publisherAbbrev,Witness.full_text_c FROM witness as Witness where Witness.witnessKey=" + str(
                witnessKey))
        for row in cursor.fetchall():
            #Create new source
            st = getSourceType(row[2])
            #witnessKey = int(row[0])
            publisherAbbrev = row[5]
            sourceDesc = row[6]

            if len(si.displayedcopy) < 1:
                displayMatch = re.search("<label>Displayed copy</label>\s*<value>(.*?)</value>", sourceDesc,
                                         re.IGNORECASE | re.MULTILINE)
                if displayMatch is not None:
                    display = displayMatch.group(1)
                    if len(display) > 0:
                        si.displayedcopy = display
                        si.save()

    return HttpResponse(log)



    # class Command(NoArgsCommand):
    #     help = """Normalizes UNICODE data in text fields, it replaces combining
    #     character with UNICODE character."""
    #
    #     def handle_noargs(self, **options):
    #         norm = 'NFKC'
    #
    #         for l in Library.objects.all():
    #             l.name = _n(norm, l.name)
    #             l.save()
    #
    #         for p in Publisher.objects.all():
    #             if p.name:
    #                 p.name = _n(norm, p.name)
    #                 p.save()
    #
    #         for s in STP.objects.all():
    #             s.publisher_name = _n(norm, s.publisher_name)
    #             s.rubric = _n(norm, s.rubric)
    #             s.save()
    #
    #         for a in Advert.objects.all():
    #             a.publisher_name = _n(norm, a.publisher_name)
    #             a.rubric = _n(norm, a.rubric)
    #             a.save()