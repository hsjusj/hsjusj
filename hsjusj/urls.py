"""hsjusj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from hsjusj.settings import MEDIA_ROOT

from blog import views

urlpatterns = [
    path('adm/', admin.site.urls),
    #主页
    path('home/', views.home, name='home'),
    #文章详情页
    re_path('article/(?P<aid>\d+)/', views.article_info, name='article'),
    #归档页
    path('archives/', views.archives, name='archives'),
    #搜索页
    path('search/', views.search, name='search'),
    #处理标签筛选请求
    path('search_tag/', views.search_tag, name='search_tag'),
    #处理标题搜索请求
    path('search_title/', views.search_title, name='search_title'),

    #about页
    path('about/', views.about, name='about'),

    #资源地址
    re_path('media/(?P<path>.*)/$', serve, {'document_root':MEDIA_ROOT}),

    #selected测试
    path('selected/', views.selected),

    #adm app(后台)
    path('hsjusj/', include('adm.urls')),
]
