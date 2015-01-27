import os
import subprocess
import shlex

from django.core.paginator import Paginator, EmptyPage, InvalidPage


__author__ = 'Elliott Hall'
#All view functions for editing bar information
from ocve.forms import *
from ocve.imagetools import verifyImageDimensions, verifyImagesViaIIP
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from ocve.bartools import *
from datatools import *
from bareditor import editBars,editBarsURL
from django.db.models import *
from uploader import *
from spine import *
from sourceeditor import *
import shutil

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

UPLOAD_EXTENSION = settings.UPLOAD_EXTENSION
STATIC_URL = settings.STATIC_URL

def fixrangeview(request):
    #log=fixBarRange()
    uploadOCVEOpus28()
    return HttpResponse(log)




@login_required
def selectSource(request):
    sForm = NewSourceForm()
    convert = lambda text: ('', int(text)) if text.isdigit() else (text, 0)
    newSources = sorted(NewSource.objects.all(), key=lambda a: [convert(c) for c in re.split('([0-9]+)', a.sourcecode)])
    return render_to_response('selectsource.html', {'newSourceForm': sForm, 'newSources': newSources},
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
    return render_to_response('selectsource.html', {'errormsg': errormsg, 'newSourceForm': s, 'newSources': newSources},
                              context_instance=RequestContext(request))


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
                    os.system('convert /vol/ocve2/images/upload/%s.tif -alpha Off /vol/ocve2/images/upload/%s.tif' % (
                    str(npi.id), str(npi.id)))
                    os.system('kdu_compress -i /vol/ocve2/images/upload/' + str(
                        npi.id) + '.tif -o /vol/ocve2/images/jp2/newjp2/' + str(
                        npi.id) + '.jp2 -rate -,4,2.34,1.36,0.797,0.466,0.272,0.159,0.0929,0.0543,0.0317,0.0185 Creversible=yes Clevels=5 Stiles=\{1024,1024\} Cblk=\{64,64\} Corder=RPCL Cmodes=BYPASS')
        except MultiValueDictKeyError:
            pass
    return HttpResponse("")


#Apply the offsets passed from editor tool to all regions on page
#signal that page has been corrected.
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
                                #                                if np.source.sourcecreated > 0:
                                #                                    source=Source.objects.get(id=np.source.sourcecreated)
                                #                                    sc=SourceComponent.objects.filter(source=source)
                                #                                    if sc[0] is not None:
                                #                                        spage=Page.objects.filter(sourcecomponent=sc[0])[0]
                                #                                        spageimage=PageImage(page=spage, startbar=0,endbar=0,corrected = 1, height=np.height, width=np.width)
                                #                                        spageimage.save()
                                #                                        newid=spageimage.id
                                #                                        pagelegacy=PageLegacy(pageimage=spageimage,jp2='jp2/newjp2/'+str(newid)+'.jp2',editstatus=EditStatus.objects.get(id=2), cropCorrected=1)
                                #                                        pagelegacy.save()
                                oldpath = '/vol/ocve2/images/jp2/newjp2/' + str(nid) + '.jp2'
                                newpath = '/vol/ocve2/images/jp2/newjp2/' + str(newid) + '.jp2'
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
    return render_to_response('correctview.html', {'source': source, 'pages': pages, 'statuses': sourceStatuses},
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

    return render_to_response('correctview.html',
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


#Sort the pages by their edit status, paginate and display
def editPageView(request):
    statuses = {}
    ps = PageImage.objects.filter(page__sourcecomponent__source__sourcelegacy__needsBarLines=1).order_by(
        'pagelegacy__editstatus', 'page__sourcecomponent__source', 'page__orderno').distinct()
    for s in EditStatus.objects.all():
        statuses[s] = ps.filter(pagelegacy__editstatus=s).count()
    filterId = 0
    #Default
    filter = EditStatus.objects.get(id=1)
    #See if filter is in the session
    try:
        filter = request.session.__getitem__('pageFilter')
    except KeyError:
        search = 0
    if request.method == 'POST':
        #Quicksearch, redirect to page
        try:
            pageimageId = int(request.POST['pageimageid'])
            try:
                p = PageImage.objects.get(id=pageimageId)
                return editBars(request, pageimageId)
            except ObjectDoesNotExist:
                message = 'ID Does not Exist'
            return render_to_response('editpages.html', {'message': message, 'statuses': statuses, 'filter': filter},
                                      context_instance=RequestContext(request))
        except ValueError:
            message = 'Please provide a number'
        except MultiValueDictKeyError:
            message = 'Bad Key'
            #filter pages based on edit status
        try:
            filterId = int(request.POST['filterStatus'])
        except MultiValueDictKeyError:
            pass
    if filterId > 0:
        filter = EditStatus.objects.get(id=filterId)
    request.session.__setitem__('pageFilter', filter)
    ps = PageImage.objects.filter(pagelegacy__editstatus=filter).filter(
        page__sourcecomponent__source__sourcelegacy__needsBarLines=1).order_by(
        'page__sourcecomponent__sourcecomponent_workcomponent__workcomponent__opus__opusno',
        'page__sourcecomponent__source', 'page__orderno')
    paginator = Paginator(ps, 100)
    page = request.GET.get('page')
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        # If page request (9999) is out of range, deliver last page of results.
    try:
        pages = paginator.page(page)
    except (EmptyPage, InvalidPage):
        pages = paginator.page(paginator.num_pages)
    return render_to_response('editpages.html', {'pages': pages, 'statuses': statuses, 'filter': filter},
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
        command = str("find /vol/ocve2/images/jp2 -iname " + u.filename + ".jp2")
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


def sourcesbywork(request):
    works = Work.objects.all()
    return render_to_response('sourcesbywork.html',
                              {'works': works, 'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL, },
                              context_instance=RequestContext(request))



