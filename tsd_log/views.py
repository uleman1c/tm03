import json

from django.http import JsonResponse
from django.shortcuts import render
# from .forms import *
from tsd_log.models import TsdLog


def add_in_tsd_log(request):

    if request.method == 'POST':

        res = dict()

        TsdLog.objects.create(text=json.loads(request.body)['text'])

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


