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
from django.urls import path, re_path
from django.views.static import serve
from hsjusj.settings import MEDIA_ROOT

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('test/', views.test, name='test'),
    path('home/', views.home, name='home'),
    re_path('article/(?P<aid>\d+)/', views.article_info, name='article_info'),
    path('archives/', views.archives, name='archives'),
    path('search/', views.search, name='search'),
    path('search_tag/', views.search_tag, name='search_tag'),
    path('search_title/', views.search_title, name='search_title'),
    path('write/', views.write, name='write'),
    path('upload_img/', views.upload_img, name='upload_img'),
    path('submit/', views.submit, name='submit'),

    re_path('media/(?P<path>.*)/$', serve, {'document_root':MEDIA_ROOT}),

    path('selected/', views.selected),

    path('orm/', views.orm, name='orm'),
]
