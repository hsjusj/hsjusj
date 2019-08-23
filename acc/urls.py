#coding=utf8

from django.urls import path, re_path
from acc import views

urlpatterns = [
    path('login/', views.login, name='acc_login'),
]