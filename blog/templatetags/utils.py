from django import template
from django.utils.safestring import mark_safe
from blog import models

register = template.Library()

@register.simple_tag
def archives():
    articles = models.Articles.objects.all()
    prev = None
    archives_str = ''
    for article in articles:
        current = article.create_datetime.strftime("%Y-%m")
        if prev == current:
            pass
        else:
            if prev:
                archives_str += "</div></div>"
            prev = current
            archives_str += '<div class="row list-blocks">'
            archives_str += '<div class="categorys"><span class="glyphicon glyphicon-tag"></span><span class="categorys-title">'+prev+'</span></div>'
            archives_str += '<div>'
        archives_str += '<div class="col-md-3 list-block">\
                                <div class="title">\
                                    <a addr="article/'+ str(article.aid) +'/">'+ article.title +'</a>\
                                </div>\
                                <div style="margin-top:13px;">\
                                    <span>'+ article.create_datetime.strftime('%Y-%m-%d') +'</span>\
                                </div>\
                            </div>'
    archives_str += "</div></div>"
    return mark_safe(archives_str)