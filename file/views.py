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

from reminder.models import Reminder

from .forms import *
from datetime import timezone, datetime, timedelta
import pytz 

import urllib.parse
import io
from django.http import FileResponse, HttpResponse
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


def gfbp(request):

    if 'userLogged' not in request.session:
        return redirect('login')
        
    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    filespath = 'I:\\Files\\'
    
    curUid = request.headers.get('id')
    pos = int(request.headers.get('pos'))

    if File.objects.filter(user=cu, idname=curUid).count() > 0:

        fo = File.objects.filter(user=cu, idname=curUid).all().get()

        frf = open(filespath + curUid + ".tmp",'rb')

        frf.seek(pos)

        part_size = 120000

        # fr = FileResponse(frf.read(part_size))
        
        # fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(fo.name.encode('utf8'))
        # fr['X-Sendfile'] = urllib.parse.quote(fo.name.encode('utf8'))

        return HttpResponse(frf.read(part_size), content_type='application/octet-stream')

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

        res = dict()
        res['success'] = True

        return JsonResponse(res)
                        
    elif request.method == 'GET':

        r_list = Reminder.objects.filter(user=cu, remind__gte=datetime.now()).order_by('remind').all()[:20]

        remind_list = list()

        for elr in r_list:
            remind_list.append({'remind': elr.remind, 'comments': elr.comments, 'fileid': elr.file.idname, 'filename': elr.file.name})

        parent_id = request.GET.get('parent_id')

        if not parent_id:

            parent_id = ""

        pathToFolder = []
        curparent_id = parent_id

        while curparent_id != '':
            parent = File.objects.filter(user=cu, idname=curparent_id, is_folder=True).all().get()
            pathToFolder.insert(0, {'name': parent.name, 'id': parent.idname})
            curparent_id = parent.parent_id

        pathToFolder.insert(0, {'name': '..', 'id': ''})


        affFolders = []

        allfiles = []

        search_file = request.GET.get('search_file')

        if search_file:



            lfiles = File.objects.filter(user=cu, is_folder=False, name__icontains=search_file, is_deleted=False, fileowner__isnull=True).order_by('-created').all()[:20]

        else:

            search_file = ''

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

            lfiles = File.objects.filter(user=cu,  parent_id=parent_id, is_folder=False, is_deleted=False, fileowner__isnull=True).order_by('-created').all()[:20]

        allfiles = list(lfiles)

        setStrSize(allfiles)

        if search_file:
            setFullPath(allfiles)


        return render(request, 'files.html', locals())


def setStrSize(allfiles):
    for f in allfiles:
        if f.size > 1024 * 1024 * 1024:
            f.size2 = str(round(f.size / (1024 * 1024 * 1024), 1)) + " Гб"

        elif f.size > 1024 * 1024:
            f.size2 = str(round(f.size / (1024 * 1024), 1)) + " Мб"

        elif f.size > 1024:
            f.size2 = str(round(f.size / (1024), 1)) + " Кб"

        else:
            f.size2 = str(f.size) + " б"

        f.size = locale.format_string('%.0f', f.size, grouping=False)

def setFullPath(allfiles):
    for f in allfiles:

        fullPath = ''
        curParentId = f.parent_id
        while curParentId != '':

            cp = File.objects.filter(idname=curParentId).all().get()

            fullPath = cp.name + '\\' + fullPath

            curParentId = cp.parent_id

        f.name = fullPath + f.name

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



def ul(request):

    filespath = 'I:\\Files\\'
    
    if request.method == 'POST':

        if 'userLogged' not in request.session:
            return redirect('login')

        res = dict()
        res['success'] = False

        cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

        eluid = request.POST.get('eluid')
        idname = request.POST.get('parentid')

        if File.objects.filter(user=cu, idname=idname).count() > 0:

            fo = File.objects.filter(user=cu, idname=idname).all().get()

            el = UploadlLink.objects.create(file=fo, idname=eluid)

            res['success'] = True

            
        return JsonResponse(res)


    elif request.method == 'GET':

        idname = request.GET.get('id')

        if UploadlLink.objects.filter(idname=idname).count() > 0:

            el = UploadlLink.objects.filter(idname=idname).all().get()

            if el.created.astimezone(pytz.timezone('Europe/Moscow')) > (datetime.now().astimezone(pytz.timezone('Europe/Moscow')) - timedelta(hours=24)):

                lfiles = File.objects.filter(parent_id=el.file.idname, is_deleted=False).order_by('-created').all()[:20]

                jlfiles = list()

                for  lf in lfiles:
                    jlfiles.append({'filename': lf.name, 'size': int(lf.size), 'created': lf.created.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y%m%d%H%M%S')})

                return JsonResponse({'success': True, 'files': jlfiles})

            else:
                
                return render(request, '404.html')

        else:

            return render(request, '404.html')

def ulbyparentid(request):

    parent_id = request.GET.get('parent_id')

    res = dict()
    res['success'] = True

    if File.objects.filter(idname=parent_id).count() > 0:
        
        fo = File.objects.filter(idname=parent_id).all().get()

        if UploadlLink.objects.filter(file=fo).count() > 0:

            el = UploadlLink.objects.filter(file=fo).order_by('-created').all()[:1].get()

            if el.created.astimezone(pytz.timezone('Europe/Moscow')) > (datetime.now().astimezone(pytz.timezone('Europe/Moscow')) - timedelta(hours=24)):

                res['id'] = el.idname
                res['enabled'] = (el.created.astimezone(pytz.timezone('Europe/Moscow')) + timedelta(hours=24)).strftime("%d.%m.%Y %H:%M:%S")
            
    return JsonResponse(res)


def ulgf(request):

    filespath = 'I:\\Files\\'
    
    if request.method == 'POST':

        reqjs = json.loads(request.body)

        res = dict()
        res['success'] = False

        if reqjs['mode'] == 'getuid':

            if UploadlLink.objects.filter(idname=reqjs['ulid']).count() > 0:

                ulo = UploadlLink.objects.filter(idname=reqjs['ulid']).all().get()

                
                fo = File.objects.create(user=ulo.file.user, parent_id=ulo.file.idname, name=urllib.parse.unquote(reqjs['filename']))

                res['success'] = True
                res['id'] = fo.idname

        elif reqjs['mode'] == 'setsize':

            if File.objects.filter(idname=reqjs['id']).count() > 0:

                fo = File.objects.filter(idname=reqjs['id']).all().get()

                fo.size = fo.size + int(reqjs['size'])

                fo.save()

                res['success'] = True
                res['id'] = fo.idname
                res['size'] = fo.size
            
        return JsonResponse(res)


    elif request.method == 'GET':

        idname = request.GET.get('id')

        if UploadlLink.objects.filter(idname=idname).count() > 0:

            el = UploadlLink.objects.filter(idname=idname).all().get()

            if el.created.astimezone(pytz.timezone('Europe/Moscow')) > (datetime.now().astimezone(pytz.timezone('Europe/Moscow')) - timedelta(hours=1)):

                return JsonResponse({'success': True})

            else:
                
                return render(request, '404.html')

        else:

            return render(request, '404.html')


def eln(request):

    filespath = 'I:\\Files\\'
    
    if request.method == 'GET':

        idname = request.GET.get('id')

        if ExternalLink.objects.filter(idname=idname).count() > 0:

            el = ExternalLink.objects.filter(idname=idname).all().get()

            if el.created.astimezone(pytz.timezone('Europe/Moscow')) > (datetime.now().astimezone(pytz.timezone('Europe/Moscow')) - timedelta(hours=1)):

                fo = el.file

                fr = FileResponse(open(filespath + fo.idname + ".tmp",'rb'))

                fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(fo.name.encode('utf8'))
                fr['X-Sendfile'] = urllib.parse.quote(fo.name.encode('utf8'))



                return JsonResponse({'filename': fo.name, 'id': fo.idname, "size": fo.size})

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



