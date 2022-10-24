import json

from django.http import JsonResponse
from django.shortcuts import render
# from .forms import *
from error_log.models import ErrorLog
from django.db import connection

def add_error_in_log(request):

    if request.method == 'POST':

        res = dict()

        ErrorLog.objects.create(error_text=json.loads(request.body)['text'])

        contractors_list = list()
        # for cc in Contractors.objects.filter(sname__contains=request.POST['search_filter'].lower()).order_by('name').all()[:20]:
        #     contractor_info = dict()
        #     contractor_info['name'] = cc.name
        #     contractor_info['inn'] = cc.inn
        #     contractor_info['kpp'] = cc.kpp
        #     contractor_info['id1c'] = cc.id1c
        #     contractors_list.append(contractor_info)

        res['success'] = True

        return JsonResponse(res)


def error_log_data(request):

    c = 0
    while c < 2000:

     #   el = ErrorLog.objects.all()[0]
      #  el.delete()

        c = c + 1

    cursor = connection.cursor()
    cursor.execute('vacuum;')
    

    res = dict()
    res['count'] = ErrorLog.objects.all().count()
    res['success'] = True

    return JsonResponse(res)

def error_log_data_count(request):

    res = dict()
    res['count'] = 1 # ErrorLog.objects.all().count()
    res['success'] = True

    return JsonResponse(res)

