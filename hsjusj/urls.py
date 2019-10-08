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
    path('admin/', admin.site.urls),

    # 资源地址
    re_path('media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),

    #博客主页
    path('hsjusj/', include('blog.urls', namespace='blog')),
    #adm app(后台)
    path('adm/', include('adm.urls')),
]
