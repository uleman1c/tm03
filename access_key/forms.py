from django import forms
from .models import *


class AccessKeyForm(forms.ModelForm):
    class Meta:
        model = AccessKey
        exclude = []
