from django.shortcuts import render, HttpResponse
from django.template.response import TemplateResponse
from blog import models

# Create your views here.

def test(request):
    return HttpResponse("TEST")

def home(request):
    print(request.META.get("HTTP_X_PJAX", False))
    if request.META.get("HTTP_X_PJAX", False):
        articles = models.Articles.objects.all()
        return TemplateResponse(request, 'home_response.html', {'articles':articles})
    elif request.method == "GET":
        articles = models.Articles.objects.all()
        return render(request, 'home.html', {'articles':articles})

def search(request):
    # print(request.META.get("HTTP_X_PJAX"))
    if request.META.get("HTTP_X_PJAX", False):
        return TemplateResponse(request, 'search_response.html')
    elif request.method == "GET":
        return render(request, 'search.html')

def orm(reuqust):
    # models.Articles.objects.create(title='git远程提交', content='git remote add origin git@github.com:hsjusj/hsjusj.git')
    # models.Tags.objects.create(tag_name='github')
    # models.ArticlesToTags.objects.create(article_id=1, tag_id=1)
    return HttpResponse('ORM')