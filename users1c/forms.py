from django import forms
from .models import *


class User1cForm(forms.ModelForm):
    class Meta:
        model = Users1c
        exclude = []
