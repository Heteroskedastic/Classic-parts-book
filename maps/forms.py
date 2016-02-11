from django import forms
from .models import *


class ImageForm(forms.ModelForm):

    class Meta:
        model = PartFile
        exclude = ['file_images']


class MapAttributeForm(forms.ModelForm):

    class Meta:
        model = MapAttribute
        exclude = []


class PartForm(forms.ModelForm):

    class Meta:
        model = Part
        exclude = []
