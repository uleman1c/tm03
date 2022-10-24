from django import forms
from .models import *


class ContractorsForm(forms.ModelForm):
    class Meta:
        model = Contractors
        exclude = []
