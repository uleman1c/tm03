import datetime
from django.shortcuts import render
from django.http import JsonResponse
from contractors.models import Contractors
from products.models import Products
from recipe.models import Recipe, RecipeGoods

from users1c.models import Users1c

# Create your views here.


def recipes(request):

    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    elements = Recipe.objects.filter(user=cu).order_by('delivered1c', '-created').all()[:20]
    elements_to_send = Recipe.objects.filter(user=cu, delivered1c=False).all()



    return render(request, 'recipes/index.html', locals())



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
