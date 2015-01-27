from ocve.models import *

def run():
    sourceQuery = Source.objects.all().distinct().order_by('sourceinformation__accode')
    sourceQuery = sourceQuery.exclude(sourcelegacy__editstatus__id=10)
    counter = 0
    noImageCounter = 0
    for src in sourceQuery:
        if src.getSourceComponents() or src.getPages():
            #print "%s %s %s %s" % (counter, src.id, len(src.getPages()), src.getSourceComponents())
            #print "%s" % (src.id,)
            counter = counter+1
        else:
            print "%s" % (src.id,)
            noImageCounter = noImageCounter +1

    print counter
    print noImageCounter


