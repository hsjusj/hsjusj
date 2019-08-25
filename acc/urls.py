#coding=utf8

from django.urls import path, re_path
from acc import views

urlpatterns = [
    path('signup/', views.signup, name='acc_signup'),
    path('login/', views.login, name='acc_login'),
    path('index/', views.index, name='acc_index'),

    path('request_submit/', views.requset_submit, name='acc_request_submit'),
]