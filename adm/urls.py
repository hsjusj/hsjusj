#coding=utf8

from django.urls import path,re_path
from adm import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('tags_editor/', views.tags_editor, name='tags_editor'),
    path('tag_editor/', views.tag_editor, name='tag_editor'),
    path('tag_del/', views.tag_del, name='tag_del'),

    path('articles_editor/', views.articles_editor, name='articles_editor'),
    re_path('article_editor/(?P<aid>\d+)/$', views.article_editor, name='article_editor'),
    path('article_del/', views.article_del, name='article_del'),

    path('article_write/', views.article_write, name='article_write'),
    path('submit/', views.submit, name='submit'),
]