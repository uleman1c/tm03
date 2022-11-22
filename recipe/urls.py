"""test_project URL Configuration

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
from django.urls import path

from recipe import views

urlpatterns = [
    # path('', views.home, name='he'),
    path('recipes/', views.recipes, name='recipes'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('sendto1c_recipe/', views.sendto1c_recipe, name='sendto1c_recipe'),
    path('leftovers/', views.leftovers, name='leftovers'),
    path('reqexec/', views.reqexec, name='reqexec'),
    path('getleftovers/', views.getleftovers, name='getleftovers'),
    path('outcome/', views.outcome, name='outcome'),
    path('getOutcome/', views.getoutcome, name='getoutcome'),
    path('prnform/', views.prnform, name='prnform'),
            ]
