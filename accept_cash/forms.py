from django import forms
from .models import *


class AcceptCashForm(forms.ModelForm):
    class Meta:
        model = AcceptCash
        exclude = []
