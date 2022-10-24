import json

from django.http import JsonResponse
from django.shortcuts import render
# from .forms import *
from error_log.models import ErrorLog


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


