from django.shortcuts import render, redirect

# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'adm/login.html')
    elif request.method == 'POST':
        pwd = request.POST.get('pwd', None)
        if pwd == '123':
            request.session['login'] = True
            return redirect('/hsjusj/index')
        else:
            return redirect('/hsjusj/login')


def index(request):
    if request.session.get('login', None):
        return render(request, 'adm/index.html')
    else:
        return redirect('/hsjusj/login')