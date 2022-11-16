import datetime
import json
import sys
from django.shortcuts import render
from django.http import JsonResponse
from contractors.models import Contractors
from products.models import Products
from recipe.models import Recipe, RecipeGoods

from users1c.models import Users1c

import pytz 
import requests


def recipes(request):

    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    elements = Recipe.objects.filter(user=cu).order_by('delivered1c', '-created').all()[:20]
    elements_to_send = Recipe.objects.filter(user=cu, delivered1c=False).all()



    return render(request, 'recipes/index.html', locals())


def leftovers(request):

    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    # elements = Recipe.objects.filter(user=cu).order_by('delivered1c', '-created').all()[:20]
    # elements_to_send = Recipe.objects.filter(user=cu, delivered1c=False).all()

    server_address = "https://ow.ap-ex.ru/tm_po/hs/dta/obj" # + "?request=getLeftovers&warehouse=" + cu.warehouse.id1c
    # server_address = "https://ow.ap-ex.ru/tm_po/hs/exch/req"
    # server_address = "http://localhost/tech_man/hs/exch/req"


    data = []
    data.append({'request': 'getLeftoversFromUpr', 'parameters': {'warehouse': cu.warehouse.id1c}})

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.post(server_address, auth=("exch", "123456"),  data=json.dumps(data)).json()
        requestid = data_dict['requestid']

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    return render(request, 'recipes/leftovers.html', locals())


def reqexec(request):

    server_address = "https://ow.ap-ex.ru/tm_po/hs/dta/obj" + "?request=getRequestExecuted&warehouse=" + request.GET.get('requestid')

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.get(server_address, auth=("exch", "123456")).json()
        requestid = data_dict['requestid']

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    return JsonResponse()


def add_recipe(request):

    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':

        cc = Contractors.objects.filter(id1c=request.POST['contractor']).all().get()

        comment = request.POST['comment']
        color_number = request.POST['colorNumber']

        ro = Recipe.objects.create(user=cu, contractor=cc, comments=comment,
                                      color_number=color_number)

        length = int(request.POST['length'])

        curInd = 0
        while(curInd < length):

            go = Products.objects.filter(id1c=request.POST['goods[' + str(curInd) + '][id1c]']   ).all().get()

            RecipeGoods.objects.create(recipe=ro, product=go, quantity=request.POST['goods[' + str(curInd) + '][quantity]'] )

            curInd = curInd + 1






        res = dict()

        res['recipe'] = ro.id1c
        res['comment'] = comment

        return JsonResponse(res)

    else:

        return render(request, 'recipes/record.html', locals())


def sendto1c_recipe(request):

    if request.method == 'POST':

        id1c = request.POST['id1c']

        if id1c == 'all':
            co = Recipe.objects.filter(delivered_1c=False).all()
        else:
            co = Recipe.objects.filter(id1c=id1c).all()

        res = dict()

        orders_list = list()

        for cco in co:
            order_info = dict()
            order_info['id1c'] = cco.id1c
            order_info['contractor'] = cco.contractor.id1c
            order_info['user'] = cco.user.id1c
            order_info['color_number'] = cco.color_number
            order_info['comment'] = cco.comments
            
            order_info['created'] = cco.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y%m%d%H%M%S')

            goods = list()

            for good in RecipeGoods.objects.filter(recipe=cco).all():

                goods.append({'id1c': good.product.id1c, 'quantity': str(good.quantity)})

            order_info['goods'] = goods

            orders_list.append(order_info)

        res['site'] = dict()
        res['site']['recipes'] = orders_list

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



