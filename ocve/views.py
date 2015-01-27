# Create your views here.


from dbmi.editviews import *
from uiviews import *
from dbmi.uploader import *

IIP_URL = settings.IIP_URL
IMAGE_SERVER_URL = settings.IMAGE_SERVER_URL

#Image format for all uploaded pages
#Forced rather than detected because only tifs should be uploaded
UPLOAD_EXTENSION = '.tif'

#Error reporting template
errorPage = 'error.html'

def sourcesbyshelfmark(request):
    sources=Source.objects.all().order_by('sourceinformation__shelfmark')
    return render_to_response('sourcesbyshelfmark.html', {'sources': sources},
        context_instance=RequestContext(request))

def buildHierarchy(request):
    #buildTree()
    #posthumousFix()
    return HttpResponse("")


def works(request):
    works = Work.objects.distinct()
    return render_to_response('tree.html', {'works': works},
        context_instance=RequestContext(request))


def work(request, id):
    w = Work.objects.get(id=id)
    wdict = w.__dict__
    sources = w.getSources()
    #sources = Source.objects.filter(sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=w).distinct()
    return render_to_response('tree.html', {'work': w, 'wdict': wdict,'sources': sources, 'IMAGE_SERVER_URL': IMAGE_SERVER_URL,}      ,
        context_instance=RequestContext(request))

def page(request, id):
    page = Page.objects.get(id=id)
    pageimages = page.getPrimaryPageImage()
    return render_to_response('page_ui.html', {'page': page, 'pageimages': pageimages , 'IMAGE_SERVER_URL': IMAGE_SERVER_URL,}      ,
        context_instance=RequestContext(request))



def source(request, id):
    source = Source.objects.get(id=id)
    sLegacy = SourceLegacy.objects.get(source=source)
    si = SourceInformation.objects.get(source=source)
    w = Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source=source).distinct()[0]
    #Multiple Instruments
    sComps = SourceComponent.objects.filter(source=source).distinct()
    if sComps.__len__() == 1:
        #Skip over source components and go straight to pages
        pages = Page.objects.filter(sourcecomponent__source=source)
        return render_to_response('tree.html',
                {'pages': pages, 'source': source, 'work': w, 'si': si, 'sLegacy': sLegacy},
            context_instance=RequestContext(request))
    else:
        #Display source components
        return render_to_response('tree.html', {'sComps': sComps, 'source': source, 'work': w, 'si': si},
            context_instance=RequestContext(request))


def workComp(request, id):
    comp = WorkComponent.objects.get(id=id)
    sComps = SourceComponent.objects.filter(sourcecomponent_workcomponent__workcomponent=comp)
    source = comp.source
    sLegacy = SourceLegacy.objects.get(source=source)
    pages = Page.objects.filter(sourcecomponent=comp)
    return render_to_response('tree.html', {'sComps': sComps, 'source': source, 'sLegacy': sLegacy},
        context_instance=RequestContext(request))


def sourceComp(request, id):
    comp = SourceComponent.objects.get(id=id)
    source = comp.source
    pages = PageImage.objects.filter(page__sourcecomponent=comp).order_by('page__orderno')
    return render_to_response('tree.html', {'pages': pages, 'comp': comp, 'source': source},
        context_instance=RequestContext(request))

#    source=Tree.objects.get(id=int(id))
#    pages=Tree.objects.filter(parent=source)


def uploadOCVE(request):
    log = upload(request)
    return HttpResponse(log)


def regionTest(request):
    #importBarRegions()
    return HttpResponse("")


def getBarRegions(request, id):
    geos = getGeoJSON(id)
    return render_to_response('geojson.html', {'geoRegions': geos, 'grouped': 0})



def getViewInPageRegions(request, id, barid):
    geos = getViewInPageJSON(id,barid)
    return render_to_response('geojson.html', {'geoRegions': geos, 'grouped': 0})



def getGroupedBarRegions(request, id):
    geos = getGeoJSON(id)
    return render_to_response('geojson.html', {'geoRegions': geos, 'grouped': 1})




def iipPage(request, id):
    source=None
    try:
        np = NewPageImage.objects.get(id=id)
        source = np.source
        #zoomifyURL = "https://ocve2-stg.cch.kcl.ac.uk/iip/iipsrv.fcgi"
        jp2Path='jp2/newjp2/'+str(np.id)+'.jp2'
    except ObjectDoesNotExist:
        np=PageImage.objects.get(id=id)
        source=Source.objects.filter(sourcecomponent__page__pageimage__id=id)[0]
        jp2Path=np.getJP2Path()
    return render_to_response('page.html', {'np': np, 'source': source, 'jp2Path': jp2Path, 'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL},
        context_instance=RequestContext(request))

#Index page for the DBMi/ bar editor
#I have made this a template so logging/edit status summaries can be attached later if needed
def dbmiView(request):
    return render_to_response('editindex.html', context_instance=RequestContext(request))

#A quick and dirty view for internal use only to examine source's structure
def sourceStructureView(request, id):
    source = Source.objects.get(id=id)
    works = Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent__source=source).distinct()
    out = ''
    sourcePages = Page.objects.filter(sourcecomponent__source=source)
    out += "<h1>" + source.cfeolabel + "</h1>"
    out += "<ul>"
    scomps = SourceComponent.objects.filter(source=source)
    out += "<ul>"
    for sc in scomps:
        works=Work.objects.filter(workcomponent__sourcecomponent_workcomponent__sourcecomponent=sc)
        out += "<li>"
        for w in works:
            out+=w.label+" "
        out +=  sc.label +" ("+str(sc.id)+")"
        pages = Page.objects.filter(sourcecomponent=sc)
        out += "<ul>"
        for p in pages:
            pi = PageImage.objects.get(page=p)
            out += "<li> <a href=\"/admin/ocve/page/"+ str(p.id) + "/\">" + p.label + "</a> " \
                   + str(pi.startbar) + "-" + str(pi.endbar)
            out+= "</li>"
        out += "</ul>"
        out += "</li>"
    out += "</ul>"
    out += "</li>"
    # out+= "</ul>"
    # out+= "</li>"

    out += "</ul>"
    out += "<h2> all pages for this source</h2><ul>"
    sourcePages = Page.objects.filter(sourcecomponent__source=source)
    for p in sourcePages:
        pi = PageImage.objects.get(page=p)
        workcomponents= WorkComponent.objects.filter(sourcecomponent_workcomponent__sourcecomponent=p.sourcecomponent)
        out += "<li><a href=\"#\" name=\"" + str(p.id) + "\">" + str(p.id) + "</a>"+p.label + " " + str(pi.startbar) + "-" + str(pi.endbar)
        out+= " ("+p.sourcecomponent.label+": <a href=\"/admin/ocve/sourcecomponent/"+str(p.sourcecomponent.id)+"/\">"+str(p.sourcecomponent.id)+"</a> "+str(p.sourcecomponent.orderno)+")"
        if workcomponents:
            wc=workcomponents[0]
            out+= " -> "+wc.label+": <a href=\"/admin/ocve/workcomponent/"+str(wc.id)+"/\">"+str(wc.id)+"</a> "
        out += "<form action=\"/ocve/updatesc/\" method=\"POST\"><input type=\"hidden\" name=\"page_id\" value=\""+ str(p.id) +"\">"
        out += "<input name=\"sourcecomponent_id\" type=\"text\" size=\"3\" value=\"0\"><input type=\"submit\"></form>"
        out+= "</li>"
    out += "</ul>"
    return render_to_response("structure.html",
            {'out': out},
        context_instance=RequestContext(request))


def updateSourceComponent(request):
    page_id=int(request.POST['page_id'])
    component_id=int(request.POST['sourcecomponent_id'])
    p=Page.objects.get(id=page_id)
    sc=SourceComponent.objects.get(id=component_id)
    if p is not None and sc is not None:
        p.sourcecomponent=sc
        p.save()
    return HttpResponseRedirect("/ocve/structure/18153/#"+str(page_id))




def user_profile(request):
    return render_to_response("registration/user_profile.html",
            {},
        context_instance=RequestContext(request))
