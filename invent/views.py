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

from back_server import get_params

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

        server_address = get_params().addr + "/hs/dta/obj"

        try:
            data_dict = requests.post(server_address, data=json.dumps(res), auth=(get_params().user, get_params().pwd)).json()
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


# def add_accept(request):
#     if 'userLogged' not in request.session:
#         return render(request, 'login.html', locals())
#
#     mobile_mode = add_request_header(request)
#
#     cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()
#
#     if request.method == 'POST':
#
#         cc = Contractors.objects.filter(id1c=request.POST['contractor']).all().get()
#
#         comment = request.POST['comment']
#         order_number = request.POST['orderNumber']
#         order_date = request.POST['orderDate'].replace('-', '')
#         sum = request.POST['sum']
#         currency = request.POST['currency']
#
#         cd = datetime.now()
#
#         if order_date == '':
#             od = datetime(1970, 1, 1)
#         else:
#             od = datetime(int(order_date[0:4]), int(order_date[4:6]), int(order_date[6:8]))
#
#         ccu = Currency.objects.filter(name__exact=currency).all().get()
#
#         AcceptCash.objects.create(user=cu, contractor=cc, currency=ccu,
#                                       sum=sum, comments=comment,
#                                       order_number=order_number, order_date=od,
#                                       created=cd)
#
#         res = dict()
#
#         res['contractor'] = cc.id1c
#         res['comment'] = comment
#
#         return JsonResponse(res)
#
#     else:
#
#         form = AcceptCash(request.POST or None)
#
#         currencies = Currency.objects.all()
#
#         return render(request, 'accepts/checkout.html', locals())
#
#
# def sendto1c_acc(request):
#     if request.method == 'POST':
#
#         id1c = request.POST['id1c']
#
#         if id1c == 'all':
#             co = AcceptCash.objects.filter(delivered1c=False).all()
#         else:
#             co = AcceptCash.objects.filter(id1c=id1c).all()
#
#         res = dict()
#
#         orders_list = list()
#
#         for cco in co:
#             order_info = dict()
#             order_info['id1c'] = cco.id1c
#             order_info['user'] = cco.user.id1c
#             order_info['contractor'] = cco.contractor.id1c
#             order_info['comment'] = cco.comments
#             order_info['sum'] = str(cco.sum)
#             order_info['currency'] = cco.currency.code
#             order_info['created'] = cco.created.strftime('%Y%m%d%H%M%S')
#             order_info['order_number'] = cco.order_number
#             order_info['order_date'] = cco.order_date.strftime('%Y%m%d%H%M%S')
#
#             orders_list.append(order_info)
#
#         res['site'] = dict()
#         res['site']['accepts'] = orders_list
#
#         server_address = get_params().addr + "/hs/dta/obj"

#         try:
#             data_dict = requests.post(server_address, data=json.dumps(res), auth=(get_params().user, get_params().pwd)).json()
#         except Exception:
#             res['exeption'] = str(sys.exc_info())
#             data_dict = {}
#
#         if data_dict.get('success') == True:
#             res['success'] = True
#             for cco in co:
#                 cco.delivered1c = True
#                 cco.save()
#
#         res['req'] = data_dict
#
#         return JsonResponse(res)
