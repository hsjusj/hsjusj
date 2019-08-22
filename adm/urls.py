#coding=utf8

from django.urls import path
from adm import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
]