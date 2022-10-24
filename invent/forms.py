from django import forms
from .models import *


class InventForm(forms.ModelForm):
    class Meta:
        model = Invent
        exclude = []
