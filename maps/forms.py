from django import forms
from .models import MapAttribute, PartFile, Part


class BookForm(forms.ModelForm):

    class Meta:
        model = PartFile
        exclude = ['created']


class MapAttributeForm(forms.ModelForm):

    class Meta:
        model = MapAttribute
        exclude = []


class PartForm(forms.ModelForm):

    class Meta:
        model = Part
        exclude = []
