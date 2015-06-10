__author__ = 'Elliot'
from django.forms import *
from django import forms
from models import *
from tinymce.widgets import TinyMCE

class WorkForm(ModelForm):

    class Meta:
        model = Work
        exclude = ('workinformation',)

class NewSourceForm(ModelForm):
     class Meta:
         model = NewSource
         exclude = ('sourcecreated',)

class SourceForm(ModelForm):

    class Meta:
        model = Source
        exclude = ('',)

class SourceComponentForm(ModelForm):
    class Meta:
        model = SourceComponent
        exclude = ('overridelabel',)

class WorkInformationForm(ModelForm):

    class Meta:
        model = WorkInformation
        exclude = ('',)

class WorkComponentForm(ModelForm):

    class Meta:
        model = WorkComponent
        exclude = ('',)

WorkComponentFormset=modelformset_factory(WorkComponent)

class SourceInformationForm(ModelForm):

    class Meta:
        model = SourceInformation
        exclude = ()

class AnnotationForm(ModelForm):

    class Meta:
        model = Annotation
        fields = ['id','notetext','noteregions','pageimage','user']
        widgets = { 'id':HiddenInput(),
                    'user':HiddenInput(),
                    'pageimage':HiddenInput(),
                    'noteregions':HiddenInput()
        }


