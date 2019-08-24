from django.shortcuts import render, redirect, HttpResponse
from django.template.response import TemplateResponse
from adm import models
from blog.models import Articles, Tags, ArticlesToTags
from acc.models import User, Request, RegisterCode
import json
import time
import datetime
import random

# Create your views here.

def login(request):
    if request.method == 'GET':
        locked = None
        obj = models.adm.objects.filter(id=1).first()
        if datetime.datetime.now() < obj.lock_datetime:
            locked = True
        return render(request, 'view/adm/login.html', {'locked':locked})
    elif request.method == 'POST':
        msg = {}
        pwd = request.POST.get('pwd', None)
        print("pwd", pwd)
        if pwd == '123123':
            models.adm.objects.filter(id=1).update(fail_count=0)
            #设置为当前时间
            models.adm.objects.filter(id=1).update(lock_datetime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            request.session['login'] = True
            request.session.set_expiry(0)
            msg['status'] = True
            return HttpResponse(json.dumps(msg))
        else:
            obj = models.adm.objects.filter(id=1).first()
            fail_count = obj.fail_count + 1
            msg['count'] = 5 - fail_count
            msg['status'] = False
            if fail_count == 5:
                models.adm.objects.filter(id=1).update(fail_count=0)
                fail_count = 0
                #锁60秒
                lock_datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() + 7))
                models.adm.objects.filter(id=1).update(lock_datetime=lock_datetime)
            else:
                models.adm.objects.filter(id=1).update(fail_count=fail_count)
            return HttpResponse(json.dumps(msg))

def tags_editor(request):
    if request.session.get('login', None):
        if request.method == 'GET':
            tags = Tags.objects.all()
            return render(request, 'view/adm/tags_editor.html', {'tags':tags})
        elif request.method == 'POST':
            tags = Tags.objects.all()
            return TemplateResponse(request, 'response/adm/tags_editor_response.html', {'tags':tags})
    else:
        return redirect('/hsjusj/login')

def tag_editor(request):
    if request.method == 'POST':
        if request.session.get('login', None):
            tid = request.POST.get('tid', None)
            new_tag_name = request.POST.get('new_tag_name', None)
            Tags.objects.filter(tid=tid).update(tag_name=new_tag_name)
            return HttpResponse(json.dumps({'status':True}))
        else:
            return HttpResponse(json.dumps({'status':False}))

def tag_del(request):
    if request.session.get('login', None):
        if request.method == 'POST':
            tid = request.POST.get("tid")
            Tags.objects.filter(tid=tid).delete()
            return HttpResponse(json.dumps({'status':True}))
        else:
            return HttpResponse(json.dumps({'status':False}))

def articles_editor(request):
    if request.session.get('login', None):
        if request.method == 'GET':
            articles = Articles.objects.all()
            return render(request, 'view/adm/articles_editor.html', {'articles':articles})
        elif request.method == "POST":
            articles = Articles.objects.all()
            return TemplateResponse(request, 'response/adm/articles_editor_response.html', {'articles':articles})
    else:
        return redirect('/hsjusj/login')

def article_editor(request, aid):
    if request.session.get('login', None):
        if request.method == 'GET':
            article = Articles.objects.filter(aid=aid).first()
            tags = Tags.objects.all()
            articletotags = ArticlesToTags.objects.filter(article_id=aid)
            for articletotag in articletotags:
                print(articletotag.tag_id)
            return render(request, 'view/adm/article_editor.html', {'aid':aid, 'article':article, 'tags':tags, 'articletotags':articletotags})
        elif request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            tids = request.POST.getlist('tids[]')
            new_tags = request.POST.getlist('new_tags[]')
            Articles.objects.filter(aid=aid).update(title=title, content=content)
            ArticlesToTags.objects.filter(article_id=aid).delete()
            for tid in tids:
                ArticlesToTags.objects.create(article_id=aid, tag_id=tid)
            for new_tag in new_tags:
                if not Tags.objects.filter(tag_name=new_tag).exists():
                    tag_obj = Tags.objects.create(tag_name=new_tag)
                    ArticlesToTags.objects.create(article_id=aid, tag_id=tag_obj.tid)
            return HttpResponse(json.dumps({'status':True}))

def article_del(request):
    if request.session.get('login', None):
        if request.method == 'POST':
            aid = request.POST.get('aid', None)
            Articles.objects.filter(aid=aid).delete()
            return HttpResponse(json.dumps({'status':True}))
        else:
            return HttpResponse(json.dumps({'status':False}))

def article_write(request):
    if request.session.get('login',None):
        if request.method == 'GET':
            tags = Tags.objects.all()
            return render(request, 'view/adm/write.html', {'tags': tags})

def acc(request):
    if request.session.get('login', None):
        if request.method == 'GET':
            registercodes = RegisterCode.objects.all()
            users = User.objects.all()
            return render(request, 'view/adm/acc.html', {'registercodes':registercodes, 'users':users})
        elif request.method == 'POST':
            registercodes = RegisterCode.objects.all()
            users = User.objects.all()
            print("PJAX")
            return TemplateResponse(request, 'response/adm/acc_response.html', {'registercodes': registercodes, 'users': users})

def code_add(request):
    if request.session.get('login', None):
        if request.method == 'POST':
            code = ''
            l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            status = True
            while status:
                for i in range(0, 18):
                    code += str(random.choice(l))
                if RegisterCode.objects.filter(code=code).exists():
                    continue
                else:
                    status = False
                    RegisterCode.objects.create(code=code)
            return HttpResponse(json.dumps({'status':True}))

def code_del(request):
    if request.session.get('login', None):
        if request.method == 'POST':
            id = request.POST.get('id')
            RegisterCode.objects.filter(id=id).delete()
            return HttpResponse(json.dumps({'status':True}))

def submit(request):
    if request.method == "POST":
        title = request.POST.get("title", None)
        content = request.POST.get("content", None)
        tids = request.POST.getlist("tids[]", None)
        new_tags = request.POST.getlist("new_tags[]", None)
        print("dict:", request.POST)
        print("title:", title)
        print("content:", content)
        print("tids:", tids)
        print("new_tags:", new_tags)
        #new article----------------------------------
        new_article = Articles.objects.create(title=title, content=content)
        #new tag--------------------------------------
        for new_tag in new_tags:
            is_exist = Tags.objects.filter(tag_name=new_tag).exists()
            if not is_exist:
                tid = Tags.objects.create(tag_name=new_tag).tid
                ArticlesToTags.objects.create(article_id=new_article.aid, tag_id=tid)
        #tag--------------------------------------
        for tid in tids:
            ArticlesToTags.objects.create(article_id=new_article.aid, tag_id=tid)
        return HttpResponse("SUBMIT")