__author__ = 'Elliot'
 # coding=utf8

#Views for the user interface
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf import settings
from django.http import HttpResponse

from bartools import *
from uitools import *
from dbmi.spine import getSpinesByWork,spinesToRegionThumbs
from dbmi.sourceeditor import cleanHTML

#Takes pageimageid
from models import keyPitch
from models_generic import BarCollection
import json
import hashlib
from django.db import connection, transaction
from forms import AnnotationForm
import os


IIP_URL = settings.IIP_URL
IMAGE_SERVER_URL = settings.IMAGE_SERVER_URL

def cfeoacview(request,acHash,mode="OCVE"):
    return acview(request,acHash,'CFEO')

#Takes a passed hashed accode from annotated catalogue and displays the source in browse
def acview(request,acHash,mode="OCVE"):
    source=None
    filters=[]
    for ac in AcCode.objects.all():
        if hashlib.md5(ac.accode.encode('UTF-8')).hexdigest() == str(acHash):
            source=Source.objects.filter(sourceinformation__accode=ac)
            if source.count() >0:
                work=source[0].getWork()
                filters.append({'type':'Work','id':work.id,'selection':work.label})
                filters.append({'type':'Source','id':source[0].id,'selection':source[0]})
    return browse(request,mode,filters)

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


def browse(request,mode="OCVE",defaultFilters=None):
    #Filter Items
    #fixHistory()
    #cursor = connection.cursor()
    #update = connection.cursor()
    #cursor.execute("SELECT p.id,sc.label FROM ocve2real.ocve_page as p,ocve2real.ocve_sourcecomponent as sc where p.sourcecomponent_id=sc.id and p.pagetype_id=1")
    #for row in cursor.fetchall():
    #    update.execute("update ocve2real.ocve_page set pagetype_id=3 where id="+str(row[0]))
    #transaction.commit_unless_managed()
    try:
        if request.session[mode+'_current_filters']:
            filterJSON=request.session[mode+'_current_filters']
            defaultFilters=json.loads(filterJSON, encoding='utf-8')
    except KeyError:
        pass
        #defaultFilters = ''
    sourceTypes=SourceType.objects.all()
    if mode == 'OCVE':
        works=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__ocve=True).distinct()
        #dedicatees=Dedicatee.objects.filter(sourceinformation__source__ocve=True).filter(id__gt=2).distinct()
        publishers=Publisher.objects.filter(sourceinformation__source__ocve=True).filter(id__gt=2).distinct()
        years=Year.objects.filter(sourceinformation__source__ocve=True).distinct()
        keyPitches=keyPitch.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__ocve=True).distinct()
        genres=Genre.objects.filter(work__workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__ocve=True).filter(id__gt=2).distinct()
    else:
        works=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__cfeo=True).distinct()
        #dedicatees=Dedicatee.objects.filter(sourceinformation__source__cfeo=True).distinct()
        publishers=Publisher.objects.filter(sourceinformation__source__cfeo=True).distinct()
        years=Year.objects.filter(sourceinformation__source__cfeo=True).distinct()
        keyPitches=keyPitch.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__cfeo=True).distinct()
        genres=Genre.objects.filter(work__workcomponent__sourcecomponent_workcomponent__sourcecomponent__source__cfeo=True).distinct()
    return render_to_response('frontend/browse.html', {'defaultFilters':defaultFilters, 'mode':mode,'keypitches':keyPitches,'sourceTypes':sourceTypes,'years':years,'publishers':publishers,'genres':genres,'works':works, 'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL}, context_instance=RequestContext(request))


#Optimised for OCVE
def sourcejs(request):
    serializeOCVESourceJson()
    serializeCFEOSourceJson()
    serializeAcCodeConnector()

    # for pi in PageImage.objects.all():
    #      textlabel="p. "+pi.page.label
    #      if pi.page.sourcecomponent.label != 'Score':
    #          textlabel=textlabel+" "+pi.page.sourcecomponent.label
    #      if pi.endbar != '0':
    #          textlabel=textlabel+", bs "+pi.startbar+"-"+pi.endbar
    #      if len(pi.textlabel) == 0:
    #         pi.textlabel=textlabel
    #         pi.save()
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
#Annotation.objects.filter(type_id=1).delete()
def ocvePageImageview(request,id):
    regionURL = "/ocve/getBarRegions/" + id + "/"
    noteURL = "/ocve/getAnnotationRegions/" + id + "/"
    pi=PageImage.objects.get(id=id)
    p=pi.page
    newN=Annotation(pageimage=pi)
    annotationForm=AnnotationForm(instance=newN)
    source=pi.page.sourcecomponent.source
    #allBars=Bar.objects.filter(barregion__pageimage__page__sourcecomponent__source=source).order_by('barnumber').distinct()
    barDict={}
    pageimages=PageImage.objects.filter(page__sourcecomponent__source=pi.page.sourcecomponent.source,page__pagetype_id=3)
    #Get all bars on relevant pages to form quickjump menu 'allBars':allBars,
    cursor=connection.cursor()
    cursor.execute("select bar.barlabel,pi.id from ocve_bar as bar,ocve_bar_barregion as brr, ocve_barregion as barregion,ocve_pageimage as pi,ocve_page as p,ocve_sourcecomponent as sc where bar.id=brr.bar_id and brr.barregion_id=barregion.id and barregion.pageimage_id=pi.id and pi.page_id=p.id and p.sourcecomponent_id=sc.id and sc.source_id="+str(source.id)+" order by bar.barnumber")
    notes=Annotation.objects.filter(pageimage_id=id,type_id=1)
    comments=Annotation.objects.filter(pageimage_id=id,type_id=2)
    [next,prev]=getNextPrevPages(p,pi)
    #opus=Opus.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()[0]
    work=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()[0]
    zoomifyURL=pi.getZoomifyPath()
    mode="OCVE"
    return render_to_response('frontend/pageview.html', {'annotationForm':annotationForm,'notes':notes,'comments':comments,'allBars':cursor,'work':work,'source':source,'prev':prev,'next':next,'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL,'pageimages':pageimages,'mode':mode,'zoomifyURL':zoomifyURL,'regionURL':regionURL,'noteURL':noteURL,'page': p, 'pageimage': pi}, context_instance=RequestContext(request))


def ocveViewInPage(request,id,barid):
    regionURL = "/ocve/getBarRegions/" + id + "/" + barid + "/"
    pi=PageImage.objects.get(id=id)
    p=pi.page
    source=pi.page.sourcecomponent.source
    pageimages=PageImage.objects.filter(page__sourcecomponent__source=pi.page.sourcecomponent.source,page__pagetype_id=3)
    opus=Opus.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()
    work=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()[0]
    zoomifyURL=pi.getZoomifyPath()
    mode="OCVE"
    return render_to_response('frontend/viewinpage.html', {'work':work,'source':source,'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL,'pageimages':pageimages,'mode':mode,'opus':opus,'zoomifyURL':zoomifyURL,'regionURL':regionURL,'page': p, 'pageimage': pi}, context_instance=RequestContext(request))
    
def cfeoPageImageview(request,id):
    mode="CFEO"
    pi=PageImage.objects.get(id=id)
    p=pi.page
    pageimages=PageImage.objects.filter(page__sourcecomponent__source=pi.page.sourcecomponent.source)
    source=pi.page.sourcecomponent.source
    [next,prev]=getNextPrevPages(p,pageimages)
    opus=Opus.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()
    work=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__page__pageimage=pi).distinct()[0]
    seaDragonURL=pi.getZoomifyPath()
    return render_to_response('frontend/cfeopageview.html', {'work':work,'source':source,'prev':prev,'next':next,'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL,'pageimages':pageimages,'mode':mode,'opus':opus,'seaDragonURL':seaDragonURL,'page': p, 'pageimage': pi}, context_instance=RequestContext(request))

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


def sourceDisplay(request,o,sources):
    opuses = Opus.objects.filter(opusno__gt=0)
    instruments=getInstrumentsByOpus(o)
    work=None
    if sources is not None and sources.__len__()>0:
        work=sources[0].getWork()
    return render_to_response('editionprototype.html', {'work':work,'instruments':instruments,'sources': sources, 'opuses': opuses, 'opus':o, 'IMAGE_SERVER_URL' : IMAGE_SERVER_URL}, context_instance=RequestContext(request))

def getSource(request,id):
    if id > 0:
        o = Opus.objects.get(id=id)
        sources = Source.objects.filter(sourcecomponent__sourcecomponent_workcomponent__workcomponent__opus=o).distinct()
    return sourceDisplay(request,o,sources)

def sourceprototype(request):
    return sourceDisplay(request,None,[])

def cfeoSourceInformation(request,id):
    return sourceinformation(request,id,'CFEO')

def cfeoWorkInformation(request,id):
    return workinformation(request,id,"CFEO")

#Display quick summary of source information
#params:  source id
def sourceinformation(request, id,mode="OCVE"):
    source=Source.objects.get(id=id)
    si = SourceInformation.objects.get(source__id=id)
    pageimages=PageImage.objects.filter(page__sourcecomponent__source=source).order_by('page__orderno')
    work=source.getWork()
    return render_to_response('frontend/sourceinformation.html', {'pageimages':pageimages,'mode':mode,'work':work,'source':source,'si': si, 'IMAGE_SERVER_URL':IMAGE_SERVER_URL,}, context_instance=RequestContext(request))

def workinformation(request,id,mode="OCVE"):
    work=Work.objects.get(id=id)
    workinformation=work.workinformation
    return render_to_response('frontend/workinformation.html', {'workinformation':workinformation,'work':work,'mode':mode}, context_instance=RequestContext(request))


def barview(request):
    opuses = Opus.objects.filter(opusno__gt=0)
    barid=int(request.GET['barid'])
    workid=int(request.GET['workid'])
    #todo:Preload collection (to make collection view from user page)
    #sourceid=int(request.GET['sourceid'])
    bar=Bar.objects.get(id=barid)
    work=Work.objects.get(id=workid)
    #source=Source.objects.get(id=sourceid)
    spine=BarSpine.objects.filter(source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work,bar=bar)
    regionThumbs = []
    sources = []
    if spine.count() > 0:
        orderno=spine[0].orderNo
        barSpines=getSpinesByWork(work, orderno)
        for sp in barSpines:
            sources.append(sp.source)
        barSpines=sorted(barSpines, key=lambda sp: sp.source.orderno)
        regionThumbs=spinesToRegionThumbs(barSpines)
    sortedsources=sorted(sources, key=lambda source: source.orderno)
    sources=sortedsources
    mode = "OCVE"
    #barregions=getRegionsByBarOpus(bar,opus)
    # get next and previous, if available
    next = False
    prev = False
    if spine.count() > 0:
        try:
            nextOrder=spine[0].orderNo+1
            nextSpine=BarSpine.objects.filter(orderNo=nextOrder,source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work).distinct()
            if nextSpine.count() >0:
                next = nextSpine[0]
        except:
            next = False
        try:
            prevOrder=spine[0].orderNo-1
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
	    return render_to_response('frontend/bar-view.html', {'mode' : mode, 'next':next, 'prev':prev, 'opuses': opuses, 'bar':bar,'barregions':regionThumbs,'spine':spine,'sources': sources, 'work': work, 'IMAGE_SERVER_URL': IMAGE_SERVER_URL, }, context_instance=RequestContext(request))

#AJAX call to save bars from existing collection
def saveCollection(request):
    return HttpResponse("")

#For removing collection.  Context user page only?
def deleteCollection(request):
    return HttpResponse("")
    
    
# Ajax call for inline collections display
def ajaxInlineCollections(request):
	if request.user.is_authenticated():
		collections = BarCollection.objects.select_related().filter(user=request.user)
		thumbs = {}
		for c in collections:
			for r in c.regions.all():
				thumbs[r.id] =  BarRegionThumbnail(r, r.pageimage.page, r.pageimage)
	else:
		collections = None
			
	return render_to_response('frontend/ajax/inline-collections.html', {"collections" : collections, "thumbs" : thumbs, 'IMAGE_SERVER_URL': IMAGE_SERVER_URL}, context_instance=RequestContext(request))
	
def ajaxChangeCollectionName(request):
	if request.user.is_authenticated():
		try:
			collection_id = int(request.POST["collection_id"])
			new_name = request.POST["new_collection_name"]
			
			collection = BarCollection.objects.get(pk=collection_id)
			if collection.user == request.user:
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

def ajaxAddCollection(request):
	if request.user.is_authenticated():
		try:
			new_name = request.POST["new_collection_name"]
			
			collection = BarCollection(user=request.user, name=new_name, xystring="")
			collection.save()
			
			status = collection.id
			
		except Exception, e:
			status = 0
	else:
		status = 0
	return render_to_response('frontend/ajax/ajax-status.html', {"status" : status,}, context_instance=RequestContext(request))

# Ajax call for inline collections display
def ajaxAddImageToCollectionModal(request):
	if request.user.is_authenticated():
		collections = BarCollection.objects.select_related().filter(user=request.user)
	else:
		collections = None
	
	return render_to_response('frontend/ajax/add-image-to-collection-modal.html', {"collections" : collections,}, context_instance=RequestContext(request))

# Ajax call for adding image to collection
def ajaxAddImageToCollection(request):
	if request.user.is_authenticated():
		try:
			# get post
			collection_id = request.POST["collection_id"]
			region_id = int(request.POST["region_id"])
			
			# fetch collection
			collection = BarCollection.objects.get(pk=collection_id)
			
			if collection.user == request.user:
				
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
def ajaxDeleteImageFromCollection(request):
	if request.user.is_authenticated():
		try:
			# get post
			collection_id = request.POST["collection_id"]
			region_id = int(request.POST["region_id"])
			
			# fetch collection
			collection = BarCollection.objects.get(pk=collection_id)
			
			if collection.user == request.user:
				
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
	
def ajaxDeleteCollection(request):
	if request.user.is_authenticated():
		try:
			collection_id = int(request.POST["collection_id"])			
			collection = BarCollection.objects.get(pk=collection_id)
			if collection.user == request.user:
				collection.delete()
				status = 1
			else:
				status = 0
			
		except Exception, e:
			status = 0
	else:
		status = 0
	return render_to_response('frontend/ajax/ajax-status.html', {"status" : status,}, context_instance=RequestContext(request))