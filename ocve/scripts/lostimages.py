import os, subprocess
from django.utils import encoding
from ocve.models import *


def list_filenames():
    """ list the source and the related image filenames of NewPageImage objects"""
    newpageimages = NewPageImage.objects.all()
    for npi in newpageimages:
        output = u"%s:%s" % ( npi.source, npi.filename )
        print encoding.smart_str(output, encoding='utf-8', errors='ignore')

def list_images_by_editstatus(editstatus):
    pls = PageLegacy.objects.filter(editstatus=editstatus)
    empty_files = []
    no_dimensions = []
    for pl in pls:
        if pl.jp2.startswith('jp2/'):
            IMAGE_DIR = '/vol/ocve2/images'
        else:
            IMAGE_DIR = '/vol/ocve2/images/jp2'

        if not pl.jp2 == 'UNVERIFIED' and not pl.jp2 == 'MISSING':
            file_path = os.path.join(IMAGE_DIR, pl.jp2)
            file_size = os.stat( file_path  ).st_size

            if file_size == 0:
                empty_files.append(pl.jp2)
            else:
                if pl.pageimage.height == 0 or pl.pageimage.width == 0:
                    """
                    no dimensions defined in the database for given image
                    so obtain them using identify (ImageMagick, not jp2
                    support in PIL for Linux), parse the resulting string
                    and add height and width to the Image object
                    """
                    no_dimensions.append(pl.jp2)
                    identify_call = subprocess.Popen(['identify',file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = identify_call.communicate()

                    if identify_call.poll() == 0:
                        image_width, image_height = out.split(' ')[2].split('x')
                        #pl.pageimage.width = image_width
                        #pl.pageimage.height = image_height
                        #pl.save()
                print u"%s;%s;%s;%s;%s;db height: %s; db width: %s; actual size: " % (pl.pageimage.id, pl.cfeoKey, pl.ocveKey, pl.jp2, file_size, pl.pageimage.height, pl.pageimage.width )
        else:
            print u"%s;%s;%s;%s;%s" % (pl.pageimage.id, pl.cfeoKey, pl.ocveKey, pl.jp2,'path differs')

    print "Number of files: %s" % len(pls)
    print "Empty files: %s" % len(empty_files,)
    print "No dimensions: %s" % len(no_dimensions,)

def run():
    """ run lostimages"""
    print "missing images"
    list_images_by_editstatus(3L)
    #print "\n\ncorrupted images\n\n"
    #list_images_by_editstatus(4L)
