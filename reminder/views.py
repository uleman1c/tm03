import datetime
from django.shortcuts import render
from django.http import JsonResponse
from file.models import File

from reminder.models import Reminder
# Create your views here.

def remind(request):

    res = dict()
    res['success'] = False

    if request.method == 'POST':

        idname = request.POST.get('idname')
        comments = request.POST.get('comments')
        remind = datetime.datetime.strptime(request.POST.get('remind'), '%Y%M%d%H%m%S')

        if File.objects.filter(idname=idname).count() > 0:

            fo = File.objects.filter(idname=idname).all().get()

            Reminder.objects.create(file=fo, comments=comments, remind=remind)

            res['success'] = True

    return JsonResponse(res)