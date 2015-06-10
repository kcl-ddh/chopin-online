import subprocess
import shlex


__author__ = 'Elliott Hall'
#All view functions for editing bar information
from ocve.imagetools import verifyImagesViaIIP
from django.contrib.auth.decorators import login_required
from bareditor import editBarsURL
from django.db.models import *
from sourceeditor import *
from ocve.uitools import generateThumbnails
import shutil

from django import template
IMAGE_SERVER_URL = settings.IMAGE_SERVER_URL
IMAGEFOLDER= settings.IMAGEFOLDER

register = template.Library()

UPLOAD_EXTENSION = settings.UPLOAD_EXTENSION
STATIC_URL = settings.STATIC_URL

#Index page for the DBMi/ bar editor
#I have made this a template so logging/edit status summaries can be attached later if needed
def dbmiView(request):
    return render_to_response('dbmi/editindex.html', context_instance=RequestContext(request))


def fixrangeview(request):
    #log=fixBarRange()
    uploadOCVEOpus28()
    return HttpResponse(log)




@login_required
def selectSource(request):
    sForm = NewSourceForm()
    convert = lambda text: ('', int(text)) if text.isdigit() else (text, 0)
    newSources = sorted(NewSource.objects.all(), key=lambda a: [convert(c) for c in re.split('([0-9]+)', a.sourcecode)])
    return render_to_response('dbmi/selectsource.html', {'newSourceForm': sForm, 'newSources': newSources},
                              context_instance=RequestContext(request))


@login_required
def addSource(request):
    s = NewSourceForm(request.POST)
    errormsg = ''
    try:
        #Check to make sure sourcecode does not exist
        sc = request.POST['sourcecode']
        if sc is None or sc.__len__() == 0:
            errormsg = 'Please provide a source code'
        else:
            dupCheck = NewSource.objects.filter(sourcecode=sc)
            if dupCheck.__len__() > 0:
                errormsg = 'Source Code already exists'
            else:
                newS = s.save()
                return render_to_response('uploadPage.html', {'source': newS})
    except MultiValueDictKeyError:
        errormsg = 'Please provide a source code'
    newSources = NewSource.objects.all()
    return render_to_response('dbmi/selectsource.html', {'errormsg': errormsg, 'newSourceForm': s, 'newSources': newSources},
                              context_instance=RequestContext(request))

@csrf_exempt
def addPages(request):
    if request.method == 'POST':
        try:
            s = NewSource.objects.get(id=int(request.POST['source']))
            if request.FILES is not None:
                fname = request.FILES['Filedata'].name
                if fname.__len__() > 0:
                    npi = NewPageImage(source=s, filename=fname, surrogate=1, versionnumber=1, permission=False,
                                       permissionnote='', height=0, width=0, startbar=0, endbar=0, corrected=0)
                    npi.save()
                    handle_uploaded_file(request.FILES['Filedata'], str(npi.id) + UPLOAD_EXTENSION)
                    # remove alpha channel from uploaded tif
                    os.system('convert '+IMAGEFOLDER+'upload/%s.tif -alpha Off '+IMAGEFOLDER+'upload/%s.tif' % (
                    str(npi.id), str(npi.id)))
                    os.system('kdu_compress -i '+IMAGEFOLDER+'upload/' + str(
                        npi.id) + '.tif -o '+IMAGEFOLDER+'jp2/newjp2/' + str(
                        npi.id) + '.jp2 -rate -,4,2.34,1.36,0.797,0.466,0.272,0.159,0.0929,0.0543,0.0317,0.0185 Creversible=yes Clevels=5 Stiles=\{1024,1024\} Cblk=\{64,64\} Corder=RPCL Cmodes=BYPASS')
        except MultiValueDictKeyError:
            pass
    return HttpResponse("")


#Apply the offsets passed from editor tool to all regions on page
#signal that page has been corrected.
@csrf_exempt
def correctCrop(request):
    id = str(request.POST['pageID'])
    offsetX = int(request.POST['offsetX'])
    offsetY = int(request.POST['offsetY'])
    correctCropping(id, offsetX, offsetY)
    pi = PageImage.objects.get(id=int(id))
    pl = PageLegacy.objects.get(pageimage=pi)
    pl.cropCorrected = 1
    pl.save()
    return HttpResponse("")


def addToSource(request, id):
    newS = NewSource.objects.get(id=id)
    newPages = NewPageImage.objects.filter(source=newS)
    sources = NewSource.objects.all()
    oldSources = Source.objects.all()

    return render_to_response('uploadPage.html',
                              {'source': newS, 'newPages': newPages, 'sources': sources, 'oldSources': oldSources,
                               'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL},
                              context_instance=RequestContext(request))


#Mark the current editing status of a page/source
@csrf_exempt
def updateStatus(request):
    sourceid = 0
    pageid = 0
    statusid = int(request.POST['status'])
    try:
        sourceid = int(request.POST['id'])
    except MultiValueDictKeyError:
        pass
    if sourceid == 0:
        try:
            pageid = int(request.POST['page_id'])
        except MultiValueDictKeyError:
            pass
    if sourceid > 0:
        #Apply this status update to all of source's pages?
        andpages = 0
        try:
            andpages = int(request.POST['andpages'])
        except MultiValueDictKeyError:
            pass
        try:
            s = Source.objects.get(id=sourceid)
            ls = SourceLegacy.objects.get(source=s)
            status = EditStatus.objects.get(id=statusid)
            ls.editstatus = status
            ls.save()
            if andpages == 1:
                pls = PageLegacy.objects.filter(pageimage__page__sourcecomponent__source=s)
                for pl in pls:
                    pl.editstatus = status
                    pl.save()
        except ObjectDoesNotExist:
            print 'Bad source ' + str(id)
            #TODO: Use reverse() for sustainability when it works
        #return uncorrectedSource(request,sourceid)
        return HttpResponseRedirect('/ocve/sourceview/' + str(sourceid) + '/')
    if pageid > 0:
        try:
            pi = PageImage.objects.get(id=pageid)
            pl = PageLegacy.objects.get(pageimage=pi)
            status = EditStatus.objects.get(id=statusid)
            pl.editstatus = status
            pl.save()
        except ObjectDoesNotExist:
            print 'Bad page ' + str(id)
            #TODO: Use reverse() for sustainability when it works
        return HttpResponseRedirect(editBarsURL + str(pageid) + '/')


def verifyImages(request):
    log = verifyImagesViaIIP()
    return HttpResponse(log)


@login_required
def modifyPage(request):
    id = 0
    if request.method == 'POST':
        try:
            id = int(request.POST['sourceID'])
            npids = request.POST.getlist('npid')
            try:
                if request.POST['movePages']:
                    nsid = request.POST['moveSource']
                    try:
                        newsource = NewSource.objects.get(id=nsid)
                        for nid in npids:
                            try:
                                np = NewPageImage.objects.get(id=nid)
                                np.source = newsource
                                np.permissionnote = ''
                                np.save()
                            except ObjectDoesNotExist:
                                pass
                    # added support for adding uploaded images to cfeo legacy sources
                    except:
                        oldsource = Source.objects.get(id=nsid)
                        for nid in npids:
                            sc = oldsource.getSourceComponents()[0]
                            spage = Page(label='uploaded', sourcecomponent=sc)
                            spage.save()
                            np = NewPageImage.objects.get(id=nid)
                            spageimage = PageImage(page=spage, startbar=0, endbar=0, corrected=0, height=0,
                                                   width=np.width)
                            spageimage.save()
                            pagelegacy = PageLegacy(pageimage=spageimage, jp2='newjp2/' + str(np.id) + '.jp2',
                                                    editstatus=EditStatus.objects.get(id=2), cropCorrected=1)
                            pagelegacy.save()
                            np.linked = 0
                            np.save()
            except MultiValueDictKeyError:
                try:
                    if request.POST['deletePages']:
                        for nid in npids:
                            np = NewPageImage.objects.get(id=nid)
                            np.delete()
                except MultiValueDictKeyError:
                    try:
                        if request.POST['duplicatePages']:
                            for nid in npids:
                                np = NewPageImage.objects.get(id=nid)
                                np.id = None
                                np.save()
                                newid = np.id
                                pl = PageLegacy.objects.filter()
                                oldpath = IMAGEFOLDER+'jp2/newjp2/' + str(nid) + '.jp2'
                                newpath = IMAGEFOLDER+'jp2/newjp2/' + str(newid) + '.jp2'
                                shutil.copyfile(oldpath, newpath)
                                np.linked = 0
                                np.filename = str(newid) + '.jp2'
                                np.save()
                    except MultiValueDictKeyError:
                        pass
        except MultiValueDictKeyError:
            pass
    return addToSource(request, id)


def uncorrectedSource(request, id):
    source = Source.objects.get(id=id)
    pages = PageImage.objects.filter(page__sourcecomponent__source=source).order_by('page__orderno')
    sourceStatuses = EditStatus.objects.all()
    return render_to_response('dbmi/correctview.html', {'source': source, 'pages': pages, 'statuses': sourceStatuses},
                              context_instance=RequestContext(request))


#OCVE sources that have yet to be corrected for Sarah
#.filter(sourcelegacy__corrected=0)
def sourceView(request, m):
    mode = int(m)
    title = ''
    ordermode = 1
    sourceQuery = ''
    filterComplete = 0
    try:
        ordermode = int(request.POST['ordermode'])
        filterComplete = int(request.POST['filtercomplete'])
        request.session.__setitem__('sourceViewOrderMode', ordermode)
        request.session.__setitem__('sourceViewFilterComplete', filterComplete)
    except MultiValueDictKeyError:
        try:
            ordermode = int(request.session.__getitem__('sourceViewOrderMode'))
            filterComplete = int(request.session.__getitem__('sourceViewFilterComplete'))
        except KeyError:
            pass
    if mode == 1:
        #By accode
        sourceQuery = Source.objects.all().distinct().order_by('sourceinformation__accode')
    elif mode == 2:
        #OCVE 1 only sources and Mellon-flagged CFEO sources
        sourceQuery = Source.objects.filter(sourcelegacy__needsBarLines=1).distinct()
        title = 'Annotated Sources'
    elif mode == 3:
        #CFEO sources only
        sourceQuery = Source.objects.filter(sourcelegacy__cfeoKey__gt=0)
    elif mode == 4:
        #all
        sourceQuery = Source.objects.all().order_by(
            'sourcecomponent__sourcecomponent_workcomponent__workcomponent__opus', 'label')
        #filter out sources marked as complete if user requests it
    if filterComplete == 1:
        sourceQuery = sourceQuery.exclude(sourcelegacy__editstatus__id=10)
    x = 0
    keys = []
    sourceQuery = sourceQuery.distinct()
    #Order the sources based on user input, or by opus if none selected
    if ordermode == 1:
        #sourceQuery=sourceQuery.order_by('sourcecomponent__sourcecomponent_workcomponent__workcomponent__opus__opusno')
        sourceQuery = sourceQuery.annotate(
            opusno=Max('sourcecomponent__sourcecomponent_workcomponent__workcomponent__opus__opusno')).order_by(
            'opusno')
    elif ordermode == 2:
        #edit status
        #sourceQuery=sourceQuery.order_by('sourcelegacy__editstatus__id')
        sourceQuery = sourceQuery.annotate(editStatus=Max('sourcelegacy__editstatus__id')).order_by('editStatus')
    sourcecounts = {}
    stats = EditStatus.objects.all()
    sources = []

    request.session.__setitem__('sourceViewMode', mode)
    for s in stats:
        sourcecounts[s] = 0
        #for s in sourceQuery:
    for s in sourceQuery:
        try:
            if keys.index(s.id) > -1:
                nothing = 0
        except ValueError:
            if s.getEditStatus() <> "":
                sources.append(s)
                keys.append(s.id)
                sourcecounts[s.getEditStatus()] += 1
                x += 1
            #            keys.append(s.id)
            #            sources.append(s)
            #            sourcecounts[s.getEditStatus()] += 1
            #            x += 1

    return render_to_response('dbmi/correctview.html',
                              {'title': title, 'sources': sources, 'sourcecounts': sourcecounts, 'ordermode': ordermode,
                               'filterComplete': filterComplete},
                              context_instance=RequestContext(request))


def loadEditPage(request, id):
    #pageID=request.POST['pageId']
    pageID = 4
    page = Page.objects.get(id=id)
    pageimage = PageImage.objects.filter(page=page)
    l = PageLegacy.objects.get(pageimage=pageimage)
    regions = barRegionsByPage(int(id))
    regionThumbs = []
    for r in regions:
        b = BarRegionThumbnail(r, page, pageimage[0])
        regionThumbs.append(b)
        #geos=toGeos(regions)
    #TODO:  How are we limiting bar number choices?
    #availBars=Bar.objects.filter(barnumber__range=(77,9fe9))
    return render_to_response('annotation.html', {'page': page, 'regionThumbs': regionThumbs, 'legacy': l},
                              context_instance=RequestContext(request))



def findUnverifiedImages(request):
    log = "<html><head></head><body>"
    log += "<table>"
    unv = PageLegacy.objects.filter(jp2="UNVERIFIED")
    mode = 0
    try:
        mode = request.GET['mode']
    except MultiValueDictKeyError:
        mode = 0
    found = 0
    missing = 0
    multiple = 0
    verified = 0
    for u in unv:
        command = str("find "+IMAGEFOLDER+"jp2 -iname " + u.filename + ".jp2")
        args = shlex.split(command)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        miss = 0
        if out.__len__() > 0:
            if out.count("\n") > 1:
                multiple += 1
                paths = out.split("\n")
                #for p in paths:
                # p=p.replace("/vol/ocve2/images","")
                #v=verifyImageDimensions(u.pageimage,path)
                #if v==1:
                #   out=p
            else:
                path = out.replace("\n", "")
                path = path.replace("/vol/ocve2/images/", "")
                v = verifyImageDimensions(u.pageimage, path)
                #out="<img title=\""+path+"\" src=\"http://ocve2.cch.kcl.ac.uk/iip/iipsrv.fcgi?FIF="+path+"&cnt=1&QLT=70&HEI=100&CVT=JPG\">"
                out = "<img title=\"" + path + "\" src=\"/iip/iipsrv.fcgi?FIF=" + path + "&cnt=1&QLT=70&HEI=100&CVT=JPG\">"
                u.jp2 = path
                u.save()
                if v == 1:
                    verified += 1
                else:
                    found += 1
        else:
            #Not where it should be, try to find in
            missing += 1
            miss = 1

        try:
            if mode == 0:
                log = log + "<tr><td>" + str(u.pageimage.id) + "</td><td>" + str(
                    u.filename) + "</td><td>" + out + "</td></tr>"
            elif mode == 1 and miss == 1:
                #missing only
                log = log + "<tr><td>" + str(u.pageimage.id) + "</td><td>" + str(
                    u.filename) + "</td><td>" + out + "</td></tr>"
        except UnicodeDecodeError:
            log = log + "<tr><td>" + str(
                u.pageimage.id) + "</td><td>FILENAME UNICODE ERROR</td><td>" + out + "</td></tr>"
    log += "</table><ul><li>Found: " + str(found) + "</li><li>Missing: " + str(missing) + "</li><li>Verified: " + str(
        verified) + "</li><li>Multiple: " + str(multiple) + "</li></ul></body></html>"
    return HttpResponse(log)

@csrf_exempt
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
    return render_to_response('dbmi/newpage.html', {'np': np, 'source': source, 'jp2Path': jp2Path, 'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL},
        context_instance=RequestContext(request))



def sourcesbywork(request):
    works = Work.objects.all()
    return render_to_response('dbmi/sourcesbywork.html',
                              {'works': works, 'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL, },
                              context_instance=RequestContext(request))



def worksview(request):
    works = Work.objects.distinct()
    return render_to_response('dbmi/tree.html', {'works': works},
        context_instance=RequestContext(request))


def work(request, id):
    w = Work.objects.get(id=id)
    wdict = w.__dict__
    sources = w.getSources()
    #sources = Source.objects.filter(sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=w).distinct()
    return render_to_response('dbmi/tree.html', {'work': w, 'wdict': wdict,'sources': sources, 'IMAGE_SERVER_URL': IMAGE_SERVER_URL,}      ,
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
        return render_to_response('dbmi/tree.html',
                {'pages': pages, 'source': source, 'work': w, 'si': si, 'sLegacy': sLegacy},
            context_instance=RequestContext(request))
    else:
        #Display source components
        return render_to_response('dbmi/tree.html', {'sComps': sComps, 'source': source, 'work': w, 'si': si},
            context_instance=RequestContext(request))

#A custom admin view to show the relevant objects for a single opus
#and a quick list of the sources attached to it
def workadmin(request,id):
    w = Work.objects.get(id=id)
    wform=WorkForm(instance=w)
    #Work information
    winfoform=WorkInformationForm(instance=w.workinformation)
    comps=WorkComponent.objects.filter(work=w)
    compFormset=WorkComponentFormset(queryset=comps)
    sources=w.getSources()
    return render_to_response('dbmi/workadmin.html', {'work': w, 'compFormset':compFormset,'workform': wform,'workinformationform': winfoform,'workcomponents':comps, 'sources':sources}      ,
        context_instance=RequestContext(request))

@csrf_exempt
def savework(request,id):
    workform=WorkForm(request.POST,instance=Work.objects.get(id=id))
    w=workform.save(commit=False)
    try:
        for changed in workform.changed_data:
                if changed == 'genre':
                    genres=workform.cleaned_data['genre']
                    for g in genres:
                        Genre_Work(work=w,genre=g).save()
    except MultiValueDictKeyError:
            pass
    w.save()
    return HttpResponseRedirect("/ocve/workadmin/"+id+"/")

@csrf_exempt
def saveworkinformation(request,id):
    wi=WorkInformation.objects.get(id=id)
    workinfoform=WorkInformationForm(request.POST,instance=wi)
    workinfoform.save()
    w = Work.objects.get(workinformation=wi)
    return HttpResponseRedirect("/ocve/workadmin/"+str(w.id)+"/")

@csrf_exempt
def saveworkcomponents(request,id):
    compFormset=WorkComponentFormset(request.POST)
    compFormset.save()
    return HttpResponseRedirect("/ocve/workadmin/"+str(id)+"/")

#Serialize all deepzoom previews as thumbnail images for browsing
def generateAllThumbnails(request):
    log=generateThumbnails(Source.objects.filter(Q(ocve=1)|Q(cfeo=1)))
    return HttpResponse(log)



