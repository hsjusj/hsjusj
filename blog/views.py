from django.shortcuts import render, HttpResponse
from django.template.response import TemplateResponse
from blog import models
import json
import re

# Create your views here.

def test(request):
    return HttpResponse("TEST")

def home(request):
    if request.META.get('HTTP_X_PJAX', False):
        articles = models.Articles.objects.all()
        return TemplateResponse(request, 'response/home_response.html', {'articles':articles})
    elif request.method == 'GET':
        articles = models.Articles.objects.all()
        return render(request, 'home.html', {'articles':articles})

def article_info(request, aid):
    if request.META.get('HTTP_X_PJAX', False):
        article = models.Articles.objects.filter(aid=aid).first()
        if article:
            return TemplateResponse(request, 'response/article_response.html', {'article':article})
    elif request.method == "GET":
        article = models.Articles.objects.filter(aid=aid).first()
        if article:
            return render(request, 'article_info.html', {'article':article})
    return render(request, '404.html')

def archives(request):
    if request.META.get('HTTP_X_PJAX', False):
        articles = models.Articles.objects.all()
        return TemplateResponse(request, 'response/archives_response.html')
    elif request.method == "GET":
        return render(request, 'archives.html')

def search(request):
    if request.META.get('HTTP_X_PJAX', False):
        tags = models.Tags.objects.all()
        return TemplateResponse(request, 'response/search_response.html', {'tags':tags})
    elif request.method == 'GET':
        tags = models.Tags.objects.all()
        return render(request, 'search.html', {'tags':tags})

def search_tag(request):
    if request.method == "POST":
        tag_name = request.POST.get('tag-name', None)
        if tag_name:
            articlestotag = models.ArticlesToTags.objects.filter(tag__tag_name=tag_name)
            articles = []
            for article in articlestotag:
                articles.append(article.article)
            return TemplateResponse(request, 'response/search_result_response.html', {'articles':articles})

def search_title(request):
    if request.method == "POST":
        key_word = request.POST.get('key-word')
        print(key_word)
        articles = models.Articles.objects.filter(title__icontains=key_word)
        return TemplateResponse(request, 'response/search_result_response.html', {'articles':articles})

def write(request):
    tags = models.Tags.objects.all()
    return render(request, 'write.html', {'tags':tags})

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
        new_article = models.Articles.objects.create(title=title, content=content)
        #new tag--------------------------------------
        for new_tag in new_tags:
            is_exist = models.Tags.objects.filter(tag_name=new_tag).exists()
            if not is_exist:
                tid = models.Tags.objects.create(tag_name=new_tag).tid
                models.ArticlesToTags.objects.create(article_id=new_article.aid, tag_id=tid)
        #tag--------------------------------------
        for tid in tids:
            models.ArticlesToTags.objects.create(article_id=new_article.aid, tag_id=tid)
        return HttpResponse("SUBMIT")


def upload_img(requset):
    img_obj = requset.FILES.get("editormd-image-file", None)
    if img_obj:
        ret = re.match('.*(\..*)', img_obj.name)
        if ret:
            img_name = str(hash(img_obj)) + ret.group(1)
        else:
            img_name = img_obj.name
        with open('media/' + img_name, 'wb') as f:
            for item in img_obj.chunks():
                f.write(item)
        return HttpResponse(json.dumps({'success':1, 'message':'上传成功', 'url':'/media/' + img_name}))


def selected(request):
    return render(request, 'utils/selected.html')

def orm(reuqust):
    models.Articles.objects.create(title='jvav&nginx', content='java&nginx')
    models.Tags.objects.create(tag_name='java')
    models.Tags.objects.create(tag_name='nginx')
    models.ArticlesToTags.objects.create(article_id=2, tag_id=2)
    models.ArticlesToTags.objects.create(article_id=2, tag_id=3)
    return HttpResponse('ORM')