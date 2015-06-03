__author__ = 'Elliot'
 # coding=utf8

#Views for the user interface
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bartools import *
from uitools import *
from dbmi.spine import getSpinesByWork,spinesToRegionThumbs
from dbmi.sourceeditor import cleanHTML,cleanSourceInformationHTML

#Takes pageimageid
from models import keyPitch
from models_generic import BarCollection
import json
import hashlib
from django.db import connection, connections, transaction
from forms import AnnotationForm
import os
from dbmi.datatools import convertEntities
from imagetools import verifyImageDimensions

#IIP_URL = settings.IIP_URL
IMAGE_SERVER_URL = settings.IMAGE_SERVER_URL


def cfeoacview(request,acHash,mode="OCVE"):
    return acview(request,acHash,'CFEO')

#Takes a passed hashed accode from annotated catalogue and displays the source in browse
def acview(request,acHash,mode="OCVE"):
    filters = []

    try:
        ac = AcCode.objects.get(accode_hash=acHash)

        if ac:
            sources = Source.objects.filter(
                sourceinformation__accode=ac).filter(Q(ocve=1) | Q(cfeo=1))

            if sources and sources.count() > 0:
                source = sources[0]
                work = source.getWork()

                if work:
                    filters.append({'type': 'Work', 'id': work.id,
                                    'selection': work.label})
                    filters.append({'type': 'Source', 'id':source.id,
                                    'selection': source})
    except ObjectDoesNotExist:
        pass

    return browse(request, mode, filters)


def shelfmarkview(request,acHash,mode="OCVE"):
     #shelfmark=hashlib.md5(acHash).hexdigest()
     #sources=Source.objects.filter(sourceinformation__shelfmark__exact=shelfmark)
     filters=[]
     foundMark=""
     filterString=""
     for si in SourceInformation.objects.all():
        if hashlib.md5(si.shelfmark.encode('UTF-8')).hexdigest() == str(acHash):
            foundMark=si.shelfmark
            work=si.source.getWork()
            filters.append({'type':'Work','id':work.id,'selection':work.label})
            filters.append({'type':'Source','id':si.source.id,'selection':si.source})
            filterString+='<br>{type:Work,id:'+str(work.id)+',selection:'+work.label+' type:Source,mark:'+si.shelfmark+',id:'+str(si.source.id)+',selection:'+si.source.label+',type:'+si.source.sourcetype.type+'}\n'
     return HttpResponse(u'shelfmark found as:'+foundMark+"<br><br> Filters:"+filterString)
     #return browse(request,mode,filters)


def cfeoBrowse(request):
    return browse(request,"CFEO")


@csrf_exempt
def serializeFilter(request):
    try:
        filters=request.POST['OCVE_current_filters']
        request.session['OCVE_current_filters'] = filters
    except MultiValueDictKeyError:
        pass
    except KeyError:
        pass
    try:
        filters=request.POST['CFEO_current_filters']
        request.session['CFEO_current_filters'] = filters
    except MultiValueDictKeyError:
        pass
    except KeyError:
        pass
    return HttpResponse()


def resetFilter(request):
    try:
        del request.session['OCVE_current_filters']
        del request.session['CFEO_current_filters']
    except MultiValueDictKeyError:
        pass
    except KeyError:
        pass
    return HttpResponse()

def cleanXML(xml):
    xml=xml.replace('<para>','<p>').replace('</para>','</p>')
    return xml

def fixsourceinformation(request):
    cursor = connections['ocve_db'].cursor()
    #sql='select sl.source_id,si.id,sl.sourceDesc,sl.witnessKey from ocve_source as s,ocve_sourceinformation as si,ocve_sourcelegacy as sl where (s.ocve=1 or s.cfeo=1) and s.id=sl.source_id and s.id=si.source_id'
    sql='select sl.source_id,si.id,sl.sourceDesc,sl.witnessKey,E.locationSimilarCopies,E.printingmethod from ocve_source as s,ocve_sourceinformation as si,ocve_sourcelegacy as sl,edition as E where (s.ocve=1 or s.cfeo=1) and E.editionKey=sl.cfeoKey and s.id=sl.source_id and s.id=si.source_id'
    sql+=' and length(si.locationsimilarcopies) = 0'
    cursor.execute(sql)
    log=""
    for row in cursor.fetchall():
        s=Source.objects.get(id=int(row[0]))
        si=SourceInformation.objects.get(id=int(row[1]))
        sourceDesc=str(row[2])
        similarcopies=str(row[4])
        printingmethod=str(row[5])
        if len(si.locationsimilarcopies) == 0 :
            si.locationsimilarcopies=similarcopies

        if PrintingMethod.objects.filter(sourceinformation=si).count == 0:
            methods=PrintingMethod.objects.filter(method=printingmethod)
            if methods.count() > 0:
                pm=methods[0]
            SourceInformation_PrintingMethod(sourceinformation=si,printingmethod=pm).save()

        sourceDesc = convertEntities(sourceDesc)
        publicationTitleMatch = re.search("<label>.*title[\:]*</label>\s*<value>(.*?)</value>", sourceDesc,
                                      re.IGNORECASE | re.MULTILINE)
        if publicationTitleMatch is not None:
            pubtitle = publicationTitleMatch.group(1)
            if len(si.title) ==0:
                si.title=pubtitle
        else:
            log+='\nNo title parsed for '+str(row[1])
        match= re.search("<label>.*Source of images[\:]*\s*</label>\s*<value>(.*?)</value>", sourceDesc,re.IGNORECASE | re.MULTILINE)
        if match is not None:
            imagesource = match.group(1)
            if len(si.imagesource) == 0:
                si.imagesource=imagesource
        else:
            log+='\nNo imagesource parsed for '+str(row[1])
        match= re.search("<component id=\"keyFeatures\">\s*<heading>Key features:</heading>\s*(.*?)</component>", sourceDesc, re.IGNORECASE | re.MULTILINE)
        if match is not None:
            keyFeatures = match.group(1)
            keyFeatures=cleanXML(keyFeatures)
            if len(si.keyFeatures) == 0:
                si.keyFeatures=keyFeatures
        else:
            log+='\nNo imagesource parsed for '+str(row[1])

        if len(s.cfeolabel) != 0:
            si.publicationtitle=s.cfeolabel
        si.save()
    return HttpResponse(log)



def browse(request,mode="OCVE",defaultFilters=None):
    #component_workcomponent__workcomponent__work_id=6355
    comps=SourceComponent.objects.filter(source_id=18036)
    piano=Instrument.objects.get(instrument="Piano")
    for c in comps:
        sourceomponentinstruments=SourceComponent_Instrument.objects.filter(sourcecomponent=c)
        if sourceomponentinstruments.count() == 0:
            SourceComponent_Instrument(sourcecomponent=c,instrument=piano).save()
        #for sci in sourceomponentinstruments:
        #    sci.instrument=piano
        #    sci.save()

    #Filter Items
    for si in SourceInformation.objects.filter(contentssummary__startswith='<p></p>'):
        si.contentssummary=si.contentssummary.replace('<p></p>','')
        si.save()
    try:
        if defaultFilters is None and request.session[mode+'_current_filters']:
            filterJSON=request.session[mode+'_current_filters']
            defaultFilters=json.loads(filterJSON, encoding='utf-8')
    except KeyError:
        pass
        #defaultFilters = ''u' Bodleian Library, Oxford'
    sourceTypes=SourceType.objects.all()
    workinfos=[]
    if mode == 'OCVE':
        works=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__ocve=True).distinct()
        if works.count() > 0:
            for w in works:
                if len(w.workinformation.OCVE)> 0:
                    workinfos.append(w.id)
        #dedicatees=Dedicatee.objects.filter(sourceinformation__source__ocve=True).filter(id__gt=2).distinct()
        publishers=Publisher.objects.filter(sourceinformation__source__ocve=True).filter(id__gt=2).distinct()
        years=Year.objects.filter(sourceinformation__source__ocve=True).distinct()
        keyPitches=keyPitch.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__ocve=True).distinct()
        genres=Genre.objects.filter(work__workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__ocve=True).filter(id__gt=2).distinct()
        instruments=Instrument.objects.filter(sourcecomponent_instrument__sourcecomponent__source__ocve=True).distinct()
    else:
        works=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__cfeo=True).distinct()
        if works.count() > 0:
            for w in works:
                if len(w.workinformation.analysis)> 0 or len(w.workinformation.generalinfo)> 0 or len(w.workinformation.relevantmanuscripts)> 0:
                    workinfos.append(w.id)
        #dedicatees=Dedicatee.objects.filter(sourceinformation__source__cfeo=True).distinct()
        publishers=Publisher.objects.filter(sourceinformation__source__cfeo=True).distinct()
        years=Year.objects.filter(sourceinformation__source__cfeo=True).distinct()
        genres=Genre.objects.filter(work__workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__cfeo=True).distinct()
        instruments=Instrument.objects.filter(sourcecomponent_instrument__sourcecomponent__source__cfeo=True).distinct()
    return render_to_response('frontend/browse.html', {'defaultFilters':defaultFilters, 'mode':mode,'workinfos':workinfos,'sourceTypes':sourceTypes,'instruments':instruments,'years':years,'publishers':publishers,'genres':genres,'works':works, 'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL}, context_instance=RequestContext(request))


#Optimised for OCVE
def sourcejs(request):
    #for s in Source.objects.filter(Q(ocve=1)|Q(cfeo=1)):
    #    overwritesourcecomponentlabels(s)
    #    setPageImageTextLabel(s)
    serializeOCVESourceJson()
    serializeCFEOSourceJson()
    serializeAcCodeConnector()
    return HttpResponse("<html><head><title>UI JSONs rebuilt</title></head><body><a href='/ocve/dbmi/'>Return to DBMI</a></body></html>")

def getNextPrevPages(p,pi):
    next=None
    prev=None
    norder=p.orderno+1
    porder=p.orderno-1
    npi=PageImage.objects.filter(page__sourcecomponent__source=p.sourcecomponent.source,page__pagetype_id=3,page__orderno=norder)
    if npi.count() > 0:
        next=npi[0]
    if porder > 0:
        ppi=PageImage.objects.filter(page__sourcecomponent__source=p.sourcecomponent.source,page__pagetype_id=3,page__orderno=porder)
        if ppi.count() > 0:
            prev=ppi[0]
    return [next,prev]

#Get relevant work for a pageimage object
def getPageImageWork(pi,source):
    work=None
    works = Work.objects.filter(
        workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()
    if works.count() ==0:
        #This is Front Matter, use the work from the whole source
        works = Work.objects.filter(
        workcomponent__sourcecomponent_workcomponent__sourcecomponent__source=source).distinct()
    if works.count() >0:
        work=works[0]
    return work

#Annotation.objects.filter(type_id=1).delete()
@csrf_exempt
def ocvePageImageview(request, id):
    mode = "OCVE"
    noteURL = "/ocve/getAnnotationRegions/" + id + "/"
    regionURL = "/ocve/getBarRegions/" + id + "/"

    view = request.GET.get('view')

    pi = PageImage.objects.get(id=id)
    p = pi.page

    newN = Annotation(pageimage=pi)
    if request.user is not None and request.user.id is not None:
        newN.user=request.user
    annotationForm = AnnotationForm(instance=newN)

    source = pi.page.sourcecomponent.source

    accode = source.getAcCodeObject()
    achash = None

    if accode:
        achash = accode.accode_hash

    pageimages = getOCVEPageImages(source)

    cursor = connections['ocve_db'].cursor()
    cursor.execute(
        """select bar.barlabel, pi.id from ocve_bar as bar,
        ocve_bar_barregion as brr, ocve_barregion as barregion,
        ocve_pageimage as pi, ocve_page as p, ocve_sourcecomponent as sc
        where bar.id=brr.bar_id and brr.barregion_id=barregion.id
        and barregion.pageimage_id=pi.id and pi.page_id=p.id
        and p.sourcecomponent_id=sc.id
        and sc.source_id=""" + str(source.id) + " order by bar.barnumber")

    notes = Annotation.objects.filter(pageimage_id=id, type_id=1)
    comments = Annotation.objects.filter(pageimage_id=id, type_id=2)
    [next_page, prev_page] = getNextPrevPages(p, pi)
    work=getPageImageWork(pi,source)
    zoomifyURL = pi.getZoomifyPath()

    request.session['page_image'] = id

    return render_to_response('frontend/pageview.html', {
        'achash': achash, 'annotationForm': annotationForm, 'notes': notes,
        'comments': comments, 'allBars': cursor, 'work': work,
        'source': source, 'prev': prev_page, 'next': next_page,
        'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL,
        'pageimages': pageimages, 'mode': mode, 'zoomifyURL': zoomifyURL,
        'regionURL': regionURL, 'noteURL': noteURL, 'page': p,
        'pageimage': pi, 'view': view},
        context_instance=RequestContext(request))


def addImageDimensions(pi):
    pl = PageLegacy.objects.get(pageimage=pi)
    path=pl.jp2
    if str(path).startswith("jp2")is False:
        path="jp2/"+path
    verifyImageDimensions(pi, path)

def ocveViewInPage(request,id,barid):
    regionURL = "/ocve/getBarRegions/" + id + "/" + barid + "/"
    pi=PageImage.objects.get(id=id)
    if pi.width == 0:
        addImageDimensions(pi)
    p=pi.page
    source=pi.page.sourcecomponent.source
    pageimages=PageImage.objects.filter(page__sourcecomponent__source=pi.page.sourcecomponent.source,page__pagetype_id=3).order_by("page")
    opus=Opus.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()
    work=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()[0]
    zoomifyURL=pi.getZoomifyPath()
    mode="OCVE"
    return render_to_response('frontend/viewinpage.html', {'work':work,'source':source,'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL,'pageimages':pageimages,'mode':mode,'opus':opus,'zoomifyURL':zoomifyURL,'regionURL':regionURL,'page': p, 'pageimage': pi}, context_instance=RequestContext(request))

def cfeoPageImageview(request,id):
    mode="CFEO"
    pi=PageImage.objects.get(id=id)
    p=pi.page
    if pi.width == 0:
        addImageDimensions(pi)
    pageimages=PageImage.objects.filter(page__sourcecomponent__source=pi.page.sourcecomponent.source).order_by("page")
    source=pi.page.sourcecomponent.source
    ac=source.getAcCode()
    achash=hashlib.md5(ac.encode('UTF-8')).hexdigest()
    [next,prev]=getNextPrevPages(p,pageimages)
    work=getPageImageWork(pi,source)
    seaDragonURL=pi.getZoomifyPath()
    return render_to_response('frontend/cfeopageview.html', {'achash':achash,'work':work,'source':source,'prev':prev,'next':next,'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL,'pageimages':pageimages,'mode':mode,'seaDragonURL':seaDragonURL,'page': p, 'pageimage': pi}, context_instance=RequestContext(request))

@csrf_exempt
def comparePageImageview(request,compareleft=0,compareright=0):
    mode="CFEO"

    if compareleft == 0:
        compareleft = request.COOKIES.get('cfeo_compare_left')

    if compareright == 0:
        compareright = request.COOKIES.get('cfeo_compare_right')



    try:
        pi_left=PageImage.objects.get(id=compareleft)
    except:
        pi_left = None

    try:
        pi_right=PageImage.objects.get(id=compareright)
    except:
        pi_right = None


    print "left"
    print pi_left
    print "right:"
    print pi_right
    #p=pi.page
    #comparepi=PageImage.objects.get(id=compareid)
    #comparep=comparepi.page
    #pageimages=PageImage.objects.filter(page__sourcecomponent__source=pi.page.sourcecomponent.source)
    #source=pi.page.sourcecomponent.source
    #[next,prev]=getNextPrevPages(p,pageimages)

    #cpageimages=PageImage.objects.filter(page__sourcecomponent__source=pi.page.sourcecomponent.source)
    #compareSource=comparep.sourcecomponent.source
    #[comparenext,compareprev]=getNextPrevPages(comparep,cpageimages)
    #opus=Opus.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()[0]
    #work=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()[0]
    #settings.IMAGE_SERVER_URL
    return render_to_response('frontend/comparepageview.html', {'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL,'mode':mode, 'pi_left' : pi_left, 'pi_right': pi_right,}, context_instance=RequestContext(request))


@csrf_exempt
def cfeoSourceInformation(request,id):
    return sourceinformation(request,id,'CFEO')

@csrf_exempt
def cfeoWorkInformation(request,id):
    return workinformation(request,id,"CFEO")

#Display quick summary of source information
#params:  source id
@csrf_exempt
def sourceinformation(request, id,mode="OCVE"):
    source=Source.objects.get(id=id)
    si = SourceInformation.objects.get(source__id=id)
    pageimages=PageImage.objects.filter(page__sourcecomponent__source=source).order_by('page__orderno')
    work=source.getWork()
    si=cleanSourceInformationHTML(si)
    return render_to_response('frontend/sourceinformation.html', {'pageimages':pageimages,'mode':mode,'work':work,'source':source,'si': si, 'IMAGE_SERVER_URL':IMAGE_SERVER_URL,}, context_instance=RequestContext(request))

@csrf_exempt
def workinformation(request,id,mode="OCVE"):
    work=Work.objects.get(id=id)
    workinformation=work.workinformation
    return render_to_response('frontend/workinformation.html', {'workinformation':workinformation,'work':work,'mode':mode}, context_instance=RequestContext(request))

@csrf_exempt
def barview(request):
    opuses = Opus.objects.filter(opusno__gt=0)
    #The position in the work spine
    orderno=0
    workid=int(request.GET['workid'])
    work=Work.objects.get(id=workid)
    regionThumbs = []
    sources = []
    try:
        range=int(request.GET['range'])
    except MultiValueDictKeyError:
        range=1
    try:
        orderno=int(request.GET['orderNo'])
        spine=BarSpine.objects.filter(source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work,orderNo=orderno)
        if spine.count() > 0:
            bar=spine[0].bar
    except MultiValueDictKeyError:
        #Coming from page, find spine point with bar,pageimage
        barid=int(request.GET['barid'])
        pageimageid=int(request.GET['pageimageid'])
        bar=Bar.objects.get(id=barid)
        pageimage=PageImage.objects.get(id=pageimageid)
        #source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work
        spine=BarSpine.objects.filter(sourcecomponent__page__pageimage=pageimage,bar=bar)
        if spine.count() > 0:
            orderno=spine[0].orderNo
    if orderno > 0:
        barSpines=getSpinesByWork(work, orderno,range)
        #Arrange bar spines into groups based on source
        barSpines=sorted(barSpines, key=lambda sp: sp.source.orderno)
        for sp in barSpines:
            if sources.__contains__(sp.source) is False:
                sources.append(sp.source)
        regionThumbs=spinesToRegionThumbs(barSpines,range)
    sortedsources=sorted(sources, key=lambda source: source.orderno)
    sources=sortedsources
    mode = "OCVE"
    #barregions=getRegionsByBarOpus(bar,opus)
    # get next and previous, if available
    next = False
    prev = False
    if orderno > 0:
        try:
            nextOrder=orderno+1
            nextSpine=BarSpine.objects.filter(orderNo=nextOrder,source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work).distinct()
            if nextSpine.count() >0:
                next = nextSpine[0]
        except:
            next = False
        try:
            prevOrder=orderno-1
            prevSpine=BarSpine.objects.filter(orderNo=prevOrder,source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work).distinct()
            if prevSpine.count() >0:
                prev = prevSpine[0]
        except:
            prev = False

    # Quick and dirty way of setting a test template mode
    try:
        request.GET['template']
        return render_to_response('frontend/bar-view-html-design.html', {}, context_instance=RequestContext(request))
    except:
            return render_to_response('frontend/bar-view.html', {'mode' : mode, 'next':next,'range':range,'prev':prev, 'opuses': opuses,'orderNo':orderno,'bar':bar,'barregions':regionThumbs,'sources': sources, 'work': work, 'IMAGE_SERVER_URL': IMAGE_SERVER_URL, }, context_instance=RequestContext(request))


# Ajax call for inline collections display
@csrf_exempt
def ajaxInlineCollections(request):
        if request.user.is_authenticated():
                collections = BarCollection.objects.select_related().filter(user_id=request.user.id)
                thumbs = {}
                for c in collections:
                        for r in c.regions.all():
                                thumbs[r.id] =  BarRegionThumbnail(r, r.pageimage.page, r.pageimage)
        else:
                collections = None

        return render_to_response('frontend/ajax/inline-collections.html', {"collections" : collections, "thumbs" : thumbs, 'IMAGE_SERVER_URL': IMAGE_SERVER_URL}, context_instance=RequestContext(request))

@csrf_exempt
def ajaxChangeCollectionName(request):
        if request.user.is_authenticated():
                try:
                        collection_id = int(request.POST["collection_id"])
                        new_name = request.POST["new_collection_name"]

                        collection = BarCollection.objects.get(pk=collection_id)
                        if collection.user_id == request.user.id:
                                collection.name = new_name
                                collection.save()
                                status = 1
                        else:
                                status = 0

                except Exception, e:
                        status = 0
        else:
                status = 0
        return render_to_response('frontend/ajax/ajax-status.html', {"status" : status,}, context_instance=RequestContext(request))

@csrf_exempt
def ajaxAddCollection(request):
        if request.user.is_authenticated():
                try:
                        new_name = request.POST["new_collection_name"]

                        collection = BarCollection(user_id=request.user.id, name=new_name, xystring="")
                        collection.save()

                        status = collection.id

                except Exception, e:
                        status = 0
        else:
                status = 0
        return render_to_response('frontend/ajax/ajax-status.html', {"status" : status,}, context_instance=RequestContext(request))

# Ajax call for inline collections display
@csrf_exempt
def ajaxAddImageToCollectionModal(request):
        if request.user.is_authenticated():
                collections = BarCollection.objects.select_related().filter(user_id=request.user.id)
        else:
                collections = None

        return render_to_response('frontend/ajax/add-image-to-collection-modal.html', {"collections" : collections,}, context_instance=RequestContext(request))

# Ajax call for adding image to collection
@csrf_exempt
def ajaxAddImageToCollection(request):
        if request.user.is_authenticated():
                try:
                        # get post
                        collection_id = request.POST["collection_id"]
                        region_id = int(request.POST["region_id"])

                        # fetch collection
                        collection = BarCollection.objects.get(pk=collection_id)

                        if collection.user_id == request.user.id:

                                # fetch region
                                bar_region = BarRegion.objects.get(pk=region_id)

                                #check if it exists
                                if collection.regions.all().filter(id=bar_region.id).exists():
                                        status = 2
                                else:
                                        collection.regions.add(bar_region)
                                        status = 1
                        else:
                                status = 0

                except Exception, e:
                        status = 0
        else:
                status = 0

        return render_to_response('frontend/ajax/ajax-status.html', {"status" : status,}, context_instance=RequestContext(request))


# Ajax call for deleting an image from a collection
@csrf_exempt
def ajaxDeleteImageFromCollection(request):
        if request.user.is_authenticated():
                try:
                        # get post
                        collection_id = request.POST["collection_id"]
                        region_id = int(request.POST["region_id"])

                        # fetch collection
                        collection = BarCollection.objects.get(pk=collection_id)

                        if collection.user_id == request.user.id:

                                # fetch region
                                bar_region = BarRegion.objects.get(pk=region_id)

                                #check if it exists
                                if collection.regions.all().filter(id=bar_region.id).exists():

                                        #delete!
                                        collection.regions.remove(bar_region)
                                        status = 1
                                else:
                                        status = 2
                        else:
                                status = 3

                except Exception, e:
                        status = 4
        else:
                status = 0

        return render_to_response('frontend/ajax/ajax-status.html', {"status" : status,}, context_instance=RequestContext(request))

@csrf_exempt
def ajaxDeleteCollection(request):
        if request.user.is_authenticated():
                try:
                        collection_id = int(request.POST["collection_id"])
                        collection = BarCollection.objects.get(pk=collection_id)
                        if collection.user_id == request.user.id:
                                collection.delete()
                                status = 1
                        else:
                                status = 0

                except Exception, e:
                        status = 0
        else:
                status = 0
        return render_to_response('frontend/ajax/ajax-status.html', {"status" : status,}, context_instance=RequestContext(request))

