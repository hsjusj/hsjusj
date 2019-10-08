from django.shortcuts import render
from django.template.response import TemplateResponse
from django.core.cache import cache
from blog import models

# Create your views here.

def home(request):
    if request.META.get('HTTP_X_PJAX', False):
        articles = models.Articles.objects.all()
        return TemplateResponse(request, 'response/blog/home_response.html', {'articles':articles})
    elif request.method == 'GET':
        articles = models.Articles.objects.all()
        return render(request, 'view/blog/home.html', {'articles':articles})

def article_info(request, aid):
    if request.META.get('HTTP_X_PJAX', False):
        article = models.Articles.objects.filter(aid=aid).first()
        if article:
            return TemplateResponse(request, 'response/blog/article_response.html', {'article':article})
    elif request.method == "GET":
        article = models.Articles.objects.filter(aid=aid).first()
        if article:
            return render(request, 'view/blog/article.html', {'article':article})
    return render(request, 'backup/404.html')

def archives(request):
    if request.META.get('HTTP_X_PJAX', False):
        return TemplateResponse(request, 'response/blog/archives_response.html')
    elif request.method == "GET":
        return render(request, 'view/blog/archives.html')

def search(request):
    if request.META.get('HTTP_X_PJAX', False):
        tags = models.Tags.objects.all()
        return TemplateResponse(request, 'response/blog/search_response.html', {'tags':tags})
    elif request.method == 'GET':
        tags = models.Tags.objects.all()
        return render(request, 'view/blog/search.html', {'tags':tags})

def search_tag(request):
    if request.method == "POST":
        tag_name = request.POST.get('tag-name', None)
        if tag_name:
            articlestotag = models.ArticlesToTags.objects.filter(tag__tag_name=tag_name)
            articles = []
            for article in articlestotag:
                articles.append(article.article)
            return TemplateResponse(request, 'response/blog/search_result_response.html', {'articles':articles})

def search_title(request):
    if request.method == "POST":
        key_word = request.POST.get('key-word')
        print(key_word)
        articles = models.Articles.objects.filter(title__icontains=key_word)
        return TemplateResponse(request, 'response/blog/search_result_response.html', {'articles':articles})

def about(request):
    if request.method == "POST":
        return TemplateResponse(request, 'response/blog/about_response.html')
    elif request.method == "GET":
        return render(request, 'view/blog/about.html')

# def selected(request):
#     return render(request, 'utils/selected.html')