from django.shortcuts import render, redirect, HttpResponse
from adm import models
import json
import time
import datetime

# Create your views here.

def login(request):
    if request.method == 'GET':
        locked = None
        obj = models.adm.objects.filter(id=1).first()
        if datetime.datetime.now() < obj.lock_datetime:
            locked = True
        return render(request, 'adm/login.html', {'locked':locked})
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

def index(request):
    if request.session.get('login', None):
        print(request.session.get('login', None))
        return render(request, 'adm/index.html')
    else:
        return redirect('/hsjusj/login')