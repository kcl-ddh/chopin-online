__author__ = 'Elliot'
from django.forms import *
from django import forms
from models import *
from tinymce.widgets import TinyMCE

class WorkForm(ModelForm):

    class Meta:
        model = Work

class NewSourceForm(ModelForm):
     class Meta:
         model = NewSource
         exclude = ('sourcecreated',)

class SourceForm(ModelForm):

    class Meta:
        model = Source

class SourceComponentForm(ModelForm):
    class Meta:
        model = SourceComponent

class WorkInformationForm(ModelForm):

    class Meta:
        model = WorkInformation

class SourceInformationForm(ModelForm):

    class Meta:
        model = SourceInformation

class AnnotationForm(ModelForm):

    class Meta:
        model = Annotation
        fields = ['id','notetext','noteregions','pageimage']
        widgets = { 'id':HiddenInput(),
                    'pageimage':HiddenInput(),
                    'noteregions':HiddenInput()
        }


