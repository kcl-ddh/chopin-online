__author__ = 'Elliott Hall'
from django.utils import unittest
from django.test.client import Client
from models import *
from editviews import *

class BarRegionTestCase(unittest.TestCase):
    def setUp(self):
        self.client= Client()
        st=SourceType.objects.create(type='Printed Edition')
        pt=PageType.objects.create(type='music')
        sct=SourceComponentType.objects.create(type='Music')
        source=Source.objects.create(label='Test Source',sourcetype=st)
        #Create dummy pageimage
        sc=SourceComponent.objects.create(source=source,sourcecomponenttype=sct)
        self.page=Page.objects.create(label='test',orderno=1,sourcecomponent=sc,pagetype=pt)
        self.pageimage=PageImage.objects.create(startbar=1,endbar=10,height=5731,width=4854,page=self.page)
        #Attach ten bars, numbered in order
        for x in range(1,11):
            #Make it look like system
            y=0
            if x>5:
                y=200
            br=BarRegion.objects.create(page=self.page,pageimage=self.pageimage,x=(x*100),y=y,anomaly=0,width=110,height=340)
            bar=Bar.objects.create(barlabel=str(x),barnumber=x)
            Bar_BarRegion.objects.create(bar=bar,barregion=br)
        pass #self.widget = Widget('The widget')
    def tearDown(self):
        pass
#        self.widget.dispose()
#        self.widget = None

    #Create new region
    def test_createRegion(self):
        self.assertEqual(self.pageimage.barregion_set.count(),10)

    #update region
    def test_updateRegions(self):
        pass
        #change geometry
        #Renumber existing region
            #Repeat (10a)
            #Multiple numbers 13,13a

    #Automatic renumbering of all bars on page
    def test_renumberRegions(self):
        pass

    #delete bar
    def test_deleteRegion(self):
        pass

#Test bar region ajax output
    #Test with unusual numbering

#class DBMITests(unittest.TestCase):
 #   pass

#Source editor tests
class sourceEditorTestCase(unittest.TestCase):

    def setUp(self):
        self.client= Client()
        #'new' as in uploaded source
        self.newsource=NewSource.objects.create(label='test Source',library='D-DL',copyright='copy',sourcecode='52-1-Test')
        #Create a bunch of new pageimages
        for x in range(1,11):
            pi=NewPageImage.objects.create(source=self.newsource,filename='test-'+str(x))
        #Existing source
        st=SourceType.objects.create(type='Printed Edition')
        pt=PageType.objects.create(type='music')
        sct=SourceComponentType.objects.create(type='Music')
        country=Country.objects.create(country='none')
        city=City.objects.create(city='none',country=country)
        archive=Archive.objects.create(name='none',siglum='',notes='',city=city)
        pub=Publisher.objects.create(publisher='test',notes='',publisherAbbrev='test')
        dedicatee=Dedicatee.objects.create(dedicatee='ME!')

        self.source=Source.objects.create(label='Test Source',sourcetype=st)
        ac=AcCode.objects.create(accode='64-1-REE')
        SourceInformation.objects.create(source=self.source,accode=ac)
        #Create dummy pageimages
        sc=SourceComponent.objects.create(source=self.source,sourcecomponenttype=sct)
        sb=1
        eb=25
        for x in range(1,11):
            page=Page.objects.create(label='test-'+str(x),orderno=1,sourcecomponent=sc,pagetype=pt)
            PageImage.objects.create(startbar=sb,endbar=eb,height=5731,width=4854,page=page)
            sb=eb+1
            eb+=26

#    Load/populate source editor page


    def test_loadEditor(self):
        #        with new source
        response =self.client.get('/ocve/sourceeditor/new/'+str(self.newsource.id)+'/')
        self.assertEqual(response.status_code,200,'Failed to load source editor with new source')
        #        with existing source
        response =self.client.get('/ocve/sourceeditor/'+str(self.source.id)+'/')
        self.assertEqual(response.status_code,200,'Failed to load source editor with existing source')

    def test_updateSourceInformation(self):
        #create sourceinformation
        #update source/information
        #delete?
        pass

    #Determine the opus from the new source's accode and assign it
    def test_getOpus(self):
        pass

    #Create components based on assigned opus
    #Using assigned opus, create source components for each workcomponent
    def test_createDefaultComponents(self):
        #Test automated creation of front/end matter
        pass

    #Manipulate components from ajax calls
    def test_updateSourceComponent(self):
        #create
        #Update (also change order)
        #delete
        pass

    #create/update page and pageImage
        #create
        #load existing
        #delete?
    def test_page(self):
        pass



