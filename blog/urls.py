from django.urls import path, re_path
from . import views
from django.views.static import serve
from hsjusj.settings import MEDIA_ROOT

urlpatterns = [
    # 主页
    path('home/', views.home, name='home'),
    # 文章详情页
    re_path('article/(?P<aid>\d+)/', views.article_info, name='article'),
    # 归档页
    path('archives/', views.archives, name='archives'),
    # 搜索页
    path('search/', views.search, name='search'),
    # 处理标签筛选请求
    path('search_tag/', views.search_tag, name='search_tag'),
    # 处理标题搜索请求
    path('search_title/', views.search_title, name='search_title'),

    # about页
    path('about/', views.about, name='about'),

    # selected测试
    path('selected/', views.selected),
]