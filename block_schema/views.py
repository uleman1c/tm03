import json
import locale
import sys

from django.http import JsonResponse
from django.shortcuts import render
import requests

from RequestHeaders.models import add_request_header
from access_key.models import AccessKey
from .forms import *
import pytz

from back_server import AUTH_DATA

def bs(request):

    if request.method == 'GET':

        access_key = request.GET.get('ak')
        
        if not access_key:

            return render(request, '404.html')

        qs = AccessKey.objects.filter(id1c=access_key)

        if qs.count() == 0:

            return render(request, '404.html')

        id1c = request.GET.get('id')
        
        if not id1c:

            return render(request, '404.html')

        ids = BlockSchema.objects.filter(id1c=id1c)

        if ids.count() == 0:

            bso = BlockSchema.objects.create(id1c=id1c)

        else:

            bso = ids.all().get()

        schema_only = request.GET.get('sch')

        if schema_only:
        
            return JsonResponse({"schema":bso.schema})

        else:

            return render(request, 'bs/index.html', locals())

    elif request.method == 'POST':
        
        res = dict()
        res['success'] = True

        id1c = request.headers.get('id')

        ids = BlockSchema.objects.filter(id1c=id1c)

        if ids.count() == 0:

            res['success'] = False

        else:

            bso = ids.all().get()

            bso.schema = request.body.decode('utf-8')

            bso.save()

        return JsonResponse(res)


def accepts(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    mobile_mode = add_request_header(request)

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()
    
    server_address = AUTH_DATA['addr'] + "/hs/dta/obj" + "?request=getCashStatus&manager=" + cu.id1c

    cash_status = 0
    try:
        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()
    except Exception:
        data_dict = {'success':True, 'responses': [{'getCashStatus':str(sys.exc_info())}]}

    if data_dict.get('success') == True:
        cash_status = data_dict.get('responses')[0].get('getCashStatus')

    cash_status_str = format(cash_status, '.2f')
    form = AcceptCash(request.POST or None)


    elements = AcceptCash.objects.filter(user=cu).order_by('delivered1c', '-created').all()[:20]
    elements_to_send = AcceptCash.objects.filter(user=cu, delivered1c=False).all()

    return render(request, 'accepts/index.html', locals())


def add_accept(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    mobile_mode = add_request_header(request)

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':

        cc = Contractors.objects.filter(id1c=request.POST['contractor']).all().get()

        comment = request.POST['comment']
        order_number = request.POST['orderNumber']
        order_date = request.POST['orderDate'].replace('-', '')
        sum = request.POST['sum']
        currency = request.POST['currency']

        cd = datetime.now()

        if order_date == '':
            od = datetime(1970, 1, 1)
        else:
            od = datetime(int(order_date[0:4]), int(order_date[4:6]), int(order_date[6:8]))

        ccu = Currency.objects.filter(name__exact=currency).all().get()

        AcceptCash.objects.create(user=cu, contractor=cc, currency=ccu,
                                      sum=sum, comments=comment,
                                      order_number=order_number, order_date=od,
                                      created=cd)

        res = dict()

        res['contractor'] = cc.id1c
        res['comment'] = comment

        return JsonResponse(res)

    else:

        form = AcceptCash(request.POST or None)

        currencies = Currency.objects.all()

        return render(request, 'accepts/checkout.html', locals())


def sendto1c_acc(request):
    if request.method == 'POST':

        id1c = request.POST['id1c']

        if id1c == 'all':
            co = AcceptCash.objects.filter(delivered1c=False).all()
        else:
            co = AcceptCash.objects.filter(id1c=id1c).all()

        res = dict()

        orders_list = list()

        for cco in co:
            order_info = dict()
            order_info['id1c'] = cco.id1c
            order_info['user'] = cco.user.id1c
            order_info['contractor'] = cco.contractor.id1c
            order_info['comment'] = cco.comments
            order_info['sum'] = str(cco.sum)
            order_info['currency'] = cco.currency.code
            order_info['created'] = cco.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y%m%d%H%M%S')
            order_info['order_number'] = cco.order_number
            order_info['order_date'] = cco.order_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y%m%d')

            orders_list.append(order_info)

        res['site'] = dict()
        res['site']['accepts'] = orders_list

        server_address = AUTH_DATA['addr'] + "/hs/dta/obj"

        try:
            data_dict = requests.post(server_address, data=json.dumps(res), auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()
        except Exception:
            res['exeption'] = str(sys.exc_info())
            data_dict = {}

        if data_dict.get('success') == True:
            res['success'] = True
            for cco in co:
                cco.delivered1c = True
                cco.save()

        res['req'] = data_dict

        return JsonResponse(res)
