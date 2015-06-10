__author__ = 'Elliott Hall'

from xlwt import Workbook, easyxf
from xlrd import open_workbook
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ocve.models import *
from ocve.bartools import BarRegionThumbnail
from django.db import connections, transaction


# *** Spine Views ***
#Export Spines of a work to an Excel workbook for editing
def exportXLS(request,id):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    if int(id) == 0:
        #Posthumous case
        sources = Source.objects.filter(sourcecomponent__sourcecomponent_workcomponent__workcomponent__work__workcollection=3).order_by('sourcecomponent__sourcecomponent_workcomponent__workcomponent__work').distinct()
        response['Content-Disposition'] = 'attachment; filename="Posthumous_Spine.xls"'
        label='Posthumous Spines'
    else:
        work = Work.objects.get(id=id)
        sources = Source.objects.filter(sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work).distinct()
        response['Content-Disposition'] = 'attachment; filename="Spine'+str(work.id)+'.xls"'
        label=work.label+ ' Spines'
    #Create Workbook and single sheet for all spines
    book = Workbook(encoding='utf-8')
    label=label.replace('[','').replace(']','')
    if len(label) > 20:
        label=label[:20]+'...'
    sheet = book.add_sheet(label)

    #Different colour backgrounds to distinguish between movements in the workbook
    mvtFormats=[
        easyxf('font: color red;'),
        easyxf('font: color blue;'),
        easyxf('font: color green;'),
        easyxf('font: color gold;'),
        easyxf('font: color brown;'),
        ]
    sourceRow=sheet.row(0)
    codeRow=sheet.row(1)
    colIndex=0
    mvtIndexes=[]
    curMvts=[]
    #Write the first two rows, containing source keys and ac codes
    for s in sources:
        code=s.getAcCode()
        sourceRow.write(colIndex,str(s.id))
        codeRow.write(colIndex,code,)
        colIndex+=1
        mvtIndexes.append(0)
        curMvts.append(None)
        #Current source component

    i=2
    orderNo=1
    while 1:
        #Write single spine as xls row
        row=sheet.row(i)
        colIndex=0
        #Make sure we have at least one spine for this orderno
        spineFound=0
        for s in sources:
            page=" "
            bar=" "
            try:
                spines=BarSpine.objects.filter(orderNo=orderNo,source=s)
                if spines.count() > 0:
                    spine=spines[0]
                    if spines.count() > 1:
                        spines[1].delete()
                    spineFound=1
                    bar=spine.bar.barlabel
                    if spine.implied == 1:
                        bar=bar+'(I)'
                    if curMvts[colIndex] is None:
                        #Inital
                        curMvts[colIndex]=spine.sourcecomponent
                    elif curMvts[colIndex] != spine.sourcecomponent:
                        #New movement, change formatting
                        mvtIndexes[colIndex]+=1
                        if mvtIndexes[colIndex] >= len(mvtFormats):
                            #Back to first colour
                            mvtIndexes[colIndex]=0
                        curMvts[colIndex]=spine.sourcecomponent
            except ObjectDoesNotExist:
                bar=" "
                #row.append(page)
            if bar != " ":
                row.write(colIndex,bar,mvtFormats[mvtIndexes[colIndex]])
            else:
                row.write(colIndex,bar)

            colIndex+=1
            #No spines left, we're done
        if spineFound == 0:
            break
        i+=1
        orderNo+=1

    #Finish and write to stream
    book.save(response)
    return response

@csrf_exempt
def importXLS(request):
    workid=int(request.POST['workid'])
    work=Work.objects.get(id=workid)
    #response = HttpResponse(content_type='text/html')
    #response.write('<html><head></head><body>')
    result="File Uploaded"
    if request.method == 'POST':
        try:
            workid=int(request.POST['workid'])
            work=Work.objects.get(id=workid)
            #response.write('<h1>'+work.label+'</h1><table border=\"1\">')
            BarSpine.objects.filter(source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work).delete()
            #wb = open_workbook(request.FILES['uploadFile'])
            wb= open_workbook(file_contents=request.FILES['uploadFile'].read())
            sources=[]
            components=[]
            for s in wb.sheets():
                for row in range(s.nrows):
                    #response.write('<tr>')
                    for col in range(s.ncols):
                        if row == 0:
                            #Source keys
                            try:
                                source=Source.objects.get(id=int(s.cell(row,col).value))
                                sources.append(source)
                                if source.getFirstBarRegion() is not None:
                                    sc=source.getFirstBarRegion().pageimage.page.sourcecomponent
                                    components.append(sc)
                                else:
                                    components.append(0)
                            except ObjectDoesNotExist:
                                result+="Source "+ str(s.cell(row,col).value)+" not found, column ignored"
                            #response.write('<td>'+s.cell(row,col).value+'</td>')
                        elif row > 1:
                            value=str(s.cell(row,col).value)
                            #response.write('<td>'+value+'</td>')
                            try:
                                if len(value) > 0 and components[col] != 0:
                                    implied=0
                                    value=value.replace('.0','')
                                    if '(I)' in value:
                                        #Implied repeat, note and clean
                                        value=value.replace('(I)','')
                                        implied=1
                                    try:
                                        bars=Bar.objects.filter(barlabel__iexact=value)
                                        if bars.count() > 0:
                                            bar=bars[0]
                                        bs=BarSpine()
                                        bs.bar=bar
                                        bs.implied=implied
                                        orderNo=row-1
                                        bs.label=orderNo
                                        bs.orderNo=orderNo
                                        bs.source=sources[col]
                                        comp=None
                                        #Verify bar (needed for implied problems)
                                        if BarRegion.objects.filter(bar=bar,pageimage__page__sourcecomponent=components[col]).count() > 0:
                                            bs.sourcecomponent=components[col]
                                        else:
                                            #Bar actually belongs to earlier component.
                                            #Try Previous component
                                            prev=BarRegion.objects.filter(bar=bar,pageimage__page__sourcecomponent__orderno=sc.orderno-1,pageimage__page__sourcecomponent__source=sources[col])
                                            if prev.count() > 0:
                                                bs.sourcecomponent=prev[0].pageimage.page.sourcecomponent
                                        bs.save()
                                    except IndexError:
                                        col
                                    try:
                                         if BarRegion.objects.filter(pageimage__page__sourcecomponent=components[col]).count() == 0 or bar == BarRegion.objects.filter(pageimage__page__sourcecomponent=components[col]).order_by('pageimage__page__sourcecomponent__orderno','pageimage__page__orderno', 'bar').distinct().reverse()[:1][0].getHighestBar():
                                             #Last bar in component, Advance source component
                                             #if bs.implied == 1 and :
                                             #else:
                                                 comps=SourceComponent.objects.filter(source=sources[col])
                                                 next=0
                                                 for x,sc in enumerate(comps):
                                                     if next == 1:
                                                         components[col]=sc
                                                         break
                                                     if sc == components[col]:
                                                         next=1
                                    except IndexError:
                                        BarRegion.objects.filter(pageimage__page__sourcecomponent=components[col]).order_by('pageimage__page__sourcecomponent__orderno','pageimage__page__orderno', 'bar').distinct().reverse()[:1][0].getHighestBar()
                            except ObjectDoesNotExist:
                                skip=0
                                #response.write('</tr>')
                                #response.write('</table></body></html>')
        except ObjectDoesNotExist:
            result="Parse Error"
    return render_to_response('dbmi/importresult.html',
        {'result': result,'work':work})





#Creates a default spine for a source.
def generateSpine(source):
    regions = BarRegion.objects.filter(pageimage__page__sourcecomponent__source=source).order_by(
        'pageimage__page__sourcecomponent__orderno','pageimage__page__orderno', 'bar').distinct()
    x = 1
    for r in regions:
        for bar in r.bar.all():
            bs = BarSpine(label=x, orderNo=x, bar=bar, source=source,sourcecomponent=r.pageimage.page.sourcecomponent)
            bs.save()
            x += 1

#get a particular spine from a work
def getSpinesByWork(work, orderNo,range=1):
    #if range > 1:
    #    spines = BarSpine.objects.filter(orderNo__range=(orderNo,orderNo+range),source__ocve=1,source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work).order_by('ocve_barSpine.source_id').distinct()
    #else:
    spines = BarSpine.objects.filter(orderNo=orderNo,source__ocve=1,source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=work).distinct()
    return spines

#Remove the bar spines for a source and then rebuild from default
def deleteSourceSpines(request,id):
    try:
        s=Source.objects.get(id=id)
        BarSpine.objects.filter(source=s).delete()
        generateSpine(s)
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect('/ocve/editspine/' + str(s.getWork().id))


def spinesToRegionThumbs(spines,range=1):
    regions = []
    for spine in spines:
        barregions = BarRegion.objects.filter(bar=spine.bar,pageimage__page__sourcecomponent=spine.sourcecomponent).distinct()
        for r in barregions:
            if range > 1:
                extent=spine.orderNo+range-1
                rangespines=BarRegion.objects.filter(bar__barspine__orderNo__range=(spine.orderNo,extent),bar__barspine__source=spine.source,pageimage__page__sourcecomponent=spine.sourcecomponent).order_by('bar__barspine__orderNo').distinct()
                b = BarRegionThumbnail(r, r.pageimage.page, r.pageimage,rangespines)
            else:
                b = BarRegionThumbnail(r, r.pageimage.page, r.pageimage)
            regions.append(b)
    return regions

#Show a particular spine from a work
def spine(request):
    orderNo = int(request.GET['orderNo'])
    prev = orderNo - 1
    next = orderNo + 1
    if str(request.GET['work_id']) == 'posthumous':
        #Special case for posthumous works
        spines = BarSpine.objects.filter(orderNo=orderNo,source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work__workcollection__id=3).distinct()
        work=None
    else:
        work = Work.objects.get(id=int(request.GET['work_id']))
        #Get relevant spines from work
        barSpines=getSpinesByWork(work, orderNo,1)
        #Arrange bar spines into groups based on source
        spines=sorted(barSpines, key=lambda sp: sp.source.orderno)
    #Get bar regions
    regions=spinesToRegionThumbs(spines)
    return render_to_response('dbmi/showspine.html',
        {'work': work, 'orderNo': orderNo, 'prev': prev, 'next': next, 'regions': regions,
         'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL},
        context_instance=RequestContext(request))




def worksforspine(request):
    works = Work.objects.all()
    return render_to_response('dbmi/workspines.html', {'works': works},
        context_instance=RequestContext(request))

def workspine(request, id):
    w = Work.objects.get(id=id)
    newWork=0
    #BarSpine.objects.filter(source__sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=w).delete()
    sources = Source.objects.filter(sourcecomponent__sourcecomponent_workcomponent__workcomponent__work=w).order_by('orderno').distinct()
    #No spines at all for this for this work, generate
    #for s in sources:
        #if BarSpine.objects.filter(source=s).count() == 0:
            #generateSpine(s)
    return spineeditor(request,w,sources)

def spineeditor(request,work,sources):
    spines = {}
    mvtColours=['red','blue','green','gold','brown']
    mvts={}
    mvtIndex={}
    cursor = connections['ocve_db'].cursor()
    if work is not None:
        workid=str(work.id)
    else:
        workid='posthumous'

    sourceKeys=[]
    sourceKeyString=''

    #cursor.execute("SELECT s.id FROM ocve_source as s, ocve_sourcecomponent as sc, ocve_sourcecomponent_workcomponent as scwc, ocve_workcomponent as wc where s.id=sc.source_id and sc.id=scwc.sourcecomponent_id and scwc.workcomponent_id=wc.id and wc.work_id="+str(work.id));
    #for row in cursor.fetchall():
    for s in sources:
        sourceKeys.append(s.id)
        if len(sourceKeyString) >0:
            sourceKeyString+=","
        sourceKeyString+=str(s.id)
        spines[str(s.id)]={}
    tbody = ''
    i=1
    rowCounter=1
    spineSQL="SELECT bs.id,b.barlabel,bs.bar_id,bs.orderNo,bs.source_id,bs.sourcecomponent_id,bs.implied FROM ocve_barspine as bs,ocve_bar as b where bs.bar_id=b.id and source_id in ("+sourceKeyString+") order by source_id,bs.sourcecomponent_id,orderNo;"
    cursor.execute(spineSQL)
    for row in cursor.fetchall():
        spineid=row[0]
        barlabel=row[1]
        bar_id=row[2]
        orderno=row[3]
        sourceid=row[4]
        sourcecomponentid=row[5]
        implied=row[6]
        spine={'implied':implied,'barlabel':barlabel,'sourcecomponentid':sourcecomponentid}
        try:
            if mvts[sourceid] is None:
                mvts[sourceid]=sourcecomponentid
        except KeyError:
            mvts[sourceid]=sourcecomponentid
        mvtIndex[sourceid]=0
        spines[str(sourceid)][str(orderno)]=(spine)

    while 1:
        spineFound=0
        tbody += '<tr>\n<td><a href="/ocve/spine?work_id=' + workid + '&orderNo=' + str(i) + '">' + str(
            i) + '</a></td>'
        for s in sources:
            try:
                #spine=BarSpine.objects.get(orderNo=i, source=s)
                spine=spines[str(s.id)][str(i)]
                if spine['sourcecomponentid'] != mvts[s.id]:
                    mvts[s.id]=spine['sourcecomponentid']
                    mvtIndex[s.id]+=1
                    if mvtIndex[s.id] >= len(mvtColours):
                        mvtIndex[s.id]=0
                tbody += '<td class='+mvtColours[mvtIndex[s.id]]+'>' + spine['barlabel']
                if spine['implied'] == 1:
                    tbody+= '(I)'
                tbody+= '</td>'
                spineFound=1
            except KeyError:
                tbody += '<td>&nbsp;</td>'
            except IndexError:
                tbody += '<td>&nbsp;</td>'
        tbody += '</tr>\n'
        i+=1
        if spineFound == 0:
            break
    return render_to_response('dbmi/editspine.html',
        {'work': work, 'sources': sources, 'tbody': tbody},
        context_instance=RequestContext(request))

#Special view for posthumous spines
def posthumousSpines(request):
    sources=Source.objects.filter(sourcecomponent__sourcecomponent_workcomponent__workcomponent__work__workcollection=3).order_by('sourcecomponent__sourcecomponent_workcomponent__workcomponent__work').distinct()
    w=Work.objects.get(id=6397)
    return spineeditor(request,None,sources)
