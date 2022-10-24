from django import forms
from .models import *


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = []
