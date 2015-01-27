__author__ = 'Elliott Hall'
#Functions and views for the specialised OCVE Source editor

from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response

from django.utils.safestring import mark_safe
from django.template.defaultfilters import register

from ocve.forms import *
from ocve.bartools import *
from datatools import *

@register.filter()
def nbsp(value):
    return mark_safe(" ".join(value.split('&nbsp;')))


#New source that is being filled with metadata
def newsourceeditor(request, id=0):
    label = ''
    st = SourceType.objects.get(id=1)
    newS=None
    sourceInformation=None
    source=None
    try:
        newS = NewSource.objects.get(id=id)
        label = newS.library
    except ObjectDoesNotExist:
        pass
    if newS.sourcecreated > 0:
        source=Source.objects.get(id=newS.sourcecreated)
        sourceInformation = SourceInformation.objects.get(source=source)
        #dd=newS.sourcecreated
        #newsource=NewSource.objects.get(sourcecreated=1)
    else:
        source = Source.objects.create(sourcetype=st, label=label)
        source.save()
        sourcelegacy = SourceLegacy(source=source, cfeoKey=0, witnessKey=0, sourceDesc='', editstatus=EditStatus.objects.get(id=2), mellon=0, needsBarLines=1)
        sourcelegacy.save()
        sourceInformation = SourceInformation(source=source)
        sourceInformation.sourcecode = newS.sourcecode
        newS.sourcecreated=source.id
        newS.save()


    accode = None
    pages = None
    wComps = None
    newpages=None
    if newS is not None:
        newpages = NewPageImage.objects.filter(source=newS)
    try:
        accode = AcCode.objects.get(accode=newS.sourcecode)
    except ObjectDoesNotExist:
        accode = AcCode.objects.create(accode=newS.sourcecode)
        accode.save()
    if accode is not None:
        sourceInformation.accode = accode
        sourceInformation.save()

        #Use the AcCode to determine Source's opus
        #Temporarily disabled and made manual
        # m=re.search('(\d+)',accode.accode)
        # if m is not None:
        #     opusNo=int(m.group(1))
        #     try:
        #         opus=Opus.objects.get(opusno=opusNo)
        #         w=Work.objects.filter(workcomponent__opus=opus)[0]
        #         if w is not None:
        #             createDefaultComponents(source,w)
        #             wComps=WorkComponent.objects.filter(work=w)
        #     except ObjectDoesNotExist:
        #         #No action for now
        #         pass

    return sourceeditor(request,source,sourceInformation,newpages, wComps)

#Link the new source to the relevant work, and generate source compoennts
#if work has things like movements
def createDefaultComponents(source,w):
    wComps=WorkComponent.objects.filter(work=w)
    if wComps.count() == 0:
        #Create default work component for new empty work
        WorkComponent(work=w,orderno=1,label="Score",music=1,keymode=keyMode.objects.get(id=1),keypitch=keyPitch.objects.get(id=1),opus=Opus.objects.get(id=1)).save()
        wComps=WorkComponent.objects.filter(work=w)
    #Defaults for new source component
    piano=Instrument.objects.get(instrument='Piano')
    pianoScore=SourceComponentType.objects.get(type='Piano Score')
    orderno=1
    newsourcecomponent=None
    for wc in wComps:
        #Create a new source component for each work component
        if SourceComponent.objects.filter(sourcecomponent_workcomponent__workcomponent=wc,source=source).count() ==0:
            sc=SourceComponent.objects.create(sourcecomponenttype=pianoScore,source=source,orderno=orderno,label=wc.label,instrumentnumber=1)
            #Attach
            SourceComponent_WorkComponent.objects.create(sourcecomponent=sc,workcomponent=wc)
            SourceComponent_Instrument.objects.create(sourcecomponent=sc,instrument=piano)
            newsourcecomponent=sc
        else:
            newsourcecomponent=SourceComponent.objects.filter(sourcecomponent_workcomponent__workcomponent=wc,source=source)[0]
    return newsourcecomponent


#Editing a source that already exists
def existingsourceeditor(request, id):
    try:
        source=Source.objects.get(id=id)
        sourceInformation = SourceInformation.objects.get(source=source)
        #pages = PageImage.objects.filter(page__sourcecomponent__source=source).order_by('page__orderno')
        workcomponents=WorkComponent.objects.filter(sourcecomponent_workcomponent__sourcecomponent__source=source).distinct()
        #Added in case new pages have been uploaded to this existing source
        try:
            newpageimages=NewPageImage.objects.filter(source=NewSource.objects.get(sourcecreated=source.id),linked=0)
        except ObjectDoesNotExist:
            newpageimages=None
        return sourceeditor(request,source,sourceInformation,newpageimages,workcomponents)
    except ObjectDoesNotExist:
        #standard error page?
        return HttpResponse("ERROR in existingsourceeditor")


#The DBMi editor view for altering source structure
#This view is used for new and existing sources
def sourceeditor(request,source,sourceInformation,newpageimages,workcomponents):
    sourceForm = SourceForm(instance=source)
    sourceInformationForm = SourceInformationForm(instance=sourceInformation)
    scForm = SourceComponentForm()
    pageimages = PageImage.objects.filter(page__sourcecomponent__source=source).order_by('page__orderno')
    instruments = Instrument.objects.all()
    sourcecomponents=SourceComponent.objects.filter(source=source).order_by('orderno')
    works = Work.objects.all()
    opus = source.getOpusLabel()
    sources=Source.objects.all()
    return render_to_response('dbmi/sourceeditor.html',
        {'works':works,'instruments': instruments, 'scForm': scForm, 'pageimages': pageimages,'newpageimages': newpageimages,'workcomponents':workcomponents,'sourcecomponents': sourcecomponents ,'sourceForm': sourceForm,
            'sourceInformationForm': sourceInformationForm, 'opus': opus, 'IMAGE_SERVER_URL': settings.IMAGE_SERVER_URL,},
        context_instance=RequestContext(request))

def editsourcecomponent(request,id):
    sc=SourceComponent.objects.get(id=id)
    source=sc.source
    work=source.getWork()
    workcomponents=WorkComponent.objects.filter(work=work)
    currentwc=None
    comps=WorkComponent.objects.filter(sourcecomponent_workcomponent__sourcecomponent=sc)
    if comps.count() > 0:
        currentwc=comps[0]
    scf=SourceComponentForm(instance=sc)
    curinstrument=None
    if Instrument.objects.filter(sourcecomponent=sc).count() > 0:
        curinstrument=Instrument.objects.filter(sourcecomponent=sc)[0]
    instruments=Instrument.objects.filter(id__gt=2)
    #If changed
        #return existingsourceeditor(request, id)
    return render_to_response('dbmi/sourcecomponent.html',{'sc':sc,'scf':scf,'workcomponents':workcomponents,'currentwc':currentwc,'instruments':instruments,'curinstrument':curinstrument})

def deletesourcecomponent(request,id):
    sc=SourceComponent.objects.get(id=id)
    sourceid=sc.source.id
    if PageImage.objects.filter(page__sourcecomponent=sc).count() == 0:
        sc.delete()
    return existingsourceeditor(request, sourceid)

def savesourcecomponent(request,id):
    scform=SourceComponentForm(request.POST,instance=SourceComponent.objects.get(id=id))
    sc=scform.save()
    try:
        wcid=request.POST["id_workcomponent"]
        wc=WorkComponent.objects.get(id=wcid)
        scwc=SourceComponent_WorkComponent.objects.filter(sourcecomponent=sc)
        if scwc.count() > 0:
            link=scwc[0]
            link.workcomponent=wc
            link.save()
        elif wcid > 1:
            SourceComponent_WorkComponent(sourcecomponent=sc,workcomponent=wc).save()
    except MultiValueDictKeyError:
        pass
    try:
        iid=request.POST["id_instrument"]
        instrument=Instrument.objects.get(id=iid)
        scic=SourceComponent_Instrument.objects.filter(sourcecomponent=sc)
        if scic.count() > 0:
            link=scic[0]
            link.instrument=instrument
            link.save()
        else:
            SourceComponent_Instrument(sourcecomponent=sc,instrument=instrument).save()
    except MultiValueDictKeyError:
        pass
    return HttpResponse("Component Saved")


#Remove superflous html tags added by TinyMCE
def cleanHTML(label):
    label=label.replace('<p>','').replace('<span>','').replace('</span>','')
    label=label.replace('</p>','').replace('\r','').replace('\n','')
    label=label.replace('<div>','').replace('</div>','').replace('<br />','').replace("<p class=\"BodyAA\">","")
    return label




#Save new source
def saveSource(request,id):
    msg = ''
    #Populate source from request
    sourcef=SourceForm(request.POST,instance=Source.objects.get(id=id))
    source=sourcef.save()
    try:
        source.label=cleanHTML(source.label)
        source.cfeolabel=cleanHTML(source.cfeolabel)
    except MultiValueDictKeyError:
        pass
    source.save()
    try:
        workid=int(request.POST["work_id"])
        w=Work.objects.get(id=workid)
        if source.getWork() != w:
            #New Modified source,
            #Get pages, if they exist (may be new source)
            oldWork=source.getWork()
            sourcePages=source.getPages()
            newsourcecomponent=createDefaultComponents(source,w)
            #Add pages to sourcecomponent corresponding to first work component
            if newsourcecomponent is not None:
                for sp in sourcePages:
                    #If this attached to opus e.g. not front matter
                    if SourceComponent_WorkComponent.objects.filter(sourcecomponent=sp.sourcecomponent).count() >0:
                        sp.sourcecomponent=newsourcecomponent
                        sp.save()
                #Delete old components
                oldcomponents=SourceComponent.objects.filter(source=source,sourcecomponent_workcomponent__workcomponent__work=oldWork).delete()


    except MultiValueDictKeyError:
        pass
    try:
        newsource=NewSource.objects.get(sourcecreated=id)
        sourcenewid=newsource.pk
        #return HttpResponseRedirect('/ocve/sourceeditor/new/' + str(newsource.pk) + '/#sourceMetadata')
        return newsourceeditor(request, newsource.pk)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/ocve/sourceeditor/' + str(id) + '/#sourceMetadata')



#New source information
def saveSourceInformation(request,id):
    #source=SourceForm(request.POST)
    sinfo=SourceInformationForm(request.POST,instance=SourceInformation.objects.get(id=id))
    #Check the form validates
    if len(sinfo.errors) > 0:
        return HttpResponse("<html><body><h1>Error saving source information</h1>"+str(sinfo.errors)+"</body></html>")
    else:
        sourceInformation=sinfo.save(commit=False)
        try:
            for changed in sinfo.changed_data:
                if changed == 'printingmethod':
                    methods=sinfo.cleaned_data['printingmethod']
                    for m in methods:
                        SourceInformation_PrintingMethod(sourceinformation=sourceInformation,printingmethod=m).save()
        except MultiValueDictKeyError:
            pass
        #Check if new authority list variables have been filled in, create and link as necessary
        try:
            newmethod=request.POST["newmethod"]
            if newmethod is not None and len(newmethod) >0:
                newm=PrintingMethod(method=newmethod)
                newm.save()
                SourceInformation_PrintingMethod(sourceinformation=sourceInformation,printingmethod=newm).save()
        except MultiValueDictKeyError:
            pass
        try:
            newarchive=request.POST["newarchive"]
            if newarchive is not None and len(newarchive)>0:
                newa=Archive(name=newarchive)
                newa.save()
                sourceInformation.archive=newa
        except MultiValueDictKeyError:
            pass
        try:
            newaccode=request.POST["newaccode"]
            if newaccode is not None and len(newaccode)>0:
                addAcCode(newaccode, sourceInformation)
        except MultiValueDictKeyError:
            pass
        #Extra widgets for adding formatting to dedicatee/publishers
        #and preserving dedicatee alternate spellings
        try:
            altDT=int(request.POST["altDedicateeType"])
            altPT=int(request.POST["altPublisherType"])
            if altDT is not None and altDT>0:
                altD=request.POST["altDedicatee"]
                if altDT == 1:
                    #New
                    d=Dedicatee(dedicatee=altD)
                    d.save()
                    sourceInformation.dedicatee=d
                    sourceInformation.save()
                if altDT == 2:
                    #Alternate
                    altDedicatee=Dedicatee(dedicatee=altD,alternateOf=sourceInformation.dedicatee)
                    altDedicatee.save()
                    sourceInformation.dedicatee=altDedicatee
                    sourceInformation.save()
                if altDT == 3:
                    #Overwrite
                    d=sourceInformation.dedicatee
                    d.dedicatee=altD
                    d.save()
            if altPT is not None and altPT>0:
                altP=request.POST["altPublisher"]
                if altPT == 1:
                    p=Publisher(publisher=altP)
                    p.save()
                    sourceInformation.publisher=p
                    sourceInformation.save()
                if altPT == 3:
                    p=sourceInformation.publisher
                    p.publisher=altP
                    p.save()
        except MultiValueDictKeyError:
            pass
        sourceInformation.save()
    source=sourceInformation.source
    #try:
    #    newsource=NewSource.objects.get(sourcecreated=source.id)
    #    sourcenewid=newsource.pk
    #    return HttpResponseRedirect('/ocve/sourceeditor/new/' + str(newsource.pk) + '/#sourceInformationMetadata')
    #except ObjectDoesNotExist:
    return HttpResponseRedirect('/ocve/sourceeditor/' + str(source.id) + '/#sourceInformationMetadata')




def createSourceComponent(request,id):
    componentlabel = nbsp(request.POST['componentlabel'])
    instrument_number=request.POST['instrumentnumber']
    id_sourcecomponenttype=request.POST['id_sourcecomponenttype']
    s = Source.objects.get(id=id)
    count =SourceComponent.objects.filter(source=s).count()
    id_workcomponent=request.POST['id_workcomponent']
    c = SourceComponentType.objects.get(id=id_sourcecomponenttype)
    newsourcecomponent = SourceComponent(source=s, orderno=count+1, label=componentlabel, instrumentnumber=instrument_number, sourcecomponenttype=c)
    newsourcecomponent.save()
    instrument_id=request.POST['instrument']
    if instrument_id <> 'None':
        i = Instrument.objects.get(id=instrument_id)
        ic =instrumentComponent(instrument=i, sourcecomponent = newsourcecomponent)
        ic.save()
    if id_workcomponent <> '0' :
        w = WorkComponent.objects.get(id=id_workcomponent)
        wcsc =SourceComponent_WorkComponent(workcomponent=w, sourcecomponent = newsourcecomponent)
        wcsc.save()

    msg = 'created '
    return HttpResponse(msg)

#Create or update a source component
def saveSourceComponent(request,id):
    msg = ''
    #If id is 0, create new, else instantiate
    #Front or end matter presets
        #else Populate/overwrite with form
    #Get all attached pages in order
    #Save pages with new order
    return HttpResponse(msg)

def updateComponentOrder(request):
    msg=''
    try:
        scString=request.POST['sckeys']
        scKeys=scString.split(",")
        x=1
        for sc in scKeys:
           key=sc.replace('sc ','')
           try:
                sourcecomponent=SourceComponent.objects.get(id=int(key))
                sourcecomponent.orderno=x
                sourcecomponent.save()
                x+=1
           except ObjectDoesNotExist:
                pass
    except MultiValueDictKeyError:
        pass
    return HttpResponse(msg)


def savePage(request):
    msg = request.POST['value']
    is_newpage=str(request.POST['is_newpage'])
    is_textlabel=str(request.POST['is_textlabel'])
    if is_textlabel == 'true':
        #Update the text label for a page
        spageimage = PageImage.objects.get(id=int(request.POST['id']))
        spageimage.textlabel=msg
        spageimage.save()
    #return HttpResponse(str(is_newpage))
    list1 = re.split('\W+', request.POST['idsc'])
    sc = SourceComponent.objects.get(id=int(list1[1]))
    sc.orderno = int(request.POST['numsc'])+1
    sc.save()
    #list2 = re.split(r'\W+', msg)
    list2 = re.findall(r"[\w\[\]]+",msg)
    pagenum=0
    startbar=0
    endbar=0
    if re.match('p\.*\s*(\S+)',msg):
        pagenum=re.search('p\.*\s*(\S+)',msg).group(1)
    if re.match('.*bs\.*\s*(\d+)-(\d+).*',msg):
        numbers=re.search('.*bs\.*\s*(\d+)-(\d+).*',msg)
        startbar=numbers.group(1)
        endbar=numbers.group(2)
    if is_newpage=='true':
        np = NewPageImage.objects.get(id=int(request.POST['id']))
        jp='newjp2/'+str(np.id)+'.jp2'
        if np.linked > 0: # the new page was already saved
            spageimage=PageImage.objects.get(id=np.linked);
            #saveBars(msg, spageimage)
            if startbar >0:
                spageimage.startbar=startbar
            if endbar > 0:
                spageimage.endbar=endbar
            spageimage.save()
            spage=Page.objects.get(id=spageimage.page.id)
            spage.label=pagenum
            spage.orderno=int(request.POST['idnum'])
            spage.sourcecomponent=sc
            spage.save()
        else:
            spage = Page(label=pagenum, orderno=int(request.POST['idnum']), sourcecomponent=sc)
            spage.save()
            spageimage=PageImage(page=spage, corrected = 0, height=np.height, width=np.width)
            if startbar >0:
                spageimage.startbar=startbar
            if endbar > 0:
                spageimage.endbar=endbar
            spageimage.save()
            pagelegacy=PageLegacy(pageimage=spageimage,jp2='newjp2/'+str(np.id)+'.jp2',editstatus=EditStatus.objects.get(id=2), cropCorrected=1)
            pagelegacy.save()
        np.linked=spageimage.id
        #saveBars(msg, np)
        np.startbar= startbar
        np.endbar = endbar
        np.save()
    else:
        spageimage = PageImage.objects.get(id=int(request.POST['id']))
        #saveBars(msg, spageimage)
        if startbar >0:
            spageimage.startbar=startbar
        if endbar >0:
            spageimage.endbar=endbar
        spageimage.save()
        spage=Page.objects.get(id=spageimage.page.id)
        if pagenum > 0:
            spage.label=pagenum
        spage.orderno=int(request.POST['idnum'])
        spage.sourcecomponent=sc
        spage.save()

    return HttpResponse(msg)

def updatepageindex(request):
    msg = request.POST['id']
    list1 = re.split('\W+', request.POST['idsc'])
    sc = SourceComponent.objects.get(id=int(list1[1]))
    sc.orderno = int(request.POST['numsc'])+1
    sc.save()
    is_newpage=str(request.POST['is_newpage'])
    if is_newpage=='true':
        np = NewPageImage.objects.get(id=int(request.POST['id']))
        if np.linked > 0: # the new page was already saved
            spageimage=PageImage.objects.get(id=np.linked)
            spage=Page.objects.get(id=spageimage.page.id)
            spage.orderno=int(request.POST['idnum']);
            spage.sourcecomponent=sc;
            spage.save()
        else:
            spage = Page(orderno=int(request.POST['idnum']), sourcecomponent=sc)
            spage.save()
            spageimage=PageImage(page=spage, startbar=0,endbar=0,corrected = 0, height=0, width=np.width)
            spageimage.save()
            pagelegacy=PageLegacy(pageimage=spageimage,jp2='newjp2/'+str(np.id)+'.jp2',editstatus=EditStatus.objects.get(id=2), cropCorrected=1)
            pagelegacy.save()
        np.linked=spageimage.id
        np.save()
    else:
        spageimage = PageImage.objects.get(id=int(request.POST['id']))
        spageimage.save();
        spage=Page.objects.get(id=spageimage.page.id)
        spage.orderno=int(request.POST['idnum']);
        spage.sourcecomponent=sc;
        spage.save();


    return HttpResponse(msg)

def deletepage(request,id):
    try:
        pi=PageImage.objects.get(id=id)
        sourceid=pi.page.sourcecomponent.source.id
        for pl in PageLegacy.objects.filter(pageimage=pi):
            pl.pageimage_id=0
            pl.save()
        pi.delete()
        return existingsourceeditor(request, sourceid)
    except ObjectDoesNotExist:
        return HttpResponse("Page with ID does not exist")
