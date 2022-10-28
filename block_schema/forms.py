from django import forms
from .models import *


class BlockSchemaForm(forms.ModelForm):
    class Meta:
        model = BlockSchema
        exclude = []
