#coding=utf-8
from django.shortcuts import render, HttpResponse, redirect
from django.template.response import TemplateResponse
from acc import models
import json
import time

# Create your views here.

def signup(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        code = request.POST.get('code')
        code_obj = models.RegisterCode.objects.filter(code=code).first()
        if code_obj:
            user_obj = models.User.objects.create(user=user, pwd=pwd, money=0)
            models.RegisterCode.objects.filter(code=code).delete()
            request.session['uid'] = user_obj.uid
            request.session.set_expiry(7)
            return HttpResponse(json.dumps({'status': True}))
        else:
            return HttpResponse(json.dumps({'status': False}))

def login(request):
    if request.session.get('uid', None):
        return redirect('/acc/index')
    else:
        if request.method == 'GET':
            return render(request, 'view/acc/login.html')
        elif request.method == 'POST':
            user = request.POST.get('user')
            pwd = request.POST.get('pwd')
            user_obj = models.User.objects.filter(user=user, pwd=pwd).first()
            if user_obj:
                request.session['uid'] = user_obj.uid
                request.session.set_expiry(60*60)
                return HttpResponse(json.dumps({'status':True}))
            else:
                return HttpResponse(json.dumps({'status':False}))

def index(request):
    if request.session.get('uid', None):
        if request.method == 'GET':
            uid = request.session.get('uid', None)
            models.User.objects.filter(uid=uid).update(final_login=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            requests = models.Request.objects.all()
            user = models.User.objects.filter(uid=uid).first()
            return render(request, 'view/acc/index.html', {'user':user, 'requests':requests})
    else:
        return redirect('/acc/login')

def requset_submit(request):
    if request.session.get('uid', None):
        uid = request.session.get('uid', None)
        if request.method == 'POST':
            # 1:借 2:还 3:待定 4:不见
            money = request.POST.get('money')
            request_type = request.POST.get('request_type')
            ps = request.POST.get('ps')
            print(money, request_type, ps)
            models.Request.objects.create(user_id=uid, money=money, request_type=request_type, ps=ps)

            user = models.User.objects.filter(uid=uid).first()
            after_money = user.money
            if request_type == "1":
                models.User.objects.filter(uid=uid).update(money=after_money + float(money))
            elif request_type == "2":
                models.User.objects.filter(uid=uid).update(money=after_money - float(money))
            requests = models.Request.objects.filter(user_id=uid)
            return TemplateResponse(request, 'response/acc/index_response.html', { 'user':user, 'requests':requests})
    else:
        return redirect('/acc/login')