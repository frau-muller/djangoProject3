import bcrypt
from .models import User 
from django.contrib import messages
from quiz_app.models import Score, Category, Question 
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse


def login(request):
    return render(request,'login.html')

def submitlogin(request):
    if request.method == 'POST':
        errors = User.objects.validateLogin(request.POST)
        if len( errors) > 0: 
            return JsonResponse(errors, status=500 )
        else:  
            logged_user = User.objects.get(username=request.POST['username'].lower())
            request.session['isadmin'] = logged_user.isadmin
            request.session['user_id'] = logged_user.id
            request.session['first_name'] = logged_user.first_name
            if request.session['isadmin']==True:
                return redirect('/admin')
            return redirect('/user')
    return HttpResponse(render(request,'index.html'))

def register(request):
    return render(request,'register.html')

def submitregister(request):
    if request.method == 'POST':
        errors = User.objects.validateRegister(request.POST)
        if len( errors) > 0:  
            return JsonResponse(errors, status=500 )
        else:  
            password=request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=request.POST['username'].lower(), password=pw_hash)
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['isadmin']=user.isadmin
            return redirect('/user')
    return HttpResponse(render(request,'index.html'))

def logout(request): 
    request.session.clear()
    return redirect('/') 