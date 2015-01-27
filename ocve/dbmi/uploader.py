__author__ = 'Elliot'
import os
import logging

from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from ocve.bartools import *
from django.conf import settings as s


logger = logging.getLogger('ocve.uploader')

def fix(request):
    np=NewPageImage.objects.filter(id__gt=5079)
    cphtml=''
    for n in np:
        cp='cp "/vol/ocve2/images/temp/'+n.filename+'" "/vol/ocve2/images/jp2/newjp2/'+str(n.id)+'.jp2"'
        cphtml=cphtml+cp+'\n'
        os.system(cp)
    return HttpResponse(cphtml)

#Show newly uploaded files taht have not been made into sources yet
def newsourcefiles(request):
    uploadPath=s.CONVERTED_UPLOAD_PATH
    uF=os.listdir(uploadPath)
    uploadFolder={}
    for u in uF:
        if os.path.isdir(uploadPath+'/'+u):
            uploadFolder[str(u)]=os.listdir(uploadPath+'/'+u)
        else:
            uploadFolder[str(u)]=None
    sources=Source.objects.order_by('sourceinformation__accode__accode').all()
    return render_to_response('uploadfolders.html', {'uploadFolder': uploadFolder,'sources':sources },
        context_instance=RequestContext(request))

#Convert an entire folder in the new upload area to a new source, then pass to the editor
def convertFolder(request,folderName):
    newS=NewSource(label=folderName,sourcecreated=0)
    newS.save()
    files=os.listdir(s.CONVERTED_UPLOAD_PATH+'/'+folderName)
    for f in files:
        npi = NewPageImage(source=newS, filename=f, surrogate=1, versionnumber=1, permission=False,
                        permissionnote='', height=0, width=0, startbar=0, endbar=0, corrected=0)
        npi.save()
        logger.debug('Copied '+s.CONVERTED_UPLOAD_PATH+'/'+f+' '+s.NEWJP2_UPLOAD_PATH+'/'+str(npi.id)+'.jp2')
        os.system('cp "'+s.CONVERTED_UPLOAD_PATH+'/'+folderName+'/'+f+' '+s.NEWJP2_UPLOAD_PATH+'/'+str(npi.id)+'.jp2"')
    return HttpResponseRedirect('/ocve/sourceeditor/new/' + str(newS.id))



#Convert a single image to a page in an existing source, pass to the editor for identification
def convertimage(request):
    source_key=int(request.POST['source_key'])
    source_id=int(request.POST['source_id'])
    try:
        imageNames=request.POST['imageName']
        folderName=None
    except MultiValueDictKeyError:
        folderName=request.POST['folderName']
        imageNames=os.listdir(s.CONVERTED_UPLOAD_PATH+'/'+folderName)
    s=None
    if source_key > 0:
        s=Source.objects.get(id=source_key)
    elif source_id > 0:
        s=Source.objects.get(id=source_id)
    if s is not None:
        try:
            newS=NewSource.objects.get(sourcecreated=s.id)
        except:
            newS=NewSource(sourcecreated=s.id)
            newS.save()
        if folderName is not None:
            for image in imageNames:
                image=folderName.encode('UTF-8')+'/'+image
                copytonewpageimage(newS,image)
        elif imageNames is not None:
           copytonewpageimage(newS,imageNames)

    return HttpResponseRedirect('/ocve/sourceeditor/' + str(s.id))

def copytonewpageimage(newS,image):
    fullurl = s.IMAGE_SERVER_URL + '?FIF='+s.CONVERTED_UPLOAD_PATH+'/'+image
    dimensions = imagetools.getImageDimensions(fullurl)
    npi = NewPageImage(source=newS, filename=image, surrogate=1, versionnumber=1, permission=False,
                         permissionnote='', height=dimensions['height'], width=dimensions['width'], startbar=0, endbar=0, corrected=0)
    npi.save()
    try:
        result= os.system('cp "'+s.CONVERTED_UPLOAD_PATH+'/'+image+'" "'+s.NEWJP2_UPLOAD_PATH+'/'+str(npi.id)+'.jp2"')
        if result !=0:
            logger.error(result)
    except OSError:
        logger.error(OSError)
    else:
        logger.debug('Copied '+s.CONVERTED_UPLOAD_PATH+'/'+image+'" "'+s.NEWJP2_UPLOAD_PATH+'/'+str(npi.id)+'.jp2"')



def posth(request):
    #sources=Source.objects.filter(sourceinformation__accode__accode__contains='PolG').distinct()
    sources=Source.objects.filter(id=18194).distinct()
    #s=Source.objects.get(id=18513).delete()
    w=Work.objects.get(id=6421)
    wc=w.workcomponent_set.all()
    nonmusic=SourceComponentType.objects.get(id=1473)
    nonumber=Opus.objects.get(id=1)
    x=1
#    for s in sources:
#        sc=s.getSourceComponents()
#        #WorkComponent(orderno=x,label=sc.label,work=w,opus=nonumber).save()
#        if SourceComponent.objects.filter(source=s,sourcecomponent_workcomponent__workcomponent__work=w).count() ==0:
#            comp=SourceComponent.objects.get(source=s,label__iexact='No 3')
#            comp.orderno=2
#            comp.save()
#            scwc=SourceComponent_WorkComponent.objects.get(sourcecomponent=comp)
#            scwc.workcomponent=wc[0]
#            scwc.save()
#            if SourceComponent.objects.filter(source=s,label__iexact='Front Matter').count()==0:
#                SourceComponent(source=s,orderno=1,label='Front Matter',sourcecomponenttype=nonmusic).save()
#            if SourceComponent.objects.filter(source=s,label__iexact='End Matter').count()==0:
#                SourceComponent(source=s,orderno=3,label='End Matter',sourcecomponenttype=nonmusic).save()
    posths=Work.objects.filter(orderno__gt=80,orderno__lt=1001)
    for p in posths:
        if p.workcomponent_set.all().count() ==0:
            WorkComponent(orderno=1,label='Score',work=p,opus=nonumber).save()
    return render_to_response('posth.html',
        {'posths': posths },
        context_instance=RequestContext(request))
