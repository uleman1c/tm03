import hashlib
import json
import urllib
from datetime import datetime
import uuid

import pytz
import os

import requests
# from django.contrib.sites import requests
from django.http import JsonResponse, FileResponse
from django.http import HttpResponse
from django.shortcuts import redirect, render

from RequestHeaders.models import add_request_header
from accept_cash.models import AcceptCash
from contractors.models import Contractors
from currency.models import Currency
from file.models import File, FileOwner, FileVersion
from products.models import Products
from products.models import Characteristics
from products.models import Warehouses
from products.models import WarehouseCells
from tsd_log.models import TsdLog
from users1c import models
from users1c.models import ContainerFilesInfoBotUser, Users1c

import datetime
import json
import sys

import requests
from selenium import webdriver
import calendar

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

import threading

from urllib.parse import unquote

from requests.structures import CaseInsensitiveDict

from back_server import AUTH_DATA

from bs4 import BeautifulSoup
import requests as req

import zipfile

bitrix_address = AUTH_DATA['bitrix_addr']


def home(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = bitrix_address + '/timeman.status?user_id=' + str(user.idbitrix)

    try:

        server_address = bitrix_address + '/timeman.status?user_id=' + str(user.idbitrix)

        data_dict = requests.get(server_address).json()

        tm_status = data_dict['result']['STATUS']
        if tm_status == 'CLOSED':
            tm_status_str = 'Начать'
        elif tm_status == 'OPENED':
            tm_status_str = 'Завершить'
        elif tm_status == 'EXPIRED':
            tm_status_str = 'Истек'

    except Exception as ex:
        tm_status_str = ''
    #    finally:

    mobile_mode = add_request_header(request)

    return render(request, 'index.html', locals())

def sdekreqs(request):

    res = dict()

    res['tn'] = request.GET.get('tn')
    res['client_id'] = request.GET.get('client_id')
    res['client_secret'] = request.GET.get('client_secret')

    url = "https://api.cdek.ru/v2/oauth/token?client_id=" + res['client_id'] + "&client_secret=" + res['client_secret'] + "&grant_type=client_credentials"
    
    resp = requests.post(url) 

    res['access_token'] = resp.json().get('access_token')

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer " + res['access_token']

    url = "https://api.cdek.ru/v2/orders?cdek_number=" + res['tn']
    
    resp = requests.get(url , headers=headers)

    rj = resp.json()

    curEntity = rj.get('entity')

    if not curEntity:

        res['success'] = False
        
    else:

        res['uuid'] = curEntity.get('uuid')

        barcodesreq = dict()

        order = dict()
        order['order_uuid'] = res['uuid']

        orders = list()
        orders.append(order)
        
        barcodesreq['orders'] = orders
        barcodesreq['format'] = "A6"
        barcodesreq['lang'] = "RUS"

        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Bearer " + res['access_token']
        headers["Content-Type"] = "application/json"
        
        url = "https://api.cdek.ru/v2/print/barcodes"
        
        data = json.dumps(barcodesreq)
        
        resp = requests.post(url, headers=headers, data=data)

        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Bearer " + res['access_token']

        url = "https://api.cdek.ru/v2/orders?cdek_number=" + res['tn']
        
        resp = requests.get(url, headers=headers)

        rj = resp.json()

        res['related_entities'] = rj.get('related_entities')


        res['success'] = True


    return JsonResponse(res)

def curencecuorses(request):

    res = dict()

    req_date_str = ''
    req_date = request.GET.get('date')
    if req_date:
        req_date_str = '?UniDbQuery.Posted=True&UniDbQuery.To=' + req_date

    resp = req.get("https://www.cbr.ru/currency_base/daily/" + req_date_str)
    
    soup = BeautifulSoup(resp.text)    
    
    res['date'] = soup.find(attrs={"class": "datepicker-filter_button"}).text

    curT = soup.find('table', attrs={"class": "data"})

    curCuor = list()

    for curTchild in curT.children:
        if curTchild.name == 'tbody':
            for curTstr in curTchild.children:
                if curTstr.name == 'tr':
                    vl = list()
                    for curTstrTr in curTstr.children:
                        if curTstrTr.name == 'td':
                            vl.append(curTstrTr.text)
                    if len(vl) > 0:
                        curCuor.append(vl)

    res['curencecuorses'] = curCuor
    res['success'] = True

    return JsonResponse(res)


def transport_container_files(ftc):

    cf = FileOwner.objects.filter(type='doc', name='ТранспортныйКонтейнер', idname=ftc, is_deleted=False)

    res = dict()
    files = list()

    for ccf in cf:

        last_version_file = ccf.file

        last_version = None
        query_last_version = FileVersion.objects.filter(file_id=last_version_file.idname).order_by('-created')[:1]
        
        if query_last_version.count() > 0:
        
            last_version = query_last_version.all().get()

            last_version_file = File.objects.filter(idname=last_version.version_id).all().get()


        name = last_version_file.name
        spl = name.split('.')

        ext = ''
        if len(spl) > 1:

            ext = spl[len(spl) - 1]

            spl.remove(ext)

            name = '.'.join(spl)

        version_text = ''
        if last_version: 
            version_text = '(версия ' + str(last_version.number + 1) + ')' 

        files.append({'id': last_version_file.idname, 'name': name, 'ext': ext, 'user': last_version_file.user.name, 
        'created': last_version_file.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y'),
        'comments': last_version_file.comments, 'version': version_text})

    res['files'] = files

    return JsonResponse(res)

def transport_container_files_array(list_ids):

    res = dict()
    files = list()

    for list_id in list_ids:

        cf = FileOwner.objects.filter(type='doc', name='ТранспортныйКонтейнер', idname=list_id, is_deleted=False)

        for ccf in cf:

            last_version_file = ccf.file

            last_version = None
            query_last_version = FileVersion.objects.filter(file_id=last_version_file.idname).order_by('-created')[:1]
            
            if query_last_version.count() > 0:
            
                last_version = query_last_version.all().get()

                last_version_file = File.objects.filter(idname=last_version.version_id).all().get()


            name = last_version_file.name
            spl = name.split('.')

            ext = ''
            if len(spl) > 1:

                ext = spl[len(spl) - 1]

                spl.remove(ext)

                name = '.'.join(spl)

            version_text = ''
            if last_version: 
                version_text = '(версия ' + str(last_version.number + 1) + ')' 

            files.append({'tc_id': list_id, 'id': ccf.file.idname, 'name': name, 'ext': ext, 'user': last_version_file.user.name, 
            'created': last_version_file.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y'),
            'comments': last_version_file.comments, 'version_id': last_version_file.idname, 'version': version_text})

    res['files'] = files

    return JsonResponse(res)

def last_file_version(lfv):

    res = dict()
    files = list()

    last_version = None
    query_last_version = FileVersion.objects.filter(file_id=lfv).order_by('-created')[:1]
    
    if query_last_version.count() > 0:
    
        last_version = query_last_version.all().get()

        last_version_file = File.objects.filter(idname=last_version.version_id).all().get()


        name = last_version_file.name
        spl = name.split('.')

        ext = ''
        if len(spl) > 1:

            ext = spl[len(spl) - 1]

            spl.remove(ext)

            name = '.'.join(spl)

        version_text = ''
        if last_version: 
            version_text = '(версия ' + str(last_version.number + 1) + ')' 

        files.append({'id': last_version_file.idname, 'name': name, 'ext': ext, 'user': last_version_file.user.name, 
        'created': last_version_file.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y'),
        'comments': last_version_file.comments, 'version': version_text})

    res['version'] = files

    return JsonResponse(res)

def last_file_versions(list_ids):

    res = dict()
    files = list()

    for list_id in list_ids:

        last_version = None
        query_last_version = FileVersion.objects.filter(file_id=list_id).order_by('-created')[:1]
        
        if query_last_version.count() > 0:
        
            last_version = query_last_version.all().get()

            last_version_file = File.objects.filter(idname=last_version.version_id).all().get()


            name = last_version_file.name
            spl = name.split('.')

            ext = ''
            if len(spl) > 1:

                ext = spl[len(spl) - 1]

                spl.remove(ext)

                name = '.'.join(spl)

            version_text = ''
            if last_version: 
                version_text = '(версия ' + str(last_version.number + 1) + ')' 

            files.append({'file_id': list_id, 'id': last_version_file.idname, 'name': name, 'ext': ext, 'user': last_version_file.user.name, 
            'created': last_version_file.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y'),
            'comments': last_version_file.comments, 'version': version_text})

    res['version'] = files

    return JsonResponse(res)

def container_files(fc):

    cf = FileOwner.objects.filter(type='doc', name='Контейнер', idname=fc, is_deleted=False)

    res = dict()
    files = list()

    for ccf in cf:

        last_version_file = ccf.file

        last_version = None
        query_last_version = FileVersion.objects.filter(file_id=last_version_file.idname).order_by('-created')[:1]
        
        if query_last_version.count() > 0:
        
            last_version = query_last_version.all().get()

            last_version_file = File.objects.filter(idname=last_version.version_id).all().get()

        spl = ccf.file.name.split('.')

        name = last_version_file.name
        ext = ''

        if len(spl) > 1:

            ext = spl[len(spl) - 1]

            spl.remove(ext)

            name = '.'.join(spl)

        version_text = ''
        if last_version: 
            version_text = '(версия ' + str(last_version.number + 1) + ')' 

        files.append({'id': last_version_file.idname, 'name': name, 'ext': ext, 'user': last_version_file.user.name, 
        'created': last_version_file.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y'),
        'comments': last_version_file.comments, 'version': version_text})

    res['files'] = files

    return JsonResponse(res)

def container_files_array(list_ids):

    res = dict()
    files = list()

    for list_id in list_ids:

        cf = FileOwner.objects.filter(type='doc', name='Контейнер', idname=list_id, is_deleted=False)

        for ccf in cf:

            last_version_file = ccf.file

            last_version = None
            query_last_version = FileVersion.objects.filter(file_id=last_version_file.idname).order_by('-created')[:1]
            
            if query_last_version.count() > 0:
            
                last_version = query_last_version.all().get()

                last_version_file = File.objects.filter(idname=last_version.version_id).all().get()

            spl = ccf.file.name.split('.')

            name = last_version_file.name
            ext = ''

            if len(spl) > 1:

                ext = spl[len(spl) - 1]

                spl.remove(ext)

                name = '.'.join(spl)

            version_text = ''
            if last_version: 
                version_text = '(версия ' + str(last_version.number + 1) + ')' 

            files.append({'c_id': list_id, 'id': last_version_file.idname, 'name': name, 'ext': ext, 'user': last_version_file.user.name, 
            'created': last_version_file.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y'),
            'comments': last_version_file.comments, 'version': version_text})

    res['files'] = files

    return JsonResponse(res)

def file_by_id(ff):

    ccf = File.objects.filter(idname=ff).all().get()
    cf = FileOwner.objects.filter(file=ccf, is_deleted=False)

    res = dict()
    files = list()

    for ccf in cf:

        spl = ccf.file.name.split('.')

        ext = ''
        name = ccf.file.name
        if len(spl) > 1:

            ext = spl[len(spl) - 1]

            spl.remove(ext)

            name = '.'.join(spl)

        files.append({'id': ccf.file.idname, 'name': name, 'ext': ext, 'user': ccf.user.name, 
            'created': ccf.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y'),
            'comments': ccf.comments })

    res['files'] = files

    return JsonResponse(res)

def file_attachment(fatt, ext, full_name):

    cfo = File.objects.filter(idname=fatt).all().get()

    filespath = 'I:\\Attachments\\'

    curName = fatt + ".tmp"

    filename = filespath + curName

    if not full_name:
        full_name = cfo.name

    return FileResponse(open(filename, 'rb'), filename=full_name)


def zip_transport_container_files(ziptc):

    filespath = 'I:\\Attachments\\'

    zipname = filespath + str(uuid.uuid4()) + ".zip"
    archive = zipfile.ZipFile(zipname, mode="w", allowZip64=False, compression=zipfile.ZIP_DEFLATED, strict_timestamps=False)

    server_address = AUTH_DATA['addr'] + '/hs/dta/obj?request=getAttachedFiles&type=doc&name=ТранспортныйКонтейнер&id=' + ziptc

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    for attf in data_dict['responses'][0]['AttachedFiles']:

        server_address = AUTH_DATA['addr'] + '/hs/dta/files/ref/КонтейнерПрисоединенныеФайлы/' + attf['Идентификатор'] + '/dfdghfgd'

        res = dict()

        res['result'] = True

        try:

            data_file = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']))

        except Exception as ex:
            tasks_list = list()
            res['message'] = str(sys.exc_info())
            res['result'] = False

        ext = attf['Расширение']
        filename = "contfiles\\" + str(uuid.uuid4()) + "." + ext

        f = open(filename, 'wb')
        f.write(data_file.content)
        f.close()

        archive.write(filename, arcname=attf['Имя'] + '.' + ext)

    cf = FileOwner.objects.filter(type='doc', name='ТранспортныйКонтейнер', idname=ziptc, is_deleted=False)

    for ccf in cf:
        archive.write(filespath + ccf.file.idname + '.tmp', arcname=ccf.file.name)

    archive.close()

    return FileResponse(open(zipname, 'rb'))


def zip_container_files(zipc):

    filespath = 'I:\\Attachments\\'

    zipname = filespath + str(uuid.uuid4()) + ".zip"
    archive = zipfile.ZipFile(zipname, mode="w", allowZip64=False, compression=zipfile.ZIP_DEFLATED, strict_timestamps=False)

    server_address = AUTH_DATA['addr'] + '/hs/dta/obj?request=getAttachedFiles&type=doc&name=Контейнер&id=' + zipc

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()

    except Exception as ex:
        tasks_list = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    for attf in data_dict['responses'][0]['AttachedFiles']:

        server_address = AUTH_DATA['addr'] + '/hs/dta/files/ref/КонтейнерПрисоединенныеФайлы/' + attf['Идентификатор'] + '/dfdghfgd'

        res = dict()

        res['result'] = True

        try:

            data_file = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']))

        except Exception as ex:
            tasks_list = list()
            res['message'] = str(sys.exc_info())
            res['result'] = False

        ext = attf['Расширение']
        filename = "contfiles\\" + str(uuid.uuid4()) + "." + ext

        f = open(filename, 'wb')
        f.write(data_file.content)
        f.close()

        archive.write(filename, arcname=attf['Имя'] + '.' + ext)


    cf = FileOwner.objects.filter(type='doc', name='Контейнер', idname=zipc, is_deleted=False)

    for ccf in cf:
        archive.write(filespath + ccf.file.idname + '.tmp', arcname=ccf.file.name)

    archive.close()

    return FileResponse(open(zipname, 'rb'))


import requests
 
def send_msg_to_container_files_info_bot(text):

    token = AUTH_DATA['container_files_info_bot_token']

    objs = ContainerFilesInfoBotUser.objects.filter()

    for curobj in objs:

        chat_id = curobj.user.telegram_id
        url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + str(chat_id) + "&text=" + text
        results = requests.get(url_req)

#    print(results.json())


def containerstatuses(request):

    if 'userLogged' not in request.session:
        return redirect('../login/?ret=/containerstatuses/')

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'GET':

        ftc = request.GET.get('ftc')
        if ftc:
            return transport_container_files(ftc)

        lfv = request.GET.get('lfv')
        if lfv:
            return last_file_version(lfv)

        fc = request.GET.get('fc')
        if fc:
            return container_files(fc)

        ff = request.GET.get('f')
        if ff:
            return file_by_id(ff)

        fatt = request.GET.get('fatt')
        if fatt:
            return file_attachment(fatt, request.GET.get('ext'), request.GET.get('full_name'))

        ziptc = request.GET.get('ziptc')
        if ziptc:
            return zip_transport_container_files(ziptc)

        zipc = request.GET.get('zipc')
        if zipc:
            return zip_container_files(zipc)
            
        smtcfib = request.GET.get('smtcfib')
        if smtcfib:
            send_msg_to_container_files_info_bot(smtcfib)



        server_address = AUTH_DATA['addr'] + "/hs/dta/obj?request=getTransportContainersStatus"

        container_statuses = None
        try:

            data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()

            container_statuses = data_dict['responses'][0]['TransportContainersStatus']

        except Exception as ex:
            tasks_list = list()
            data_dict = str(sys.exc_info())

    #   мОстатков.Добавить(Новый Структура("Файлы, Контейнеры, Период, ТранспортныйКонтейнер, НомерПоДаннымПеревозчика, ВнутреннийНомер, ТоварПоставщик, НомерКонтейнера, ПунктНазначения, СтатусПоставки, "
    #       + "РасчетнаяНеделяПрибытияНаТаможню, Получатель, СтоимостьФрахта, Валюта, ПроцентОплаты, Перевозчик, ПунктЗагрузки, СтанцияОтправления, "
    #       + "ОтгрузкаСоСкладаПоставщика, ВыходСоСтанцииИзПорта, ВПортПерегрузаНаГраницу, ОтГраницыРф, ПриходВПунктНазначения, ПриходНаСклад", 

        if container_statuses:

            for container_status in container_statuses:
                container_status['Период'] = datetime.datetime.strptime(container_status['Период'], '%Y%m%d%H%M%S').strftime('%d.%m.%Y %H:%M:%S')
                container_status['ЕстьФайлы'] = False

                for container in container_status['Контейнеры']:
                    container['ЕстьФайлы'] = False

                if len(container_status['Файлы']) > 0:
                    container_status['ЕстьФайлы'] = True

                    for curFile in container_status['Файлы']:
                        
                        curFile['ДатаСоздания'] = datetime.datetime.strptime(curFile['ДатаСоздания'], '%Y%m%d%H%M%S').strftime('%d.%m.%Y')
                        
                        if curFile['Расширение'] == 'pdf':
                            curFile['Картинка'] = '/static/pdf.png'
                        elif curFile['Расширение'] == 'jpg':
                            curFile['Картинка'] = '/static/jpg.png'
                        elif curFile['Расширение'] == 'xls' or curFile['Расширение'] == 'xlsx':
                            curFile['Картинка'] = '/static/xls.png'
                        elif curFile['Расширение'] == 'doc' or curFile['Расширение'] == 'docx':
                            curFile['Картинка'] = '/static/doc.png'

                        for container in container_status['Контейнеры']:
                            if container['ИдентификаторКонтейнера'] == curFile['ИдентификаторКонтейнера']:
                                container['ЕстьФайлы'] = True
                        

            container_statuses_h = json.dumps(container_statuses)

        return render(request, 'containerstatuses/index.html', locals())

    elif request.method == 'POST':

        lfv = request.GET.get('lfv')
        if lfv:
            return last_file_versions(json.loads(request.body.decode('utf-8')))

        ftc = request.GET.get('ftc')
        if ftc:
            return transport_container_files_array(json.loads(request.body.decode('utf-8')))

        fc = request.GET.get('fc')
        if fc:
            return container_files_array(json.loads(request.body.decode('utf-8')))

        filespath = 'I:\\Attachments\\'
        
        type1c = request.headers.get('type1c')
        name1c = urllib.parse.unquote(request.headers.get('name1c'))
        id1c = request.headers.get('id1c')        

        curUid = request.headers.get('id')
        curparent_id = ''
        part = request.headers.get('part')

        if not curparent_id:
            curparent_id = ''

        if File.objects.filter(idname=curUid).count() == 0:

            filename = urllib.parse.unquote(request.headers.get('filename'))
            co = File.objects.create(user=cu, idname=curUid, name=filename, parent_id=curparent_id)

            cfo = FileOwner.objects.create(user=cu, file=co, type=type1c, name=name1c, idname=id1c)

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

        res = dict()
        res['success'] = True

        return JsonResponse(res)


def fileversions(request):

    if 'userLogged' not in request.session:
        return redirect('../login/?ret=/fileversions/')

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'GET':

        container_name = request.GET.get('cname')

        fatt = request.GET.get('fatt')
        if fatt:
            return file_attachment(fatt, request.GET.get('ext'), request.GET.get('full_name'))

        smtcfib = request.GET.get('smtcfib')
        if smtcfib:
            send_msg_to_container_files_info_bot(smtcfib)

        ownerid = request.GET.get('id')
        ownername = request.GET.get('name')
        cid = request.GET.get('cid')

        in_t = request.GET.get('in_t') == '1'
        if not in_t:

            server_address = AUTH_DATA['addr'] + '/hs/dta/obj?request=getAttachedFiles&type=doc&name=' + ownername + '&id=' + ownerid

            res = dict()

            res['result'] = True

            try:

                data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()

            except Exception as ex:
                tasks_list = list()
                res['message'] = str(sys.exc_info())
                res['result'] = False

            ccfp = None
            for attf in data_dict['responses'][0]['AttachedFiles']:

                if attf['Идентификатор'] == cid:
                    ccfp = attf

        else:

            ccf = File.objects.filter(idname=cid).all().get()
        
            ext = ''
            name = ccf.name

            spl = ccf.name.split('.')

            if len(spl) > 1:

                ext = spl[len(spl) - 1]

                spl.remove(ext)

                name = '.'.join(spl)

            ccfp = {'Идентификатор': cid, 'Имя': name, 'Расширение': ext, 'ДатаСоздания': ccf.created.strftime('%Y%m%d%H%M%S'), 'Автор': ccf.user.name}

        ccfp['ownerid'] = ownerid
        ccfp['ownername'] = ownername

        name_ext = ccfp['Имя'] + '.' + ccfp['Расширение']

        fv = FileVersion.objects.filter(file_id=ccfp['Идентификатор'], is_deleted=False).order_by('created')

        res = dict()
        versions = list()

        versions.append({'created': datetime.datetime.strptime(ccfp['ДатаСоздания'], '%Y%m%d%H%M%S').strftime('%d.%m.%Y %H:%M:%S'), 'number': 0,
            'user': ccfp['Автор'], 'name': ccfp['Имя'] + '.' + ccfp['Расширение'], 'ext': ccfp['Расширение'], 'id': ccfp['Идентификатор'], 'in_t':in_t})

        

        for cfv in fv:

            cur_version_file = File.objects.filter(idname=cfv.version_id).all().get()
            
            versions.append({'created': cfv.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y %H:%M:%S'), 'number': cfv.number,
                'user': cfv.user.name, 'name': cur_version_file.name, 'id': cfv.version_id, 'in_t':True})


        if False:

            fid = request.GET.get('id')
            ext = request.GET.get('ext')

            server_address = AUTH_DATA['addr'] + '/hs/dta/files/' + request.GET.get('type') + '/' + request.GET.get('name') + '/' + fid + '/dfdghfgd'

            res = dict()

            res['result'] = True

            try:

                data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']))

            except Exception as ex:
                tasks_list = list()
                res['message'] = str(sys.exc_info())
                res['result'] = False

        #                    response = FileResponse(file)
        #                   response['Content-Type'] = 'application/octet-stream'
        #                  response['Content-Disposition'] = 'attachment;filename='+FileName

        # return HttpResponse(content=data_dict.content, content_type='application/' + ext, filename=fid + '.' + ext)

            filename = "contfiles\\" + str(uuid.uuid4()) + "." + ext

            f = open(filename, 'wb')
            f.write(data_dict.content)
            f.close()





        return render(request, 'containerstatuses/fileversions.html', locals())

    elif request.method == 'POST':

        filespath = 'I:\\Attachments\\'
        
        ownerid = request.headers.get('ownerid')
        ownername = urllib.parse.unquote(request.headers.get('ownername'))
        fileid = request.headers.get('fileid')        

        curUid = request.headers.get('id')
        curparent_id = ''
        part = request.headers.get('part')

        if not curparent_id:
            curparent_id = ''

        if File.objects.filter(idname=curUid).count() == 0:

            filename = urllib.parse.unquote(request.headers.get('filename'))
            co = File.objects.create(user=cu, idname=curUid, name=filename, parent_id=curparent_id)

            versionnumber = 0
            query_last_version_number = FileVersion.objects.filter(file_id=fileid).order_by('-number')[:1]
            if query_last_version_number.count() > 0:
                versionnumber = query_last_version_number.all().get().number

            cversion = FileVersion.objects.create(user=cu, file_id=fileid, version_id=curUid, number=versionnumber + 1)

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

        res = dict()
        res['success'] = True

        return JsonResponse(res)




def skladthr(request):
    boxes = '' \
'       // BOXES\n' \
'           const geometryBox = new THREE.BoxGeometry(10, 500, 10);\n' \
'           const materialBox = new THREE.MeshBasicMaterial({color: 0x00ff00});\n' \
'           const cube = new THREE.Mesh(geometryBox, material);\n' \
'           cube.position.x = i * 100;\n' \
'           cube.position.y = 0;\n' \
'           cube.updateMatrix();\n' \
'           cube.matrixAutoUpdate = false;\n' \
'           scene.add(cube);\n' \
'           const cube2 = new THREE.Mesh(geometryBox, material);\n' \
'           cube2.position.x = i * 100;\n' \
'           cube2.position.y = 0;\n' \
'           cube2.position.z = 100;\n' \
'           cube2.updateMatrix();\n' \
'           cube2.matrixAutoUpdate = false;\n' \
'           scene.add(cube2);\n'

    shelves = ''\
'           const geometryShelve = new THREE.BoxGeometry(5000, 10, 100);\n' \
'           const shelve = new THREE.Mesh(geometryShelve, material);\n' \
'           shelve.position.x = 2500;\n' \
'           shelve.position.z = 50;\n' \
'           shelve.position.y = -150 + i * 100;\n' \
'           scene.add(shelve);\n' \
''

    return render(request, 'skladthr/index.html', locals())


def bitrixwh(request):
    res = dict()

    TsdLog.objects.create(text=unquote(request.body.decode("utf-8")))

    contractors_list = list()
    # for cc in Contractors.objects.filter(sname__contains=request.POST['search_filter'].lower()).order_by('name').all()[:20]:
    #     contractor_info = dict()
    #     contractor_info['name'] = cc.name
    #     contractor_info['inn'] = cc.inn
    #     contractor_info['kpp'] = cc.kpp
    #     contractor_info['id1c'] = cc.id1c
    #     contractors_list.append(contractor_info)

    res['success'] = True

    return JsonResponse(res)


def lp(request):
    url = "https://api.l-post.ru"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = "method=Auth&secret=EAT50ex3W8tY3emG"

    resp = requests.post(url, headers=headers, data=data)

    # print(resp.status_code)

    return JsonResponse(resp.json())


def lpl2(request):
    sjson = request.GET.get('json')

    url = "https://api.l-post.ru/?method=" + request.GET.get('method') \
          + "&token=" + request.GET.get('token') + "&ver=" + request.GET.get('ver') \
          + "&json=" + sjson

    # headers = CaseInsensitiveDict()
    # headers["Content-Type"] = "application/x-www-form-urlencoded"
    #
    # data = "method=Auth&secret=EAT50ex3W8tY3emG"

    resp = requests.get(url)

    id_order = json.loads(sjson).get("ParamsForLabels")[0].get("ID_Order")

    filename = id_order + ".pdf"

    f = open(filename, 'wb')
    f.write(bytearray.fromhex(json.loads(resp.json().get("JSON_TXT")).get("CargoesLabel")[0].get("Label")))

    res = dict()
    res['filename'] = filename
    res['label'] = json.loads(resp.json().get("JSON_TXT")).get("CargoesLabel")[0].get("Label")

    fread = open(filename, 'rb')

    # print(resp)

    return FileResponse(fread)  # JsonResponse(res)

def savesdek(request):

    basename = "logfile"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "savesdek\\" + "_".join([basename, suffix]) + ".txt"

    f = open(filename, 'w')
    f.write(request.method + ' ' + request.get_full_path())
    f.write(str(request.META))
    f.write(json.dumps(request.GET))
    f.write(json.dumps(request.POST))



    res = dict()
    res['res'] = 'OK'

    return JsonResponse(res)


def lpl(request):
    sjson = request.GET.get('json')

    url = "https://api.l-post.ru/?method=" + request.GET.get('method') \
          + "&token=" + request.GET.get('token') + "&ver=" + request.GET.get('ver') \
          + "&json=" + sjson

    # headers = CaseInsensitiveDict()
    # headers["Content-Type"] = "application/x-www-form-urlencoded"
    #
    # data = "method=Auth&secret=EAT50ex3W8tY3emG"

    resp = requests.get(url)

    errorMessageStr = resp.json().get("errorMessage")

    res = dict()
    if errorMessageStr:

        res['errorMessage'] = errorMessageStr

        return JsonResponse(res)

    else:

        id_order = json.loads(sjson).get("ParamsForLabels")[0].get("ID_Order")

        filename = "savelpl\\" + id_order + ".pdf"

        f = open(filename, 'wb')
        f.write(bytearray.fromhex(json.loads(resp.json().get("JSON_TXT")).get("CargoesLabel")[0].get("Label")))

        res['filename'] = filename
        res['label'] = json.loads(resp.json().get("JSON_TXT")).get("CargoesLabel")[0].get("Label")

        fread = open(filename, 'rb')

        # print(resp)

        return FileResponse(fread)  # JsonResponse(res)


def sha1(request):
    sh = request.GET.get('sh')

    hash_object = hashlib.sha1(bytearray(sh, "utf8"))
    hex_dig = hash_object.hexdigest()

    res = dict()
    res['res'] = hex_dig

    return JsonResponse(res)


def dm(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    dmid = request.GET.get('id')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    return render(request, 'dm.html', locals())


def dmtaskstouser(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    dmid = request.GET.get('id')

    author = request.GET.get('author')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if dmid == '1':
        cur_dmbase = user.dmbase
        cur_dbuser = user.dmuser
    else:
        cur_dmbase = user.dmbase2
        cur_dbuser = user.dmuser2

    server_address = cur_dmbase + "/hs/unido/req?request=getTaskList&executor=" + cur_dbuser

    data = []
    data.append({'request': 'getTaskList',
                 'parameters': {'author': author, 'executor': cur_dbuser}})

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']), json=data).json()

        tasks_list = data_dict['responses'][0]['getTaskList']

    except Exception as ex:
        tasks_list = list()
        data_dict = str(sys.exc_info())

    for tl in tasks_list:
        if tl['СрокИсполнения']:
            tl['СрокИсполнения'] = datetime.datetime.strptime(tl['СрокИсполнения'][:8], "%Y%m%d")

    from_user = False

    server_address = cur_dmbase + "/hs/unido/req?request=userList"

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()

        executors = data_dict['responses'][0]['userList']

    except Exception as ex:
        executors = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    if not author:
        author = ""

    executors.insert(0, {'Ссылка': '', 'Наименование': 'Все'})

    return render(request, 'dmtaskstouser.html', locals())


def dmtasksfromuser(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    dmid = request.GET.get('id')

    executor = request.GET.get('executor')

    if dmid == '1':
        cur_dmbase = user.dmbase
        cur_dbuser = user.dmuser
    else:
        cur_dmbase = user.dmbase2
        cur_dbuser = user.dmuser2

    server_address = cur_dmbase + "/hs/unido/req?request=getTaskList&author=" + cur_dbuser

    data = []
    data.append({'request': 'getTaskList',
                 'parameters': {'author': cur_dbuser, 'executor': executor}})

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']), json=data).json()

        tasks_list = data_dict['responses'][0]['getTaskList']

    except Exception as ex:
        tasks_list = list()
        data_dict = str(sys.exc_info())

    for tl in tasks_list:
        if tl['Дата']:
            tl['Дата'] = datetime.datetime.strptime(tl['Дата'][:8], "%Y%m%d")
        if tl['СрокИсполнения']:
            tl['СрокИсполнения'] = datetime.datetime.strptime(tl['СрокИсполнения'][:8], "%Y%m%d")

    from_user = True

    server_address = cur_dmbase + "/hs/unido/req?request=userList"

    res = dict()

    res['result'] = True

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()

        executors = data_dict['responses'][0]['userList']

    except Exception as ex:
        executors = list()
        res['message'] = str(sys.exc_info())
        res['result'] = False

    if not executor:
        executor = ""

    executors.insert(0, {'Ссылка': '', 'Наименование': 'Все'})

    return render(request, 'dmtaskstouser.html', locals())


def dmtask(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    dmid = request.GET.get('dmid')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if dmid == '1':
        cur_dmbase = user.dmbase
        cur_dbuser = user.dmuser
    else:
        cur_dmbase = user.dmbase2
        cur_dbuser = user.dmuser2

    server_address = cur_dmbase + "/hs/unido/req?request=getTask&ref=" + request.GET.get('id')

    may_exec = False

    try:

        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()

        task = data_dict['responses'][0]['getTask']

        may_exec = (dmid == '1' and user.dmuser == task['ТекущийИсполнительСтрокой']) or (
                dmid == '2' and user.dmuser2 == task['ТекущийИсполнительСтрокой'])

    except Exception as ex:
        task = dict()
        data_dict = str(sys.exc_info())

    return render(request, 'dmtask.html', locals())


def adddmtask(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':

        name = request.POST['name']
        description = request.POST['description']
        executor = request.POST['executor']

        dmid = request.POST.get('dmid')

        if dmid == '1':
            cur_dmbase = user.dmbase
            cur_dbuser = user.dmuser
        else:
            cur_dmbase = user.dmbase2
            cur_dbuser = user.dmuser2

        server_address = user.dmbase + "/hs/unido/req?request=newTask&name=" + name + "&description=" + description
        server_address = cur_dmbase + "/hs/unido/req"

        data = []
        data.append({'request': 'newTask', 'parameters': {'author': cur_dbuser, 'executor': executor, 'name': name,
                                                          'description': description}})

        res = dict()

        res['result'] = True

        try:

            data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']), json=data).json()

            tasks_list = data_dict['responses'][0]['newTask']

        except Exception as ex:
            tasks_list = list()
            res['message'] = str(sys.exc_info())
            res['result'] = False

        return JsonResponse(res)

    else:

        dmid = request.GET.get('dmid')

        if dmid == '1':
            cur_dmbase = user.dmbase
            cur_dbuser = user.dmuser
        else:
            cur_dmbase = user.dmbase2
            cur_dbuser = user.dmuser2

        server_address = cur_dmbase + "/hs/unido/req?request=userList"

        res = dict()

        res['result'] = True

        try:

            data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()

            executors = data_dict['responses'][0]['userList']

        except Exception as ex:
            executors = list()
            res['message'] = str(sys.exc_info())
            res['result'] = False

        return render(request, 'adddmtask.html', locals())


def ctrinfo(request):
    id1c = request.GET.get('id')

    server_address = AUTH_DATA['addr'] + "/hs/dta/obj" + "?request=getContractorInfo&Contractor=" + id1c

    contractor_info = dict()
    try:
        data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()
    except Exception:
        data_dict = {'success': False, 'responses': [{'getContractorInfo': str(sys.exc_info())}]}

    if data_dict.get('success') == True:
        contractor_info = data_dict.get('responses')[0].get('getContractorInfo')

    return render(request, 'ctrinfo.html', locals())


def tmchange(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = bitrix_address + 'timeman.status?user_id=' + str(user.idbitrix)

    data_dict = requests.get(server_address).json()

    tm_status = data_dict['result']['STATUS']
    tm_method = ''
    if tm_status == 'CLOSED' or tm_status == 'PAUSED':
        tm_method = 'open'
    elif tm_status == 'OPENED':
        tm_method = 'close'

    if tm_method == 'close':

        return render(request, 'dayreport.html', locals())

    elif tm_method != '':
        server_address = bitrix_address + 'timeman.' + tm_method + '?user_id=' + str(user.idbitrix)

        data_dict = requests.get(server_address).json()

    return redirect('/')


def leads(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = bitrix_address + 'crm.lead.list?filter[ASSIGNED_BY_ID]=' \
                     + str(user.idbitrix) + '&filter[STATUS_SEMANTIC_ID]=P' \
                     + '&order[DATE_CREATE]=desc'

    data_dict = requests.get(server_address).json()

    elements = data_dict['result']

    return render(request, 'leads.html', locals())


def lead(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = bitrix_address + 'crm.lead.get?id=' + request.GET['id']

    data_dict = requests.get(server_address).json()

    item = data_dict['result']

    return render(request, 'lead.html', locals())


def companies(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = bitrix_address + 'crm.company.list?filter[ASSIGNED_BY_ID]=' \
                     + str(user.idbitrix) + '&order[TITLE]=asc'  # + '&filter[REAL_STATUS]=2'

    data_dict = requests.get(server_address).json()

    elements = data_dict['result']

    return render(request, 'companies.html', locals())


def company(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = bitrix_address + 'crm.company.get?id=' + request.GET['id']

    data_dict = requests.get(server_address).json()

    item = data_dict['result']

    # comments = requests.get(bitrix_address + 'task.commentitem.getlist?id=' + task['id']).json()['result']

    return render(request, 'company.html', locals())


def tasks(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = bitrix_address + 'tasks.task.list?filter[responsible_id]=' + str(
        user.idbitrix) + '&filter[REAL_STATUS]=2'

    data_dict = requests.get(server_address).json()

    elements = data_dict['result']['tasks']
    # for el in data_dict['result']['tasks']:
    #     task_info = dict()
    #     task_info['id'] = el['id']

    return render(request, 'tasks.html', locals())


def task(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = bitrix_address + 'tasks.task.get?id=' + request.GET['id']

    data_dict = requests.get(server_address).json()

    task = data_dict['result']['task']

    comments = requests.get(bitrix_address + 'task.commentitem.getlist?id=' + task['id']).json()['result']

    return render(request, 'task.html', locals())


def savecomment(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':
        id = request.POST['id']
        comment = request.POST['comment']

        # task.commentitem.add?taskId = 36 & fields[AUTHOR_ID] = 25 & fields[POST_MESSAGE] = HELLO

        comments = requests.get(bitrix_address + 'task.commentitem.add?taskId=' + id + '&fields[AUTHOR_ID]=' + str(
            cu.idbitrix) + '&fields[POST_MESSAGE]=' + comment).json()['result']

        #     co = Order.objects.create(user=cu, contractor=cc, comments=comment)
        #
        #     for el in elements:
        #         cpo = ProductInOrder.objects.create(order=co, product=el.product, quantity=el.quantity)
        #
        #         ProductInBasket.objects.filter(user1c=cu, product=el.product).delete()
        #
        res = dict()

        res['id'] = id
        res['comment'] = comment

        return JsonResponse(res)
    #
    # else:
    #
    #     form = OrderForm(request.POST or None)
    #     return render(request, 'orders/checkout.html', locals())


def savedmcomment(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':
        id = request.POST['id']
        comment = request.POST['comment']

        dmid = request.POST.get('dmid')

        if dmid == '1':
            cur_dmbase = user.dmbase
            cur_dbuser = user.dmuser
        else:
            cur_dmbase = user.dmbase2
            cur_dbuser = user.dmuser2

        server_address = cur_dmbase + "/hs/unido/req"

        data = []
        data.append({'request': 'saveTaskComment', 'parameters': {'id': id, 'comment': comment}})

        res = dict()

        res['result'] = True

        try:

            data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd']), json=data).json()

            tasks_list = data_dict['responses'][0]['saveTaskComment']

        except Exception as ex:
            tasks_list = list()
            res['message'] = str(sys.exc_info())
            res['result'] = False

        return JsonResponse(res)


def add_to_report(now, user, pwd, idbitrix, report):
    res = "000"

    s = Service('C:\\Users\\MihailAdmin\\PycharmProjects\\tm03\\tm03\\chromedriver\\chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()

    wait = WebDriverWait(driver, 500)

    url = 'https://bitrix.apx-service.ru/'

    try:
        driver.get(url)
        elem = driver.find_element(by=By.NAME, value="USER_LOGIN")
        elem.clear()
        elem.send_keys(user)
        elem = driver.find_element(by=By.NAME, value="USER_PASSWORD")
        elem.clear()
        elem.send_keys(pwd)

        elem = driver.find_element(By.CLASS_NAME, 'login-btn')
        elem.click()

        wait.until(EC.presence_of_element_located((By.ID, "timeman-container")))

        driver.get('https://bitrix.apx-service.ru/timeman/timeman.php')

        fcn = 'js-' + str(idbitrix) + '_' + str(now.year) + '-' + format(now.month, '02d') + '-' + format(now.day,
                                                                                                          '02d')

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, fcn)))

        elems = driver.find_elements(By.CLASS_NAME, fcn)
        if elems:
            elems[0].click()

        fcn = 'side-panel-iframe'

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, fcn)))

        spi = driver.find_element(By.CLASS_NAME, fcn)

        driver.switch_to.frame(spi)

        fcn = 'feed-com-add-box-outer'

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, fcn)))

        cur_elem = driver.find_element(By.CLASS_NAME, fcn)

        cur_elem.location_once_scrolled_into_view

        wait.until(EC.element_to_be_clickable(cur_elem))

        cur_elem.click()

        cur_elem.location_once_scrolled_into_view

        fcn = 'bx-editor-iframe'

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, fcn)))

        driver.switch_to.frame(driver.find_element(By.CLASS_NAME, fcn))

        wait.until(EC.element_to_be_clickable((By.TAG_NAME, "body")))

        elem = driver.find_element(By.TAG_NAME, "body")
        elem.send_keys(report)

        driver.switch_to.default_content()

        driver.switch_to.frame(spi)
        send_btns = driver.find_element(By.CLASS_NAME, 'feed-add-post-buttons')
        send_btn = send_btns.find_element(By.XPATH, '//button[contains(@class, "ui-btn ui-btn-sm ui-btn-primary")]')
        send_btn.click()

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    return res


def add_to_report_thread(report_date, user_name, report):
    user = Users1c.objects.filter(name=user_name).all().get()

    add_to_report(report_date, user.name, user.pwd, user.idbitrix, report)

    return True


def savecommentreport(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':

        server_address = bitrix_address + 'timeman.close?user_id=' + str(user.idbitrix)

        data_dict = requests.get(server_address).json()

        if data_dict['result'] and data_dict['result']['TIME_FINISH']:
            comment = request.POST['comment']

            report_date = datetime.datetime(2022, 1, 1).strptime(data_dict['result']['TIME_FINISH'][0:10], "%Y-%m-%d")

            x = threading.Thread(target=add_to_report_thread, args=(report_date, user.name, comment))
            x.start()

            res = dict()

            res['comment'] = comment

            return JsonResponse(res)


def executetask(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':
        id = request.POST['id']

        comments = requests.get(bitrix_address + 'tasks.task.complete?taskId=' + id).json()['result']

        res = dict()

        res['id'] = id

        return JsonResponse(res)


def executedmtask(request):
    if 'userLogged' not in request.session:
        return render(request, 'login.html', locals())

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    if request.method == 'POST':
        id = request.POST['id']

        dmid = request.POST.get('dmid')

        if dmid == '1':
            cur_dmbase = user.dmbase
            cur_dbuser = user.dmuser
        else:
            cur_dmbase = user.dmbase2
            cur_dbuser = user.dmuser2

        server_address = cur_dmbase + "/hs/unido/req?request=executeTask&id=" + id

        res = dict()

        res['result'] = True

        try:

            data_dict = requests.get(server_address, auth=(AUTH_DATA['user'], AUTH_DATA['pwd'])).json()

            tasks_list = data_dict['responses'][0]['executeTask']

        except Exception as ex:
            tasks_list = list()
            res['message'] = str(sys.exc_info())
            res['result'] = False

        return JsonResponse(res)


def signout(request):
    request.session.pop('userLogged')
    return redirect('login')


def upload(request):
    res = {'users': [], 'contractors': [], 'products': [], 'all': list(), 'success': False}
    if request.method == 'GET':
        return HttpResponse(content=json.dumps(res))
    elif request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
        except:
            data_dict = {}

        if type(data_dict) == type(list()):
            res['all'] = upload_all(data_dict)
        else:
            if 'users' in data_dict:
                res['users'] = upload_users(data_dict['users'])

            if 'contractors' in data_dict:
                res['contractors'] = upload_contractors(data_dict['contractors'])

            if 'products' in data_dict:
                res['products'] = upload_products(data_dict['products'])

        res['success'] = True

        return HttpResponse(content=json.dumps(res))


def upload_all(data_dict):
    res = list()
    for el in data_dict:

        if el['Тип'] == 'Справочник':

            if el['Вид'] == 'Номенклатура':

                qp = Products.objects.filter(id1c__exact=el['Ссылка']).all()
                if len(qp) == 0:
                    Products.objects.create(article=el['Реквизиты']['Артикул'], name=el['Наименование'],
                                            fullname=el['Реквизиты']['НаименованиеПолное'],
                                            sfullname=el['Реквизиты']['НаименованиеПолное'].lower(),
                                            is_group=el['ЭтоГруппа'], is_deleted=el['ПометкаУдаления'],
                                            id1c=el['Ссылка'])
                else:
                    cp = qp.get()
                    cp.article = el['Реквизиты']['Артикул']
                    cp.name = el['Наименование']
                    cp.fullname = el['Реквизиты']['НаименованиеПолное']
                    cp.sfullname = el['Реквизиты']['НаименованиеПолное'].lower()
                    cp.is_group = el['ЭтоГруппа']
                    cp.is_deleted = el['ПометкаУдаления']
                    cp.save()

                res.append(el['Ссылка'])

            elif el['Вид'] == 'ХарактеристикиНоменклатуры':

                qp = Characteristics.objects.filter(id1c__exact=el['Ссылка']).all()
                if len(qp) == 0:
                    Characteristics.objects.create(name=el['Наименование'],
                                            is_deleted=el['ПометкаУдаления'],
                                            id1c=el['Ссылка'],
                                            owner_id1c=el['Владелец']['Ссылка'])
                else:
                    cp = qp.get()
                    cp.name = el['Наименование']
                    cp.is_deleted = el['ПометкаУдаления']
                    cp.owner_id1c = el['Владелец']['Ссылка']
                    cp.save()

                res.append(el['Ссылка'])

            elif el['Вид'] == 'Склады':

                qp = Warehouses.objects.filter(id1c__exact=el['Ссылка']).all()
                if len(qp) == 0:
                    Warehouses.objects.create(name=el['Наименование'],
                                              sname=el['Наименование'].lower(),
                                            is_group=el['ЭтоГруппа'], 
                                            is_deleted=el['ПометкаУдаления'],
                                            id1c=el['Ссылка'])
                else:
                    cp = qp.get()
                    cp.name = el['Наименование']
                    cp.sname = el['Наименование'].lower()
                    cp.is_group = el['ЭтоГруппа']
                    cp.is_deleted = el['ПометкаУдаления']
                    cp.save()

                res.append(el['Ссылка'])

            elif el['Вид'] == 'СкладскиеЯчейки':

                qp = WarehouseCells.objects.filter(id1c__exact=el['Ссылка']).all()
                if len(qp) == 0:
                    cp = WarehouseCells.objects.create(code=el['Код'],
                                                name=el['Наименование'],
                                              sname=el['Наименование'].lower(),
                                            is_group=el['ЭтоГруппа'], 
                                            is_deleted=el['ПометкаУдаления'],
                                            id1c=el['Ссылка'],
                                            warehouse_id1c=el['Владелец']['Ссылка'], section='', line='', rack='', stage='', position='')
                else:
                    cp = qp.get()
                    cp.code = el['Код']
                    cp.name = el['Наименование']
                    cp.sname = el['Наименование'].lower()
                    cp.is_group = el['ЭтоГруппа']
                    cp.is_deleted = el['ПометкаУдаления']
                    cp.warehouse_id1c=el['Владелец']['Ссылка']
                    cp.save()

                if el['Реквизиты']:
                    cp.section=el['Реквизиты']['Секция']
                    cp.line=el['Реквизиты']['Линия']
                    cp.rack=el['Реквизиты']['Стеллаж']
                    cp.stage=el['Реквизиты']['Ярус']
                    cp.position=el['Реквизиты']['Позиция']
                    cp.save()
                    
                res.append(el['Ссылка'])

            elif el['Вид'] == 'Контрагенты':

                qp = Contractors.objects.filter(id1c__exact=el['Ссылка']).all()
                if len(qp) == 0:
                    Contractors.objects.create(name=el['Наименование'], sname=el['Наименование'].lower(),
                                               inn=el['Реквизиты']['ИНН'], kpp=el['Реквизиты']['КПП'],
                                               id1c=el['Ссылка'])
                else:
                    cp = qp.get()
                    cp.name = el['Наименование']
                    cp.sname = el['Наименование'].lower()
                    cp.inn = el['Реквизиты']['ИНН']
                    cp.kpp = el['Реквизиты']['КПП'].lower()
                    cp.save()

                res.append(el['Ссылка'])

            elif el['Вид'] == 'Валюты':

                qp = Currency.objects.filter(code__exact=el['Код']).all()
                if len(qp) == 0:
                    Currency.objects.create(code=el['Код'], name=el['Наименование'])
                else:
                    cp = qp.get()
                    cp.code = el['Код']
                    cp.name = el['Наименование']
                    cp.save()

                res.append(el['Ссылка'])

        elif el['Тип'] == 'Документ':

            if el['Вид'] == 'ПолучениеПодотчетнымЛицомОплатыОтПокупателя':

                cd = datetime.datetime(int(el['Дата'][0:4]), int(el['Дата'][4:6]), int(el['Дата'][6:8]),
                                       int(el['Дата'][8:10]), int(el['Дата'][10:12]), int(el['Дата'][12:14]))

                ods = el['Реквизиты']['ДатаЗаказа']
                if ods == '':
                    od = datetime.datetime(1970, 1, 1)
                else:
                    od = datetime.datetime(int(ods[0:4]), int(ods[4:6]), int(ods[6:8]),
                                           int(ods[8:10]), int(ods[10:12]), int(ods[12:14]))

                cc = Contractors.objects.filter(id1c__exact=el['Реквизиты']['Контрагент']['Ссылка']).all().get()
                qu = Users1c.objects.filter(id1c__exact=el['Реквизиты']['Пользователь']['Ссылка']).all()

                if len(qu) == 0:
                    сu = Users1c.objects.create(name=el['Реквизиты']['Пользователь']['Наименование'].lower(), pwd='',
                                                id1c=el['Реквизиты']['Пользователь']['Ссылка'])
                else:
                    cu = qu.get()

                ccu = Currency.objects.filter(code__exact=el['Реквизиты']['Валюта']['Код']).all().get()

                qp = AcceptCash.objects.filter(id1c__exact=el['Ссылка']).all()
                if len(qp) == 0:
                    AcceptCash.objects.create(delivered1c=True, user=cu, contractor=cc, currency=ccu,
                                              sum=el['Реквизиты']['Сумма'], comments=el['Реквизиты']['Комментарий'],
                                              order_number=el['Реквизиты']['НомерЗаказа'], order_date=od,
                                              is_deleted=el['ПометкаУдаления'],
                                              created=cd, id1c=el['Ссылка'])
                else:
                    cp = qp.get()
                    cp.user = cu
                    cp.contractor = cc
                    cp.currency = ccu
                    cp.sum = el['Реквизиты']['Сумма']
                    cp.comments = el['Реквизиты']['Комментарий']
                    cp.order_number = el['Реквизиты']['НомерЗаказа']
                    cp.order_date = od
                    cp.created = cd
                    cp.delivered1c = True
                    cp.is_deleted = el['ПометкаУдаления']
                    cp.save()

                res.append(el['Ссылка'])

    return res


def upload_users(musers):
    count = []
    for cu in musers:
        id1c = cu['Ид1с']
        q = Users1c.objects.filter(id1c__exact=id1c).all()
        if len(q) == 0:
            u = Users1c.objects.create(name=cu['ИмяПользователя'].lower(), pwd=cu['Пароль'], id1c=id1c)
        else:
            o = q.get()
            need_to_save = False
            if o.name != cu['ИмяПользователя'].lower():
                o.name = cu['ИмяПользователя'].lower()
                need_to_save = True
            if o.pwd != cu['Пароль']:
                o.pwd = cu['Пароль']
                need_to_save = True
            if need_to_save:
                o.save()

        count.insert(len(count), id1c)

    return count


def upload_contractors(musers):
    count = []
    for cu in musers:
        id1c = cu['Ид1с']
        q = Contractors.objects.filter(id1c__exact=id1c).all()
        if len(q) == 0:
            u = Contractors.objects.create(name=cu['Наименование'], sname=cu['Наименование'].lower(), inn=cu['ИНН'],
                                           kpp=cu['КПП'], id1c=id1c)
        else:
            o = q.get()
            need_to_save = False
            if o.name != cu['Наименование']:
                o.name = cu['Наименование']
                need_to_save = True
            if o.sname != cu['Наименование'].lower():
                o.sname = cu['Наименование'].lower()
                need_to_save = True
            if o.inn != cu['ИНН']:
                o.inn = cu['ИНН']
                need_to_save = True
            if o.kpp != cu['КПП']:
                o.kpp = cu['КПП']
                need_to_save = True
            if need_to_save:
                o.save()

        count.insert(len(count), id1c)

    return count


def upload_products(musers):
    count = []
    for cu in musers:
        id1c = cu['Ид1с']
        q = Products.objects.filter(id1c__exact=id1c).all()
        if len(q) == 0:
            u = Products.objects.create(article=cu['Артикул'], name=cu['Наименование'],
                                        fullname=cu['НаименованиеПолное'],
                                        sfullname=cu['НаименованиеПолное'].lower(), id1c=id1c)
        else:
            o = q.get()
            need_to_save = False
            if o.article != cu['Артикул']:
                o.article = cu['Артикул']
                need_to_save = True
            if o.name != cu['Наименование']:
                o.name = cu['Наименование']
                need_to_save = True
            if o.fullname != cu['НаименованиеПолное']:
                o.fullname = cu['НаименованиеПолное']
                need_to_save = True
            if o.sfullname != cu['НаименованиеПолное'].lower():
                o.sfullname = cu['НаименованиеПолное'].lower()
                need_to_save = True
            if need_to_save:
                o.save()

        count.insert(len(count), id1c)

    return count


def uploadtest(cur_request):
    url = 'http://localhost:8010/upload/'
    data = json.loads("""[
{
"Тип": "Документ",
"Вид": "ПолучениеПодотчетнымЛицомОплатыОтПокупателя",
"Ссылка": "80cb3d3d-cf5b-11eb-a994-000c29dbc4e3",
"ВерсияДанных": "AAAAAAALXpg=",
"Номер": "000000008",
"Дата": "20210611152815",
"Проведен": true,
"ПометкаУдаления": false,
"Реквизиты": {
"ПодотчетноеЛицо": {
"Тип": "Справочник",
"Вид": "ФизическиеЛица",
"Ссылка": "77f3c435-caa6-11eb-a994-000c29dbc4e3",
"ВерсияДанных": "AAAAAAAKMtc=",
"Код": "0000000048",
"Наименование": "Романовская Яна",
"ПометкаУдаления": false,
"ЭтоГруппа": false,
"Родитель": null
},
"Контрагент": {
"Тип": "Справочник",
"Вид": "Контрагенты",
"Ссылка": "ab8127e1-2a38-11eb-a994-000c29dbc4e3",
"ВерсияДанных": "AAAAAAANfbM=",
"Код": "Р4750    ",
"Наименование": "Самурай Сервис ООО",
"ПометкаУдаления": false,
"ЭтоГруппа": false,
"Родитель": {
"Тип": "Справочник",
"Вид": "Контрагенты",
"Ссылка": "860f5d60-14b5-11e9-9e2a-000c2934e816",
"ВерсияДанных": "AAAAAAAE2Ts=",
"Код": "Р3448    ",
"Наименование": "Евгений Локшин",
"ПометкаУдаления": false,
"ЭтоГруппа": true,
"Родитель": {
"Тип": "Справочник",
"Вид": "Контрагенты",
"Ссылка": "c18e6fd5-b84f-11e0-9a78-00155d7b7606",
"ВерсияДанных": "AAAAAAAE2JU=",
"Код": "133      ",
"Наименование": "ОПТ-РОССИЯ",
"ПометкаУдаления": false,
"ЭтоГруппа": true,
"Родитель": null
}
}
},
"Сумма": 13860,
"Валюта": {
"Тип": "Справочник",
"Вид": "Валюты",
"Ссылка": "8bc4bf19-7704-11e0-92c1-00155d7b7606",
"ВерсияДанных": "AAAAAAAC+/4=",
"Код": "643",
"Наименование": "руб",
"ПометкаУдаления": false,
"ЭтоГруппа": false,
"Родитель": null
},
"Автор": {
"Тип": "Справочник",
"Вид": "Пользователи",
"Ссылка": "a595de71-c922-11eb-a994-000c29dbc4e3",
"ВерсияДанных": "AAAAAAAKKw0=",
"Код": "",
"Наименование": "lkpo",
"ПометкаУдаления": false,
"ЭтоГруппа": false,
"Родитель": null
},
"Комментарий": "",
"НомерЗаказа": "",
"ДатаЗаказа": "",
"Пользователь": {
"Тип": "Справочник",
"Вид": "Пользователи",
"Ссылка": "b5eb09bd-caa6-11eb-a994-000c29dbc4e3",
"ВерсияДанных": "AAAAAAAKK4Q=",
"Код": "",
"Наименование": "Романовская Яна",
"ПометкаУдаления": false,
"ЭтоГруппа": false,
"Родитель": null
}
},
"ТабличныеЧасти": {}
}
]""")
    message = requests.post(url, json=data)
    return message.content


def checkout(request):
    return render(request, 'index.html', locals())
