import bcrypt
from login_app.models import User
from django.contrib import messages
from django.db.models import Sum 
from .models import Comment, Reply
from quiz_app.models import Score, Category, Question 
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse


def dashboard(request):
    if 'user_id' in request.session:
        all_users=User.objects.all()
        all_categories=Category.objects.all()
        score_results = Score.objects.values('quiz_category','quiz_taken_by').annotate(sum=Sum('score')).order_by('-sum')
    
        context={
            "categories":Category.objects.all(),
            "users":User.objects.all(),
            "scores":score_results,
        }
        return render(request,'dashboard.html',context)
    return HttpResponse(render(request,'index.html'))


def stats(request):
    if 'user_id' in request.session:
        categories= Category.objects.all()
        sum_scores=Score.objects.values('quiz_category','quiz_taken_by').annotate(sum=Sum('score')).order_by('-sum') 
 
        highest_score=[] 
        for catg in categories:
            for score in sum_scores:
                if score['quiz_category'] == catg.id :
                    highest_score.append(score)
                    break

        context={
            "categories":Category.objects.all(), 
            "users":User.objects.all(),
            "scores":Score.objects.values('quiz_taken_by'),
            "comments":Comment.objects.all(),
            'replies':Reply.objects.all(),
            'highest_score':highest_score
        }
        return render(request,'categorystats.html',context)
    return HttpResponse(render(request,'index.html'))

def user(request):
    if request.session['isadmin']==True:
        return redirect('/admin')
    elif 'user_id' in request.session:
        current_users=User.objects.get(id=request.session['user_id'])
        questions=Question.objects.filter(created_by_id=current_users)
        context={
                "questions":questions
        }
        return render(request,'user.html',context)
    return HttpResponse(render(request,'index.html'))

def admin(request):
    if request.session['isadmin']==True:
        current_user=User.objects.get(id=request.session['user_id'])
        questions=Question.objects.all()
        users=User.objects.exclude(id=request.session['user_id'])
        context={
            "questions":questions,
            "users":users,
            "current_user":current_user,
            "categories":Category.objects.all()
        }
        return render(request,'admin.html',context)
    return HttpResponse(render(request,'index.html'))
 
def setadmin(request,admin_id):
    if request.session['isadmin']==True:
        make_admin=User.objects.get(id=admin_id)
        make_admin.isadmin=True
        make_admin.save()
        return redirect("/admin")
    return HttpResponse(render(request,'index.html'))


def removeadmin(request,admin_id):
    if request.session['isadmin']==True:
        make_admin=User.objects.get(id=admin_id)
        make_admin.isadmin=False
        make_admin.save()
        return redirect("/admin" )
    return HttpResponse(render(request,'index.html'))


def comment(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            errors = Comment.objects.validateEmptyComment(request.POST)
            if len( errors) > 0:   
                return JsonResponse(errors, status=500, safe=False)
            else:  
                user=User.objects.get(id=request.session['user_id'])
                Comment.objects.create(comment_content=request.POST['comment'], user_comment=user)
                context = {
                    'comments':Comment.objects.all(),
                    'replies':Reply.objects.all(),
                }
                return render(request,'_comments.html',context)
    return HttpResponse(render(request,'index.html'))

def reply(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            errors = Reply.objects.validateEmptyReply(request.POST)
            if len( errors) > 0:   
                return JsonResponse(errors, status=500, safe=False)
            else:  
                user=User.objects.get(id=request.session['user_id'])
                comment_id=Comment.objects.get(id=request.POST['comment_id'])
                Reply.objects.create(reply_content=request.POST['reply'], user_reply=user,reply_to=comment_id)
                context = {
                    'replies':Reply.objects.all(),
                    'comments':Comment.objects.all()
                }
                return render(request,'_comments.html',context)
    return HttpResponse(render(request,'index.html'))


def deleteuser(request,user_id):
    if request.session['isadmin']==True:
        user=User.objects.get(id=user_id)
        user.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

