"""tm03 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from tm03 import views, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signout/', views.signout, name='signout'),
    path('tmchange/', views.tmchange, name='tmchange'),
    path('ctrinfo/', views.ctrinfo, name='ctrinfo'),
    path('tasks/', views.tasks, name='tasks'),
    path('task/', views.task, name='task'),
    path('leads/', views.leads, name='leads'),
    path('lead/', views.lead, name='lead'),
    path('companies/', views.companies, name='companies'),
    path('company/', views.company, name='company'),
    path('dm/', views.dm, name='dm'),
    path('dmtaskstouser/', views.dmtaskstouser, name='dmtaskstouser'),
    path('dmtasksfromuser/', views.dmtasksfromuser, name='dmtasksfromuser'),
    path('dmtask/', views.dmtask, name='dmtask'),
    path('adddmtask/', views.adddmtask, name='adddmtask'),
    path('savecomment/', views.savecomment, name='savecomment'),
    path('savedmcomment/', views.savedmcomment, name='savedmcomment'),
    path('savecommentreport/', views.savecommentreport, name='savecommentreport'),
    path('executetask/', views.executetask, name='executetask'),
    path('executedmtask/', views.executedmtask, name='executedmtask'),
    path('upload/', views.upload, name='upload'),
    path('uploadtest/', views.uploadtest, name='uploadtest'),
    path('lp/', views.lp, name='lp'),
    path('lpl/', views.lpl, name='lpl'),
    path('lpl2/', views.lpl2, name='lpl2'),
    path('sha1/', views.sha1, name='sha1'),
    path('bitrixwh/', views.bitrixwh, name='bitrixwh'),
    path('skladthr/', views.skladthr, name='skladthr'),
    path('savesdek/', views.savesdek, name='savesdek'),
    path('sdekreqs/', views.sdekreqs, name='sdekreqs'),
    path('containerstatuses/', views.containerstatuses, name='containerstatuses'),
    path('fileversions/', views.fileversions, name='fileversions'),
    path('tchystory/', views.tchystory, name='tchystory'),
    path('curencecuorses/', views.curencecuorses, name='curencecuorses'),
    path('', include('users1c.urls')),
    path('', include('login.urls')),
    path('', include('contractors.urls')),
    path('', include('orders.urls')),
    path('', include('products.urls')),
    path('', include('accept_cash.urls')),
    path('', include('error_log.urls')),
    path('', include('tsd_log.urls')),
    path('', include('win_event_log.urls')),
    path('', include('bitrixqueue.urls')),
    path('', include('order_info.urls')),
    path('', include('invent.urls')),
    path('', include('file.urls')),
    path('', include('block_schema.urls')),
    path('', include('access_key.urls')),
    path('', include('reminder.urls')),
    path('', include('recipe.urls')),
]

              # + static(settings.STATIC_URL, document_root = os.path.join(settings.BASE_DIR, 'static'))
