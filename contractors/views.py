from django.http import JsonResponse
from django.shortcuts import render
from .forms import *


def contractors(request):

    form = ContractorsForm(request.POST or None)

    return render(request, 'contractors/index.html', locals())


def contractorsfilter(request):
    res = dict()
    contractors_list = list()
    for cc in Contractors.objects.filter(sname__contains=request.POST['search_filter'].lower()).order_by('name').all()[:20]:
        contractor_info = dict()
        contractor_info['name'] = cc.name
        contractor_info['inn'] = cc.inn
        contractor_info['kpp'] = cc.kpp
        contractor_info['id1c'] = cc.id1c
        contractors_list.append(contractor_info)

    res['contractors'] = contractors_list

    return JsonResponse(res)


