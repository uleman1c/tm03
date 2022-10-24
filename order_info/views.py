import json

from django.http import JsonResponse
from django.shortcuts import render
# from .forms import *
from order_info.models import OrderInfo


def add_order_info(request):

    if request.method == 'POST':

        res = dict()

        bodys = json.loads(request.body)

        OrderInfo.objects.filter(id1c=bodys[0]['id1c']).delete()

        for body in bodys:

            OrderInfo.objects.create(id1c=body['id1c'], strnum=body['strnum'], product=body['product'], character=body['character'], 
                quantity=body['quantity'], quantity1=body['quantity1'], quantity2=body['quantity2'], quantity3=body['quantity3'], 
                quantity4=body['quantity4'], quantity5=body['quantity5'], comment=body['comment'])

        res['success'] = True

        return JsonResponse(res)


def order_info(request):

    id1c = request.GET.get('id')

    oi = OrderInfo.objects.filter(id1c=id1c).all()

    return render(request, 'orderinfo.html', locals())



