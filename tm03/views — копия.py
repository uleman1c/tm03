import json
from datetime import datetime

import requests
# from django.contrib.sites import requests
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect, render

from RequestHeaders.models import add_request_header
from accept_cash.models import AcceptCash
from contractors.models import Contractors
from currency.models import Currency
from products.models import Products
from users1c import models
from users1c.models import Users1c

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

bitrix_address = 'https://bitrix.apx-service.ru/rest/313/dgu8ygk1g6boen2p/'


def home(request):
    if 'userLogged' not in request.session:
        return redirect('login')

    user = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    server_address = bitrix_address + 'timeman.status?user_id=' + str(user.idbitrix)

    data_dict = requests.get(server_address).json()

    tm_status = data_dict['result']['STATUS']
    if tm_status == 'CLOSED':
        tm_status_str = 'Начать'
    elif tm_status == 'OPENED':
        tm_status_str = 'Завершить'
    elif tm_status == 'EXPIRED':
        tm_status_str = 'Истек'

    mobile_mode = add_request_header(request)

    return render(request, 'index.html', locals())


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

        fcn = 'js-' + str(idbitrix) + '_' + str(now.year) + '-' + format(now.month, '02d') + '-' + format(now.day, '02d')

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

                cd = datetime(int(el['Дата'][0:4]), int(el['Дата'][4:6]), int(el['Дата'][6:8]),
                              int(el['Дата'][8:10]), int(el['Дата'][10:12]), int(el['Дата'][12:14]))

                ods = el['Реквизиты']['ДатаЗаказа']
                if ods == '':
                    od = datetime(1970, 1, 1)
                else:
                    od = datetime(int(ods[0:4]), int(ods[4:6]), int(ods[6:8]),
                                  int(ods[8:10]), int(ods[10:12]), int(ods[12:14]))

                cc = Contractors.objects.filter(id1c__exact=el['Реквизиты']['Контрагент']['Ссылка']).all().get()
                cu = Users1c.objects.filter(id1c__exact=el['Реквизиты']['Пользователь']['Ссылка']).all().get()
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
