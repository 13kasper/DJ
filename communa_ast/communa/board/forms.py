from django import forms
from django.forms import ModelForm
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title',
            }),
            'display_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Select banner image',
            }),
        }


class ImageForm(forms.ModelForm):
    images = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Images
        fields = ("images",)
