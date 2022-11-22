import datetime
import json
import sys
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse
from contractors.models import Contractors
from products.models import Characteristics, Products
from recipe.models import Recipe, RecipeGoods

from users1c.models import Users1c

import pytz 
import requests

from back_server import AUTH_DATA


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

    server_address = AUTH_DATA['addr'] + "/hs/dta/obj" # + "?request=getLeftovers&warehouse=" + cu.warehouse.id1c

    data = []
    data.append({'request': 'getLeftoversFromUpr', 'parameters': {'warehouse': cu.warehouse.id1c}})

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.post(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']),  data=json.dumps(data)).json()
        requestid = data_dict['requestid']

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    return render(request, 'recipes/leftovers.html', locals())


def reqexec(request):

    server_address = AUTH_DATA['addr'] + "/hs/dta/obj" + "?request=getRequestExecuted&requestid=" + request.headers.get('requestid')

    res = dict()
    res['result'] = True

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()
        res['executed'] = data_dict['responses'][0]['RequestExecuted']

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    return JsonResponse(res)


def getleftovers(request):

    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = AUTH_DATA['addr'] + "/hs/dta/obj" + "?request=getLeftoversUpr&warehouse=" + cu.warehouse.id1c

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()
        res['leftovers'] = data_dict['responses'][0]['LeftoversUpr']

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    return JsonResponse(res)

def getoutcome(request):

    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = AUTH_DATA['addr'] + "/hs/dta/obj" + "?request=getOutcomeUpr&warehouse=" + cu.warehouse.id1c

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()
        res['outcome'] = data_dict['responses'][0]['OutcomeUpr']

        for el in res['outcome']:
            if el['ДатаОтгрузки']:
                el['ДатаОтгрузки'] = datetime.datetime.strptime(el['ДатаОтгрузки'], '%Y%m%d%H%M%S').strftime('%d.%m.%Y')

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    return JsonResponse(res)

def prnform(request):

    server_address = AUTH_DATA['addr'] + '/hs/dta/prn/doc/ПеремещениеТоваров/' + request.GET.get('id') + '/dfdghfgd'

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']))

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    return HttpResponse(content=data_dict.content, content_type='application/pdf')



def add_recipe(request):

    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':

        cc = Contractors.objects.filter(id1c=request.POST['contractor']).all().get()

        comment = request.POST['comment']
        color_number = request.POST['colorNumber']
        end_product = request.POST['endproduct']
        end_product_text = request.POST['endproducttext']
        quantity = int(request.POST['endproductquantity'])

        ep = None
        if end_product:
            ep = Products.objects.filter(id1c=end_product).all().get()

        ro = Recipe.objects.create(user=cu, contractor=cc, comments=comment, end_product=ep,
                                      color_number=color_number, end_product_text=end_product_text, quantity=quantity)

        length = int(request.POST['length'])

        curInd = 0
        while(curInd < length):

            go = Products.objects.filter(id1c=request.POST['goods[' + str(curInd) + '][id1c]']   ).all().get()

            cidc = request.POST['goods[' + str(curInd) + '][cid1c]']

            cho = None
            if cidc:
                cho = Characteristics.objects.filter(id1c=cidc).all().get()

            RecipeGoods.objects.create(recipe=ro, product=go, characteristic=cho, quantity=request.POST['goods[' + str(curInd) + '][quantity]'] )

            curInd = curInd + 1






        res = dict()

        res['recipe'] = ro.id1c
        res['comment'] = comment

        return JsonResponse(res)

    else:

        return render(request, 'recipes/record.html', locals())


def outcome(request):

    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = AUTH_DATA['addr'] + "/hs/dta/obj" 

    data = []
    data.append({'request': 'getOutcomeFromUpr', 'parameters': {'warehouse': user.warehouse.id1c}})

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.post(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']),  data=json.dumps(data)).json()
        requestid = data_dict['requestid']

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    return render(request, 'outcome/index.html', locals())


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

            order_info['warehouse'] = ''
            if cco.user.warehouse:
                order_info['warehouse'] = cco.user.warehouse.id1c

            order_info['color_number'] = cco.color_number
            order_info['comment'] = cco.comments

            order_info['end_product'] = ''
            if cco.end_product:
                order_info['end_product'] = cco.end_product.id1c
                

            order_info['end_product_text'] = cco.end_product_text
            order_info['quantity'] = str(cco.quantity)

            order_info['created'] = cco.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y%m%d%H%M%S')

            goods = list()

            for good in RecipeGoods.objects.filter(recipe=cco).all():

                characteristic_id1c = ''
                if good.characteristic:
                    characteristic_id1c = good.characteristic.id1c
                

                goods.append({'id1c': good.product.id1c, 'characteristic_id1c': characteristic_id1c, 'quantity': str(good.quantity)})


            order_info['goods'] = goods

            orders_list.append(order_info)

        res['site'] = dict()
        res['site']['recipes'] = orders_list

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



