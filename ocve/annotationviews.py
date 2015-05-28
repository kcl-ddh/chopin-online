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
    annotation_id = request.POST['annotation_id']
    annotation = None

    if int(annotation_id) > 0:
        #Update
        annotation = Annotation.objects.get(id=int(annotation_id))
        #Clear previous notes
        Annotation_BarRegion.objects.filter(annotation=annotation).delete()
    else:
        #Insert Annotation()
        annotation = Annotation()

    try:
        annotation_type_id = request.POST['type_id']
        annotation_type = AnnotationType.objects.get(
            id=int(annotation_type_id))
    except Exception:
        annotation_type = AnnotationType.objects.get(id=1)

    form = AnnotationForm(request.POST, instance=annotation)
    form.type = annotation_type

    new_annotation = form.save()

    #Transform POLYGON feature def for later GeoJSON export
    #POLYGON((1426 2368,1170 2036,1358 1824,1350 2084,1526 2152,1426 2368))
    geotext = new_annotation.noteregions
    if len(geotext) > 0 :
        geotext=geotext.replace('POLYGON((', '').replace('))', '').replace(
            ',', '],[').replace(' ', ',')
        new_annotation.noteregions = '[' + geotext + ']'
        new_annotation.save()
    
    #Recalculate which bar regions intersect with this note
    try:
        bars = request.POST['noteBars']
        labels = notebars.split(',')
        for label in labels:
            bar = Bar.objects.filter(barlabel=label)
            if bar and bar.count() > 0:
                regions = BarRegion.objects.filter(
                    bar=bar, pageimage_id=new_annotation.pageimage_id)

                for region in regions:
                    Annotation_BarRegion(
                        annotation=new_annotation, barregion=region).save()
    except Exception:
        pass

    return render_to_response('frontend/ajax/updatenote.html',
                              {'note': new_annotation})


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
