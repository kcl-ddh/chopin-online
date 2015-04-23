from ocve.models import *

def convertBars(pobjs):
    for pi in pobjs:
        print "%s-%s %s" % (pi.startbar, pi.endbar, pi.id)
        barsequence = BarSequence()
        barsequence.startbar = pi.startbar
        barsequence.endbar = pi.endbar
        barsequence.content_object = pi
        barsequence.save()

def run():
    pimages = PageImage.objects.all()
    npimages = NewPageImage.objects.all()

    print "converting the bars of PageImage objects"
    convertBars(pimages)
    print "converting the bars of NewPageImage objects"
    convertBars(npimages)


