from multiprocessing import parent_process
import os

import json
import locale
from subprocess import list2cmdline
import sys
from unicodedata import name

from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests

from .forms import *
from datetime import timezone, datetime, timedelta
import pytz 

import urllib.parse
import io
from django.http import FileResponse
from django.db import connection


def filepart_clear_data(request):

    # c = 0
    # while c < 2000:

        # el = FilePart.objects.all()[0]
        # el.delete()

        # c = c + 1

    cursor = connection.cursor()
    cursor.execute('vacuum;')
    

    res = dict()
    res['count'] = FilePart.objects.all().count()
    res['success'] = True

    return JsonResponse(res)



def getfile(request):

    if 'userLogged' not in request.session:
        return redirect('login')
        
    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    filespath = 'I:\\Files\\'
    
    curUid = request.GET.get('id')

    if File.objects.filter(user=cu, idname=curUid).count() > 0:

        fo = File.objects.filter(user=cu, idname=curUid).all().get()

        fr = FileResponse(open(filespath + curUid + ".tmp",'rb'))

        fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(fo.name.encode('utf8'))
        fr['X-Sendfile'] = urllib.parse.quote(fo.name.encode('utf8'))

        return fr

    return ""
    
    
    
def files(request):

    if 'userLogged' not in request.session:
        return redirect('login')

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    filespath = 'I:\\Files\\'
    
    if request.method == 'POST':

        curUid = request.headers.get('id')
        curparent_id = request.headers.get('parentid')
        part = request.headers.get('part')

        if not curparent_id:
            curparent_id = ''

#        curUid = request.POST.get('id')
        
        if File.objects.filter(idname=curUid).count() == 0:
 #           filename = request.POST.get('filename')
            filename = urllib.parse.unquote(request.headers.get('filename'))
            co = File.objects.create(user=cu, idname=curUid, name=filename, parent_id=curparent_id)
        else:
            co = File.objects.filter(idname=curUid).all().get()

#        part = request.POST.get('part')
        if int(part) >= 0:
            # cfp = FilePart.objects.create(file=co, number=part)
            curName = str(co.idname) + ".tmp"
        
            destination = open(filespath + curName, 'ab+')
            destination.write(request.body)
            destination.close()
                
        
            # stat = os.stat(filespath + curName)
        
            co.size = co.size + int(request.headers.get('size'))
            co.save()
                    
            # if part:
                # cfp.size = stat.st_size
                # cfp.save()
                        
        else:
            size = request.headers.get('size')
            
            if co.size != int(size):
                co.size = 0
                co.save()
                        
        # res = dict()

        # return JsonResponse(res)        
            
           # cfps = FilePart.objects.filter(file=co).order_by('number').all()

           # if cfps.count() > 0:
               # resName = str(cfps[0].idname) + ".tmp"
               # resFile = open(filespath + resName, 'ab+')
               
               # c = 1
               # while c < cfps.count():
                   # partName = str(cfps[c].idname) + ".tmp"
                   
                   # partFile = open(filespath + partName, 'rb')

                   # buf = partFile.read(int(cfps[c].size))

                   # resFile.write(buf)

                   # partFile.close()

                   # c = c + 1

               # resFile.close()
               
               # resFile = None

               # co.idname = cfps[0].idname 
               # co.save()

               # c1 = 1
               # while c1 < cfps.count():
                   # partName = str(cfps[c1].idname) + ".tmp"
                   
                   # try:
                        # os.remove(filespath + partName)
                   # except:
                       # d = 1

                   # c1 = c1 + 1


    parent_id = request.GET.get('parent_id')

    if not parent_id:

        parent_id = ""


    affFolders = []
    lfiles = File.objects.filter(user=cu, parent_id=parent_id, is_folder=True, is_deleted=False).order_by('name').all()
    affFolders = list(lfiles)

    setStrSize(affFolders)    
    
    if parent_id != "":
        
        lfiles = File.objects.filter(user=cu, idname=parent_id).all()

        firstFolder = list(lfiles)
        firstFolder[0].name = '..'
        firstFolder[0].idname = firstFolder[0].parent_id
        firstFolder[0].size = ''

        affFolders.insert(0, firstFolder[0])



    allfiles = []

    search_file = request.GET.get('search_file')

    if search_file:
        lfiles = File.objects.filter(user=cu, parent_id=parent_id,  is_folder=False, name__icontains=search_file, is_deleted=False).order_by('-created').all()[:20]
    else:

        search_file = ""

        lfiles = File.objects.filter(user=cu,  parent_id=parent_id, is_folder=False, is_deleted=False).order_by('-created').all()[:20]

    allfiles = list(lfiles)

    setStrSize(allfiles)


    return render(request, 'files.html', locals())

def setStrSize(allfiles):
    for f in allfiles:
        if f.size > 1024 * 1024 * 1024:
            f.size = str(round(f.size / (1024 * 1024 * 1024), 1)) + " Гб"

        elif f.size > 1024 * 1024:
            f.size = str(round(f.size / (1024 * 1024), 1)) + " Мб"

        elif f.size > 1024:
            f.size = str(round(f.size / (1024), 1)) + " Кб"

        else:
            f.size = str(f.size) + " б"

def el(request):

    filespath = 'I:\\Files\\'
    
    if request.method == 'POST':

        if 'userLogged' not in request.session:
            return redirect('login')

        res = dict()
        res['success'] = False

        cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

        eluid = request.POST.get('eluid')
        idname = request.POST.get('idname')

        if File.objects.filter(user=cu, idname=idname).count() > 0:

            fo = File.objects.filter(user=cu, idname=idname).all().get()

            el = ExternalLink.objects.create(file=fo, idname=eluid)

            res['success'] = True

            
        return JsonResponse(res)


    elif request.method == 'GET':

        idname = request.GET.get('id')

        if ExternalLink.objects.filter(idname=idname).count() > 0:

            el = ExternalLink.objects.filter(idname=idname).all().get()

            if el.created.astimezone(pytz.timezone('Europe/Moscow')) > (datetime.now().astimezone(pytz.timezone('Europe/Moscow')) - timedelta(hours=1)):

                fo = el.file

                fr = FileResponse(open(filespath + fo.idname + ".tmp",'rb'))

                fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(fo.name.encode('utf8'))
                fr['X-Sendfile'] = urllib.parse.quote(fo.name.encode('utf8'))

                return fr

            else:
                
                return render(request, '404.html')

        else:

            return render(request, '404.html')


def addFolder(request):

    if 'userLogged' not in request.session:
        return redirect('login')

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    filespath = 'I:\\Files\\'
    
    if request.method == 'POST':

        co = File.objects.create(user=cu, name=request.POST.get('filename'), is_folder=True, parent_id=request.POST.get('parent_id'))

        res = dict()
        res['parent_id'] = co.idname

        return JsonResponse(res)

def setFolder(request):

    if 'userLogged' not in request.session:
        return redirect('login')

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    filespath = 'I:\\Files\\'
    
    if request.method == 'POST':

        co = File.objects.filter(user=cu, idname=request.POST.get('idname')).all().get()

        co.parent_id = request.POST.get('parent_id')
        co.save()

        res = dict()
        res['parent_id'] = co.parent_id

        return JsonResponse(res)

def setToBasket(request):

    if 'userLogged' not in request.session:
        return redirect('login')

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    filespath = 'I:\\Files\\'
    
    if request.method == 'POST':

        co = File.objects.filter(user=cu, idname=request.POST.get('idname')).all().get()

        co.is_deleted = True
        co.save()

        res = dict()
        res['parent_id'] = co.parent_id

        return JsonResponse(res)


def fileRename(request):

    if 'userLogged' not in request.session:
        return redirect('login')

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    filespath = 'I:\\Files\\'
    
    if request.method == 'POST':

        co = File.objects.filter(user=cu, idname=request.POST.get('idname')).all().get()

        co.name = request.POST.get('filename')
        co.save()

        res = dict()
        res['parent_id'] = co.parent_id

        return JsonResponse(res)





def filesold(request):

    if 'userLogged' not in request.session:
        return redirect('login')
        
    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    filespath = 'I:\\Files\\'
    
    if request.method == 'POST':
        for file in request.FILES.getlist('photo'):

            co = File.objects.create(user=cu, name=file.name)

            if request.POST.get('part'):
                cfp = File.objects.create(file=co)

            curName = str(co.idname) + ".tmp"
            
            with open(filespath + curName, 'wb+') as destination:
                
                for chunk in file.chunks():
                    destination.write(chunk)
                    
            
            stat = os.stat(filespath + curName)
            
            co.size = stat.st_size
            co.save()
                    
    allfiles = []

    allfiles = File.objects.filter(user=cu).order_by('-created').all()[:20]


    return render(request, 'files.html', locals())





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
#         server_address = "https://ow.ap-ex.ru/tm_po/hs/dta/obj"
#         # server_address = "https://ow.ap-ex.ru/tm_po/hs/exch/req"
#         # server_address = "http://localhost/tech_man/hs/exch/req"
#
#         try:
#             data_dict = requests.post(server_address, data=json.dumps(res), auth=("exch", "123456")).json()
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
