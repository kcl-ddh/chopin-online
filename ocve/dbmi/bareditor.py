__author__ = 'Elliott Hall'

import json
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response

from ocve.forms import *
from ocve.imagetools import verifyImageDimensions
from ocve.bartools import *
from datatools import *




#Error reporting template
errorPage = '500.html'
UPLOAD_EXTENSION = settings.UPLOAD_EXTENSION
STATIC_URL = settings.STATIC_URL

editBarsURL = '/ocve/editbars/'

def editBars(request, id):
    regionURL = "/ocve/getBarRegions/" + str(id) + "/"
    zoomifyURL = "https://" + IIP_URL + "?zoomify="
    p = None
    regionString = ''
    editStatuses = EditStatus.objects.all()
    try:
        pi = PageImage.objects.get(id=id)
        p = pi.page
        pl = PageLegacy.objects.get(pageimage=pi)

        #Redirect to the crop correct view if uncorrected before displaying editor
        if pl.cropCorrected == 0:
            return cropCorrectView(request, id)
        if pl.cfeoKey > 0:
            path = re.search("(.*?)_(.*)", pl.filename)
            oldPath = "jp2/cfeojp2-proc/" + path.group(1) + "/" + path.group(1) + "_" + path.group(2) + ".jp2"
            verifyImageDimensions(pi, oldPath)
            zoomifyURL = zoomifyURL +  oldPath + "/"
        elif pl.jp2 is not None and pl.jp2.__len__() > 0 and pl.jp2 != 'UNVERIFIED':
            #Correct system on which all legacy naming files will be moved
            path=pl.jp2
            if str(path).startswith("jp2")is False:
                path="jp2/"+path
            verifyImageDimensions(pi, path)
            zoomifyURL = zoomifyURL.replace("jp2/","") + pl.jp2 + "/"
        elif pl.storageStructure is not None and pl.storageStructure.__len__() > 0:
            path = re.search("(\d+)\/.*?\/(.*)", pl.storageStructure)
            sl = SourceLegacy.objects.get(source=p.sourcecomponent.source)
            oldPath = "jp2/ocvejp2-proc/" + path.group(1) + "/" + str(sl.witnessKey) + "/" + path.group(2) + ".jp2"
            verifyImageDimensions(pi, oldPath)
            zoomifyURL = zoomifyURL + oldPath + "/"
        zoomifyURL = pi.getZoomifyPath()

        #String of all bar numbers on page
        regions = barRegionsByPageImage(int(id))
        dels= BarRegion.objects.filter(pageimage__id=int(id)).filter(Q(y__lt=0) | Q(x__lt=0)|Q(width__lt=0)| Q(height__lt=0))
        dels.delete()
        for r in regions:
            label=''
            bars=r.bar.all()
            if bars.count() >0:
                bid=bars[0].id
                for b in bars:
                    if len(label)>0:
                        label+=', '
                    label+=b.barlabel
                regionString = regionString +'<span data-regionid=\"'+str(r.id)+'\">'+ label + '</span>, '

                #Next and previous page images
        try:
            before = p.orderno - 1
            prev = PageImage.objects.get(page__orderno=before, page__sourcecomponent=p.sourcecomponent)
        except ObjectDoesNotExist:
            prev = None
        try:
            after = p.orderno + 1
            next = PageImage.objects.get(page__orderno=after, page__sourcecomponent=p.sourcecomponent)
        except ObjectDoesNotExist:
            next = None
    except ObjectDoesNotExist:
        errormsg = 'Page key invalid'
        return render_to_response(errorPage, {'errormsg': errormsg})
    return render_to_response('bareditor.html',
            {'mode': 0, 'statuses': editStatuses, 'next': next, 'prev': prev, 'regionString': regionString,
         'regionURL': regionURL, 'pageimage': pi, 'page': p,'STATIC_URL': STATIC_URL,
         'zoomifyURL': zoomifyURL}, context_instance=RequestContext(request))

def cropCorrectView(request, id):
    regionURL = "/ocve/getGroupedBarRegions/" + id + "/"
    zoomifyURL = IIP_URL + "?zoomify=jp2/"
    p = None
    try:
        pi = PageImage.objects.get(id=id)
        p = pi.page
        pl = PageLegacy.objects.get(pageimage=pi)
        if pl.cfeoKey > 0:
            path = re.search("(.*?)_(.*)", pl.filename)
            oldPath = "jp2/cfeojp2-proc/" + path.group(1) + "/" + path.group(1) + "_" + path.group(2) + ".jp2"
            verifyImageDimensions(pi, oldPath)
            zoomifyURL = zoomifyURL +  oldPath + "/"
        elif pl.jp2 is not None and pl.jp2.__len__() > 0 and pl.jp2 != 'UNVERIFIED':
            #Correct system on which all legacy naming files will be moved
            path=pl.jp2
            if str(path).startswith("jp2")is False:
                path="jp2/"+path
            verifyImageDimensions(pi, path)
            zoomifyURL = zoomifyURL.replace("jp2/","") + pl.jp2 + "/"
        elif pl.storageStructure is not None and pl.storageStructure.__len__() > 0:
            path = re.search("(\d+)\/.*?\/(.*)", pl.storageStructure)
            sl = SourceLegacy.objects.get(source=p.sourcecomponent.source)
            oldPath = "jp2/ocvejp2-proc/" + path.group(1) + "/" + str(sl.witnessKey) + "/" + path.group(2) + ".jp2"
            verifyImageDimensions(pi, oldPath)
            zoomifyURL = zoomifyURL + oldPath + "/"
        zoomifyURL = pi.getZoomifyPath()

        #u'http://ocve2.cch.kcl.ac.uk/iip/iipsrv.fcgi?QLT=100&zoomify=jp2/ocvejp2-proc/38/15/05/38-1-W_GBOb_p05.jp2/'
        #20/20-1-BH_GBLbl_H471p4/09/20-1-BH_GBLbl_p09
    except ObjectDoesNotExist:
        errormsg = 'Page key invalid'
        return render_to_response(errorPage, {'errormsg': errormsg})
    return render_to_response('bareditor.html',
        {'mode': 1, 'regionURL': regionURL, 'pageimage': pi, 'page': p, 'zoomifyURL': zoomifyURL},
        context_instance=RequestContext(request))

def no_letters(number):
    return int(re.sub('[a-z|A-Z]*','',str( number) ))


#An automatic reordering of the bars on a page using y, then x coordinates
def reorderBarNumbers(request):
    id = int(request.POST['pageid'])
    pi = PageImage.objects.get(id=id)
    regions = BarRegion.objects.filter(pageimage=pi).order_by('y', 'x')
    barNum = int(re.sub('[a-z|A-Z]*','',pi.startbar))
    barLabel=pi.startbar
    for r in regions:
        #If normal bar assign and increment the number.  Leave anomalies alone
        if r.anomaly == 0:
            #clear region's links to bar numbers
            links = Bar_BarRegion.objects.filter(barregion=r)
            for l in links:
                l.delete()
            try:
                b = Bar.objects.get(barnumber=barNum, barlabel__iexact=str(barLabel))
            except ObjectDoesNotExist:
                b=Bar(barnumber=barNum, barlabel=barLabel)
                b.save()
            Bar_BarRegion(bar=b, barregion=r).save()
            barNum += 1
            #Special case in case last bar has letters
            if barNum==int(re.sub('[a-z|A-Z]*','',pi.endbar)) and re.match('[a-z|A-Z]+',str(barNum)) is not None:
                barLabel=pi.endbar
            else:
                barLabel=barNum
        else:
            #Anomalous bar, advance to highest bar number
            barNum = int(r.getHighestBarNumber()) + 1
            barLabel=barNum
            #return editBars(request, id)
    return HttpResponseRedirect(editBarsURL + str(id) + "/")



#Change the bar region's number
def updateBarNumber(request):
    id = request.POST['id']
    numbers = request.POST['barNumber']
    br = BarRegion.objects.get(id=int(id))
    pageimageid=br.pageimage.id
    try:
        #Manual bar delete for invisible bars
        if request.POST['Delete']:
            br.delete()
    except MultiValueDictKeyError:
        #Repeat bar, or other anomalous bar numbering?
        anomaly = 0
        try:
            anomaly = request.POST['anomaly']
        except MultiValueDictKeyError:
            pass

        #clear region's links to bar numbers
        links = Bar_BarRegion.objects.filter(barregion=br)
        for l in links:
            l.delete()
            #Split on commas in case multiple bars
        for number in numbers.split(","):
            number = number.strip(' ')
            bars = Bar.objects.filter(barlabel=number)
            if bars.__len__() > 0:
                for b in bars:
                    #br.bar_barregion_set.create(bar=b,barregion=br)
                    barlink = Bar_BarRegion(bar=b, barregion=br)
                    barlink.save()
            else:
                m = re.search("(\d+)", number)
                if m is not None:
                    num = m.group(1)
                    b = Bar(barlabel=number, barnumber=int(num))
                    b.save()
                    barlink = Bar_BarRegion(bar=b, barregion=br)
                    barlink.save()
                    #Force anomaly if multiple numbers assigned, in case user forgets
        if re.search("(\D+)", numbers) is not None:
            anomaly = 1
        br.anomaly = anomaly
        br.save()
    #return editBars(request, br.pageimage.id)
    return HttpResponseRedirect(editBarsURL + str(pageimageid) + "/")

#Updates bar regions POSTed as JSON
def updateBarRegion(request):
    regions = request.POST['regions']
    try:
        #Delete region
        delete = request.POST['delete']
        f = json.loads(regions)
        deleteID = f['properties']['id']
        br = BarRegion.objects.get(id=int(deleteID))
        br.delete()
        return HttpResponse("{\"message\":\"Region deleted\",\"id\":" + str(deleteID) + "}",
            content_type="application/json")
    except MultiValueDictKeyError:
        pass
    try:
        #Insert new region
        insert = request.POST['insert']
        pageImageID = request.POST['pageID']
        pi = PageImage.objects.get(id=int(pageImageID))
        b = Bar.objects.get(id=1)
        br = BarRegion(pageimage=pi, page=pi.page)
        updateBarRegionFromFeature(br, json.loads(regions))
        Bar_BarRegion(bar=b, barregion=br).save()
        return HttpResponse("{\"message\":\"Region added\",\"id\":" + str(br.id) + "}", content_type="application/json")
    except MultiValueDictKeyError:
        pass
        #Update all regions
    features = json.loads(regions)['features']
    for f in features:
        try:
            id = f['properties']['id']
        except MultiValueDictKeyError:
            id = -1
        except KeyError:
            id = 0
        if id > 0:
            br = BarRegion.objects.get(id=int(id))
            updateBarRegionFromFeature(br, f)
        elif id == 0:
            #Insert
            #"insert":1,"pageID":pageID
            pageImageID = request.POST['pageID']
            pi = PageImage.objects.get(id=int(pageImageID))
            b = Bar.objects.get(id=1)
            br = BarRegion(pageimage=pi)
            updateBarRegionFromFeature(br, f)
            Bar_BarRegion(barregion=br, bar=b).save()
    return HttpResponse("{\"message\":\"Regions updated\",\"id\":0}", content_type="application/json")