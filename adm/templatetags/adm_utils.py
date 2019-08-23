#coding=utf8
from django import template
from django.utils.safestring import mark_safe
from blog import models

register = template.Library()

@register.simple_tag
def article_tag(aid):
    code = ""
    articletotags = models.ArticlesToTags.objects.filter(article_id=aid)
    tags = models.Tags.objects.all()
    if not articletotags:
        for tag in tags:
            code += """<li tid="""+ str(tag.tid) +""" class="selected-tag">"""+str(tag.tag_name)+"""</li>"""
        return mark_safe(code)
    for tag in tags:
        flag = True
        for articletotag in articletotags:
            if tag.tid == articletotag.tag_id:
                code += """<li tid="""+ str(tag.tid) +""" class="selected-tag selected-active">"""+str(tag.tag_name)+"""</li>"""
                flag = False
                break
        if flag:
            code += """<li tid="""+ str(tag.tid) +""" class="selected-tag">"""+str(tag.tag_name)+"""</li>"""
    return mark_safe(code)