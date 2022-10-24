from django import forms
from .models import *


class BitrixQueueForm(forms.ModelForm):
    class Meta:
        model = BitrixQueue
        exclude = []
