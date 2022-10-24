import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from RequestHeaders.models import add_request_header
from invent.models import Invent
from orders.models import ProductInBasket
from users1c.models import Users1c
from .forms import *


def products(request):

    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    mobile_mode = add_request_header(request)
    # mobile_mode = True

    form = ProductsForm(request.POST or None)
    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    mp = Products.objects.filter(Q(is_deleted=False) & Q(is_group=False) & Q(is_active=True)).order_by('name').all()[:20]

    elements = products_with_basket(cu, mp)
    cur_basket_quantity = basket_quantity(cu)

    return render(request, 'products/index.html', locals())


def products_with_basket(cu, mp):
    elements = list()
    for el in mp:
        prod_info = dict()
        prod_info['fullname'] = el.fullname
        prod_info['id1c'] = el.id1c
        qb = ProductInBasket.objects.filter(user1c=cu, product=el).all()
        if len(qb) == 0:
            prod_info['quantity'] = ''
        else:
            prod_info['quantity'] = qb.get().quantity
            if round(prod_info['quantity']) == prod_info['quantity']:
                prod_info['quantity'] = round(prod_info['quantity'])

        if prod_info['quantity'] == 0:
            prod_info['quantity'] = ''

        elements.append(prod_info)

    return elements


def goodsfilter(request):

    mobile_mode = add_request_header(request)

    res = dict()

    res['mobile_mode'] = mobile_mode

    search_filter = request.POST['search_filter'].lower()

    Filters.objects.create(text=search_filter)

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    ls = search_filter.split(' ')

    if len(ls) == 1:
        mp = Products.objects.filter((Q(sfullname__contains=ls[0]) | Q(article__contains=ls[0]))
                                     & Q(is_deleted=False) & Q(is_group=False) & Q(is_active=True)).order_by('name').all()[:20]
    elif len(ls) == 2:
        mp = Products.objects.filter((Q(sfullname__contains=ls[0]) | Q(article__contains=ls[0]))
                                     & (Q(sfullname__contains=ls[1]) | Q(article__contains=ls[1]))
                                     & Q(is_deleted=False) & Q(is_group=False) & Q(is_active=True)).order_by('name').all()[:20]
    elif len(ls) == 3:
        mp = Products.objects.filter((Q(sfullname__contains=ls[0]) | Q(article__contains=ls[0]))
                                     & (Q(sfullname__contains=ls[1]) | Q(article__contains=ls[1]))
                                     & (Q(sfullname__contains=ls[2]) | Q(article__contains=ls[2]))
                                     & Q(is_deleted=False) & Q(is_group=False) & Q(is_active=True)).order_by('name').all()[:20]
    elif len(ls) == 4:
        mp = Products.objects.filter((Q(sfullname__contains=ls[0]) | Q(article__contains=ls[0]))
                                     & (Q(sfullname__contains=ls[1]) | Q(article__contains=ls[1]))
                                     & (Q(sfullname__contains=ls[2]) | Q(article__contains=ls[2]))
                                     & (Q(sfullname__contains=ls[3]) | Q(article__contains=ls[3]))
                                     & Q(is_deleted=False) & Q(is_group=False) & Q(is_active=True)).order_by('name').all()[:20]
    elif len(ls) == 5:
        mp = Products.objects.filter((Q(sfullname__contains=ls[0]) | Q(article__contains=ls[0]))
                                     & (Q(sfullname__contains=ls[1]) | Q(article__contains=ls[1]))
                                     & (Q(sfullname__contains=ls[2]) | Q(article__contains=ls[2]))
                                     & (Q(sfullname__contains=ls[3]) | Q(article__contains=ls[3]))
                                     & (Q(sfullname__contains=ls[4]) | Q(article__contains=ls[4]))
                                     & Q(is_deleted=False) & Q(is_group=False) & Q(is_active=True)).order_by('name').all()[:20]
    elif len(ls) == 6:
        mp = Products.objects.filter((Q(sfullname__contains=ls[0]) | Q(article__contains=ls[0]))
                                     & (Q(sfullname__contains=ls[1]) | Q(article__contains=ls[1]))
                                     & (Q(sfullname__contains=ls[2]) | Q(article__contains=ls[2]))
                                     & (Q(sfullname__contains=ls[3]) | Q(article__contains=ls[3]))
                                     & (Q(sfullname__contains=ls[4]) | Q(article__contains=ls[4]))
                                     & (Q(sfullname__contains=ls[5]) | Q(article__contains=ls[5]))
                                     & Q(is_deleted=False) & Q(is_group=False) & Q(is_active=True)).order_by('name').all()[:20]
    else:
        mp = Products.objects.filter((Q(sfullname__contains=ls[0]) | Q(article__contains=ls[0]))
                                     & (Q(sfullname__contains=ls[1]) | Q(article__contains=ls[1]))
                                     & (Q(sfullname__contains=ls[2]) | Q(article__contains=ls[2]))
                                     & (Q(sfullname__contains=ls[3]) | Q(article__contains=ls[3]))
                                     & (Q(sfullname__contains=ls[4]) | Q(article__contains=ls[4]))
                                     & (Q(sfullname__contains=ls[5]) | Q(article__contains=ls[5]))
                                     & (Q(sfullname__contains=ls[6]) | Q(article__contains=ls[6]))
                                     & Q(is_deleted=False) & Q(is_group=False) & Q(is_active=True)).order_by('name').all()[:20]

    elements = products_with_basket(cu, mp)

    res['products'] = elements

    return JsonResponse(res)


def add_to_basket(request):
    res = dict()
    if request.method == 'POST':
        ul = request.session['userLogged']
        q = Users1c.objects.filter(name=ul.lower()).all()
        if len(q) > 0:
            qp = Products.objects.filter(id1c__exact=request.POST['product_id1c']).all()
            if len(qp) > 0:
                cu = q.get()
                cp = qp.get()
                qb = ProductInBasket.objects.filter(user1c=cu, product=cp).all()
                cur_quantity = int(request.POST['product_quantity'])
                if len(qb) == 0:
                    cb = ProductInBasket.objects.create(user1c=cu, product=cp, quantity=cur_quantity)
                else:
                    cb = qb.get()
                    cb.quantity += cur_quantity
                    cb.save()

                res['success'] = True
                res['quantity'] = cb.quantity
                if round(cb.quantity) == cb.quantity:
                    res['quantity'] = round(cb.quantity)

                if cb.quantity == 0:
                    res['quantity'] = ''
                    cb.delete()

                res['basket_quantity'] = basket_quantity(cu)

    return JsonResponse(res)


def basket_quantity(cu):
    res = 0
    for product_in_basket in ProductInBasket.objects.filter(user1c=cu).all():
        res += product_in_basket.quantity

    if round(res) == res:
        res = round(res)

    return res

def warehousesfilter(request):
    res = dict()
    contractors_list = list()
    for cc in Warehouses.objects.filter(sname__contains=request.POST['search_filter'].lower()).order_by('name').all()[:20]:
        contractor_info = dict()
        contractor_info['name'] = cc.name
        contractor_info['id1c'] = cc.id1c
        contractors_list.append(contractor_info)

    res['warehouses'] = contractors_list

    return JsonResponse(res)



def characteristicsfilter(request):
    res = dict()
    contractors_list = list()
    for cc in Characteristics.objects.filter(owner_id1c=request.POST['product']).order_by(
            'name').all()[
              :20]:
        contractor_info = dict()
        contractor_info['name'] = cc.name
        contractor_info['id1c'] = cc.id1c
        contractors_list.append(contractor_info)

    res['characteristics'] = contractors_list

    return JsonResponse(res)

def warehousecellsfilter(request):
    res = dict()
    contractors_list = list()
    for cc in WarehouseCells.objects.filter(warehouse_id1c=request.POST['warehouse']).filter(is_group=False).filter(sname__contains=request.POST['search_filter'].lower()).order_by(
            'name').all()[
              :20]:
        contractor_info = dict()
        contractor_info['name'] = cc.name
        contractor_info['id1c'] = cc.id1c
        contractors_list.append(contractor_info)

    res['warehousecells'] = contractors_list

    return JsonResponse(res)


def saveinvent(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    mobile_mode = add_request_header(request)

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':

        cw = Warehouses.objects.filter(id1c=request.POST['warehouse']).all().get()
        cc = Products.objects.filter(id1c=request.POST['product']).all().get()

        cchar = request.POST['сharacteristic']

        if cchar != '':
            cchar = Characteristics.objects.filter(id1c=cchar).all().get()

        cwc = request.POST['warehouseCell']

        if cwc != '':
            cwc = WarehouseCells.objects.filter(id1c=cwc).all().get()

        comment = request.POST['comment']
        quantity = request.POST['quantity']

        if cchar != '':
            if cwc != '':
                ci = Invent.objects.create(user=cu, warehouse=cw, product=cc, characteristic=cchar, warehouse_cell=cwc, quantity=quantity, comments=comment)
            else:
                ci = Invent.objects.create(user=cu, warehouse=cw, product=cc, characteristic=cchar, quantity=quantity, comments=comment)
        else:
            if cwc != '':
                ci = Invent.objects.create(user=cu, warehouse=cw, product=cc, warehouse_cell=cwc, quantity=quantity, comments=comment)
            else:
                ci = Invent.objects.create(user=cu, warehouse=cw, product=cc, quantity=quantity, comments=comment)


        # co = Order.objects.create(user=cu, contractor=cc, comments=comment)
        #
        # for el in elements:
        #     cpo = ProductInOrder.objects.create(order=co, product=el.product, quantity=el.quantity)
        #
        #     ProductInBasket.objects.filter(user1c=cu, product=el.product).delete()

        res = dict()

        res['warehouse'] = cw.id1c
        res['product'] = cc.id1c
        res['comment'] = comment

        return JsonResponse(res)

    # else:

        # form = OrderForm(request.POST or None)
        # return render(request, 'orders/checkout.html', locals())

