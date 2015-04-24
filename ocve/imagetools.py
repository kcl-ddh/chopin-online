import re
import urllib
from ocve.models import PageLegacy, SourceLegacy
from ocve.models import PageImage
from django.conf import settings
from django.utils.html import escape
import logging

__author__ = 'Elliot'

logger = logging.getLogger(__name__)

def buildOldPath(pi):
    p = pi.page
    pl = PageLegacy.objects.get(pageimage=pi)
    oldPath = 'ERRor'
    if pl.cfeoKey > 0:
        path = re.search("(.*?)_(.*)", pl.filename)
        if path is not None:
            oldPath = path.group(1) + "/" + path.group(1) + "_" + path.group(2) + ".jp2"
    elif pl.storageStructure is not None:
        path = re.search("(\d+)\/.*?\/(.*)", pl.storageStructure)
        if path is not None:
            sl = SourceLegacy.objects.get(source=p.sourcecomponent.source)
            oldPath = path.group(1) + "/" + str(sl.witnessKey) + "/" + path.group(2) + ".jp2"
    return oldPath


#Use the iip server to get width/height of an image
#Param full url to the image in iip format
def getImageDimensions(fullurl):
    meta = urllib.urlopen(fullurl+ '&obj=IIP,1.0&obj=Max-size&obj=Tile-size&obj=Resolution-number')
    dimensions={'width':0,'height':0}
    for line in meta.readlines():
       m = re.search("Max-size:\s*(\d+)\s*(\d+)", line)
       if m is not None:
         width = int(m.group(1))
         height = int(m.group(2))
         dimensions['width']=width
         dimensions['height']=height
    if dimensions['width'] == 0:
        logger.error('Image at '+fullurl+' not found')
    return dimensions


#Uses iip server to make sure dimensions in db correct
#pi=pageimage to check
def verifyImageDimensions(pi, oldPath):
    found=0
    try:
        fullurl = settings.IMAGE_SERVER_URL + '?FIF='
        fullurl = fullurl + oldPath
        dimensions=getImageDimensions(fullurl)
        if dimensions['width'] >0:
            if  pi.width != dimensions['width'] or pi.height != dimensions['height']:
                pi.width = dimensions['width']
                pi.height= dimensions['height']
                pi.permissionnote = ''
                pl=PageLegacy.objects.filter(pageimage=pi)
                if pl.count() >0:
                    if pl[0].jp2 == 'UNVERIFIED':
                        pl[0].jp2=oldPath
                        pl[0].save()
                pi.save()
                found=1
    except IOError:
        print("Could not contact server at "+fullurl)
    return found

#Request image information from the iip serv
#to verify images paths are correct
#http://ocve2-stg.cch.kcl.ac.uk/iip/iipsrv.fcgi?FIF=jp2/ocvejp2-proc/20/1/01TP/20-1-BH_GBLbl_p01TP.jp2&obj=IIP,1.0&obj=Max-size&obj=Tile-size&obj=Resolution-number
#iipsrv.fcgi?FIF=jp2/ocvejp2-proc/20/1/01TP/20-1-BH_GBLbl_p01TP.jp2&obj=IIP,1.0&obj=Max-size&obj=Tile-size&obj=Resolution-number
#jp2/ocvejp2-proc/20/1/02B/20-1-BH_GBLbl_p02B.jp2
def verifyImagesViaIIP():
    log = '<html><head>IMAGE REPORT</head><body><ul>'
    fullurl = settings.IMAGE_SERVER_URL + '?FIF=jp2/' #'http://ocve2-stg.cch.kcl.ac.uk/iip/iipsrv.fcgi?FIF=jp2/'
    allpages = PageImage.objects.filter(pagelegacy__jp2='UNVERIFIED')
    count=0
    for pi in allpages:
        #build old path
        oldPath = buildOldPath(pi)
        fullurl = settings.IMAGE_SERVER_URL + '?FIF=jp2/' #'http://ocve2-stg.cch.kcl.ac.uk/iip/iipsrv.fcgi?FIF=jp2/'
        #Request iamge informaiton from iip
        pl = PageLegacy.objects.get(pageimage=pi)
        if pl.cfeoKey > 0:
            fullurl = 'jp2/cfeojp2-proc/' + oldPath + '&obj=IIP,1.0&obj=Max-size'
        else:
            fullurl = 'jp2/ocvejp2-proc/' + oldPath + '&obj=IIP,1.0&obj=Max-size'
        meta = urllib.urlopen(fullurl)
        # found=0
        # for line in meta.readlines():
        #     m = re.search("Max-size:\s*(\d+)\s*(\d+)", line)
        #     if m is not None:
        #         found=1
        verifyImageDimensions(pi, oldPath)
        if found is 0:
            found=0
            if pl.cfeoKey > 0:
                #Check the _loose directory, they might be in there
                pi.width=0
                verifyImageDimensions(pi,'/_loose/'+pl.filename+'.jp2')
                if pi.width>0:
                    pl.jp2='cfeojp2-proc/_loose/'+pl.filename+'.jp2'
                    if pl.storageStructure is None:
                        pl.storageStructure=''
                    pl.save()
                    found=1
                    #log=log+'<li>FOUND IN _loose:  '+s.label+':  '+pi.page.label+' key:'+str(pi.id)+' at path '+oldPath+':'+pl.filename+'</li>'
            if found is 0:
                #Image not found, write to log
                s=pi.page.sourcecomponent.source
                print str(pi.id)+' not found'
                try:
                    log=log+'<li>'+s.label+':  '+pi.page.label+' key:'+str(pi.id)+' at path '+oldPath+':'+pl.filename+'</li>'
                except TypeError:
                    log=log+'<li> key:'+str(pi.id)+' </li>'
                count+=1
        else:
            #Record correct path in pagelegacy.jp2
            if pl.cfeoKey > 0:
                pl.jp2='cfeojp2-proc/' + oldPath
            else:
                pl.jp2='ocvejp2-proc/' + oldPath
            if pl.storageStructure is None:
                pl.storageStructure=''
            pl.save()
    return log + '</ul><h2>Total: ' + str(count) + '</h2></body>'

