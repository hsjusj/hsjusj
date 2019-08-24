from django.shortcuts import render, HttpResponse, redirect
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
                request.session.set_expiry(7)
                return HttpResponse(json.dumps({'status':True}))
            else:
                return HttpResponse(json.dumps({'status':False}))

def index(request):
    if request.session.get('uid', None):
        if request.method == 'GET':
            uid = request.session.get('uid', None)
            models.User.objects.filter(uid=uid).update(final_login=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            user_obj = models.User.objects.filter(uid=uid).first()
            return render(request, 'view/acc/index.html', {'user_obj':user_obj})
    else:
        return redirect('/acc/login')