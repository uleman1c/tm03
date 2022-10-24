from django.shortcuts import render
from .forms import *


def bitrixqueue(request):
    form = BitrixQueueForm(request.POST or None)
    return render(request, 'bitrixqueue/index.html', locals())
