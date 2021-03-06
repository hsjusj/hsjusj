#coding=utf-8
from django.shortcuts import render, redirect, HttpResponse
from django.template.response import TemplateResponse
from adm import models
from blog.models import Articles, Tags, ArticlesToTags
import json, time, datetime, re

# Create your views here.

#记得加session验证，如果有cookie直接跳转进首页
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
        if pwd == models.adm.objects.filter(id=1).first().pwd:
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
                lock_datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() + 60))
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
        return redirect('/adm/login')

def tag_editor(request):
    if request.session.get('login', None):
        if request.method == 'POST':
            tid = request.POST.get('tid', None)
            new_tag_name = request.POST.get('new_tag_name', None)
            Tags.objects.filter(tid=tid).update(tag_name=new_tag_name)
            return HttpResponse(json.dumps({'status':True}))
    else:
        return redirect("/adm/login")

def tag_del(request):
    if request.session.get('login', None):
        if request.method == 'POST':
            tid = request.POST.get("tid")
            Tags.objects.filter(tid=tid).delete()
            return HttpResponse(json.dumps({'status':True}))
        else:
            return HttpResponse(json.dumps({'status':False}))
    else:
        return redirect("/adm/login")

def articles_editor(request):
    if request.session.get('login', None):
        if request.method == 'GET':
            articles = Articles.objects.all()
            return render(request, 'view/adm/articles_editor.html', {'articles':articles})
        elif request.method == "POST":
            articles = Articles.objects.all()
            return TemplateResponse(request, 'response/adm/articles_editor_response.html', {'articles':articles})
    else:
        return redirect('/adm/login')

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
    else:
        return redirect("/adm/login")

def article_del(request):
    if request.session.get('login', None):
        if request.method == 'POST':
            aid = request.POST.get('aid', None)
            Articles.objects.filter(aid=aid).delete()
            return HttpResponse(json.dumps({'status':True}))
        else:
            return HttpResponse(json.dumps({'status':False}))
    else:
        return redirect("/adm/login")

def article_write(request):
    if request.session.get('login',None):
        if request.method == 'GET':
            tags = Tags.objects.all()
            return render(request, 'view/adm/write.html', {'tags': tags})
    else:
        return redirect("/adm/login")

def upload_img(request):
    if request.session.get('login', None):
        img_obj = request.FILES.get("editormd-image-file", None)
        if img_obj:
            ret = re.match('.*(\..*)', img_obj.name)
            if ret:
                img_name = str(hash(img_obj)) + ret.group(1)
            else:
                img_name = img_obj.name
            with open('media/articles_pic/' + img_name, 'wb') as f:
                for item in img_obj.chunks():
                    f.write(item)
            return HttpResponse(json.dumps({'success':1, 'message':'上传成功', 'url':'/hsjusj/media/articles_pic/' + img_name}))
    else:
        return redirect("/adm/login")

def submit(request):
    if request.session.get('login', None):
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
    else:
        return redirect("/adm/login")