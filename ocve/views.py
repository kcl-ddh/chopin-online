# Create your views here.


from dbmi.dbmiviews import *
from uiviews import *

IIP_URL = settings.IIP_URL
IMAGE_SERVER_URL = settings.IMAGE_SERVER_URL

#Image format for all uploaded pages
#Forced rather than detected because only tifs should be uploaded
UPLOAD_EXTENSION = '.tif'

#Error reporting template
errorPage = 'error.html'





def uploadOCVE(request):
    log = upload(request)
    return HttpResponse(log)

@csrf_exempt
def getBarRegions(request, id):
    geos = getGeoJSON(id)
    return render_to_response('geojson.html', {'geoRegions': geos, 'grouped': 0})



def getViewInPageRegions(request, id, barid):
    geos = getViewInPageJSON(id,barid)
    return render_to_response('geojson.html', {'geoRegions': geos, 'grouped': 0})


@csrf_exempt
def getGroupedBarRegions(request, id):
    geos = getGeoJSON(id)
    return render_to_response('geojson.html', {'geoRegions': geos, 'grouped': 1})




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
    