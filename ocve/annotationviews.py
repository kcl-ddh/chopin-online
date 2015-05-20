from django.template import RequestContext
from ocve.forms import AnnotationForm
from ocve.models import PageImage, Annotation
from ocve.models_generic import AnnotationType

__author__ = 'Elliot'
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext

from bartools import toGeos
from ocve.models import Annotation_BarRegion,Bar,BarRegion
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


#Note edit views

OP_INSERT = 1
OP_UPDATE = 2
OP_DELETE = 3

#Mini wrapper class for geojson
class noteGeos:
    def __init__(self, annotation):
        self.annotation=annotation
        self.barregions=annotation.getBarRegions()
        if self.barregions.count() > 0:
            self.geos=toGeos(self.barregions)
        else:
            self.geos=[]

#Delete user annotation
@csrf_exempt
@login_required
def deleteNote(request,id):
    try:
        Annotation.objects.get(id=id).delete()
    except:
        pass
    return HttpResponse("Deleted")


#Takes an annotation form and updates
@csrf_exempt
@login_required
def saveNote(request):
    #Delete, don't bother with the rest
    noteid=request.POST['annotation_id']
    if int(noteid) != 0:
        #Update
        note=Annotation.objects.get(id=int(noteid))
        #Clear previous notes
        Annotation_BarRegion.objects.filter(annotation=note).delete()
    else:
        #Insert Annotation()
        note=Annotation()
    n=AnnotationForm(request.POST,instance=note)
    try:
        typeid=request.POST['type_id']
        type=AnnotationType.objects.get(id=int(typeid))
    except Exception:
        type=AnnotationType.objects.get(id=1)
    n.type=type
    newNote=n.save()
    #Transform POLYGON feature def for later GeoJSON export
    #POLYGON((1426 2368,1170 2036,1358 1824,1350 2084,1526 2152,1426 2368))
    geotext=newNote.noteregions
    if len(geotext) > 0 :
        geotext=geotext.replace('POLYGON((','').replace('))','').replace(',','],[').replace(' ',',')
        newNote.noteregions='['+geotext+']'
        newNote.save()
    #Recalculate which bar regions intersect with this note
    try:
        notebars=request.POST['noteBars']
        barLabels=notebars.split(",")
        for bl in barLabels:
            b=Bar.objects.filter(barlabel=bl)
            if b.count() > 0:
                regions=BarRegion.objects.filter(bar=b,pageimage_id=newNote.pageimage_id)
                for r in regions:
                    Annotation_BarRegion(annotation=newNote,barregion=r).save()
    except Exception:
        pass
    return render_to_response('frontend/ajax/updatenote.html', {'note': newNote})


@csrf_exempt
def getAnnotations(request,id):
    notes=Annotation.objects.filter(annotation_barregion__barregion_id=id,type_id__gt=1)
    return render_to_response('frontend/ajax/annotations.html',{'notes': notes})

@csrf_exempt
def getAnnotationRegions(request,id):
    notes=Annotation.objects.filter(pageimage_id=id)
    annotations=[]
    for n in notes:
        annotations.append(noteGeos(n))
    return render_to_response('geojson.html', {'annotations': annotations, 'grouped': 0})
