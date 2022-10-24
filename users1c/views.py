from django.shortcuts import render
from .forms import *


def users1c(request):
    form = User1cForm(request.POST or None)
    return render(request, 'users1c/index.html', locals())
