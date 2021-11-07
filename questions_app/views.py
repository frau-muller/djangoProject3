import bcrypt
from django.contrib import messages
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from login_app.models import User
from quiz_app.models import Category, Question

def questionnew(request):
    context={
        "categories":Category.objects.all(),
    }
    return render(request,'newquestion.html',context)

def questioncreate(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            errors = Question.objects.validateQuestion(request.POST)
            if len( errors) > 0:
                return JsonResponse(errors, status=500 ,safe=False)
            else:
                category=Category.objects.get(id=request.POST['category'])
                user=User.objects.get(id=request.session['user_id'])
                question = Question.objects.create(belong_category= category , question=request.POST['question'], answer=request.POST['answer'], created_by=user)
                if request.session['isadmin']==True:
                    return redirect("/admin")
                return redirect("/user")
    return HttpResponse(render(request,'index.html'))

def categorycreate(request):
    if request.session['isadmin']==True:
        if request.method == 'POST':
            err = Category.objects.validateCategory(request.POST)
            if err!="":
                return JsonResponse(err, status=500,safe=False)
            else:
                category = Category.objects.create(title=request.POST['new_category'])
                return redirect("/admin")
    return HttpResponse(render(request,'index.html'))


def questionedit(request,question_id):
    context={
        "question":Question.objects.get(id=question_id),
    }
    return render(request,'editquestion.html',context)

def questionupdate(request,question_id):
    if 'user_id' in request.session:
        user=User.objects.get(id=request.session['user_id'])
        if request.method == 'POST':
            errors = Question.objects.validateQuestion(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/question/edit/{question_id}')
            else:
                question=Question.objects.get(id=question_id)
                question.question=request.POST['question']
                question.answer=request.POST['answer']
                question.save()
                if request.session['isadmin']==True:
                    return redirect("/admin")
                return redirect("/user")
    return HttpResponse(render(request,'index.html'))

def questiondelete(request,question_id):
    if 'user_id' in request.session:
        user=User.objects.get(id=request.session['user_id'])
        question=Question.objects.get(id=question_id)
        if question.created_by.id==user.id or request.session['isadmin']==True:
            question.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))