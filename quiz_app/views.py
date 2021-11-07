import bcrypt
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from login_app.models import User
from .models import Score, Category, Question
import random


def index(request):
    return render(request, 'index.html')


def play(request):
    context = {
        "categories": Category.objects.all(),
    }
    return render(request, 'play.html', context)


def quiz(request):
    if request.method == 'POST':
        err = Question.objects.validateStartQuiz(request.POST)
        if len(err) > 0:
            messages.error(request, err)
            return redirect('/play')
        else:
            request.session['playcategory'] = request.POST['category']
            request.session['numquestions'] = request.POST['number_of_questions']
            context = {
                "category": Category.objects.get(id=request.session['playcategory']),
                "questions": Question.objects.filter(belong_category=request.session['playcategory']).order_by('?')[
                             :int(request.session['numquestions'])]
            }
            return render(request, 'quiz.html', context)
        return redirect('/')
    return HttpResponse(render(request, 'index.html'))


def quizpost(request):
    if request.method == 'POST':
        request.session['totalscore'] = 0
        request.session['correct'] = 0
        request.session['wrong'] = 0
        answers = {}
        for q in request.POST:
            if q[0:2] == "id":
                for key in request.POST:
                    if key[-1] == q[-1] and key[0:2] == "an":
                        answers[request.POST[q]] = request.POST[key]

    for answer in answers:
        this_answer = Question.objects.get(id=answer)
        if this_answer.answer.lower() == answers[answer].lower():
            request.session['totalscore'] += 10
            request.session['correct'] += 1
        else:
            request.session['wrong'] += 1
    if "user_id" in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        category_id = request.session['playcategory']
        category = Category.objects.get(id=category_id)
        Score.objects.create(score=request.session['totalscore'], quiz_category=category, quiz_taken_by=user)
    return redirect('/results')
    return HttpResponse(render(request, 'index.html'))


def results(request):
    return render(request, 'results.html')