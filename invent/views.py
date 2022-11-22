import json
import locale
import sys

from django.http import JsonResponse
from django.shortcuts import render
import requests

from RequestHeaders.models import add_request_header
from .forms import *
from datetime import timezone, datetime, timedelta
import pytz 

from back_server import AUTH_DATA

def invents(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    mobile_mode = add_request_header(request)

    wid = request.GET.get('wid')

    cw = None
    if wid is not None:
        cw = Warehouses.objects.filter(id1c=wid).all().get()

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()


    if wid is not None:
        elements = Invent.objects.filter(user=cu, warehouse=cw).order_by('delivered_1c', '-created').all()[:20]
    else:
        elements = Invent.objects.filter(user=cu).order_by('delivered_1c', '-created').all()[:20]


    elements_to_send = Invent.objects.filter(user=cu, delivered_1c=False).all()

    return render(request, 'invents/index.html', locals())


def sendto1c_invent(request):
    if request.method == 'POST':

        id1c = request.POST['id1c']

        if id1c == 'all':
            co = Invent.objects.filter(delivered_1c=False).all()
        else:
            co = Invent.objects.filter(id1c=id1c).all()

        res = dict()

        orders_list = list()

        for cco in co:
            order_info = dict()
            order_info['id1c'] = cco.id1c
            order_info['user'] = cco.user.id1c
            order_info['warehouse'] = cco.warehouse.id1c
            order_info['product'] = cco.product.id1c

            if cco.characteristic is not None:
                order_info['characteristic'] = cco.characteristic.id1c
            else:
                order_info['characteristic'] = ""

            order_info['comment'] = cco.comments
            
            if cco.warehouse_cell is not None:
                order_info['warehouse_cell'] = cco.warehouse_cell.id1c
            else:
                order_info['warehouse_cell'] = ""

            order_info['quantity'] = str(cco.quantity)
            order_info['created'] = cco.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y%m%d%H%M%S')

            orders_list.append(order_info)

        res['site'] = dict()
        res['site']['invents'] = orders_list

        server_address = AUTH_DATA['addr'] + "/hs/dta/obj"

        try:
            data_dict = requests.post(server_address, data=json.dumps(res), auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()
        except Exception:
            res['exeption'] = str(sys.exc_info())
            data_dict = {}

        if data_dict.get('success') == True:
            res['success'] = True
            for cco in co:
                cco.delivered_1c = True
                cco.save()

        res['req'] = data_dict

        return JsonResponse(res)

