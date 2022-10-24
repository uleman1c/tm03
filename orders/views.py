import json
import sys

from django.http import JsonResponse
from django.shortcuts import render
import requests

from RequestHeaders.models import add_request_header
from .forms import *


def order(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    mobile_mode = add_request_header(request)

    form = OrderForm(request.POST or None)

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    elements = Order.objects.filter(user=cu).order_by('delivered1c', '-created').all()[:20]
    elements_to_send = Order.objects.filter(user=cu, delivered1c=False).all()

    return render(request, 'orders/index.html', locals())


def checkout(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    mobile_mode = add_request_header(request)

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()
    elements = ProductInBasket.objects.filter(user1c=cu).all()

    if request.method == 'POST':

        cc = Contractors.objects.filter(id1c=request.POST['contractor']).all().get()

        comment = request.POST['comment']

        co = Order.objects.create(user=cu, contractor=cc, comments=comment)

        for el in elements:
            cpo = ProductInOrder.objects.create(order=co, product=el.product, quantity=el.quantity)

            ProductInBasket.objects.filter(user1c=cu, product=el.product).delete()

        res = dict()

        res['contractor'] = cc.id1c
        res['comment'] = comment

        return JsonResponse(res)

    else:

        form = OrderForm(request.POST or None)
        return render(request, 'orders/checkout.html', locals())


def sendto1c(request):
    if request.method == 'POST':

        id1c = request.POST['id1c']

        if id1c == 'all':
            co = Order.objects.filter(delivered1c=False).all()
        else:
            co = Order.objects.filter(id1c=id1c).all()

        res = dict()

        orders_list = list()

        for cco in co:
            order_info = dict()
            order_info['id1c'] = cco.id1c
            order_info['user'] = cco.user.id1c
            order_info['contractor'] = cco.contractor.id1c
            order_info['comment'] = cco.comments
            order_info['created'] = cco.created.strftime('%Y%m%d%H%M%S')

            products_info = list()

            for pi in ProductInOrder.objects.filter(order=cco):
                product_info = dict()
                product_info['id1c'] = pi.product.id1c
                product_info['quantity'] = str(pi.quantity)

                products_info.append(product_info)

            order_info['products_info'] = products_info

            orders_list.append(order_info)

        res['site'] = dict()
        res['site']['orders'] = orders_list

        server_address = "https://ow.ap-ex.ru/tm_po/hs/dta/obj"
        # server_address = "https://ow.ap-ex.ru/tm_po/hs/exch/req"
        # server_address = "http://localhost/tech_man/hs/exch/req"

        try:
            data_dict = requests.post(server_address, data=json.dumps(res), auth=("exch", "123456")).json()
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
