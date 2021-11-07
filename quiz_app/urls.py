from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('play',views.play),
    path('quiz',views.quiz),
    path('quiz/submit',views.quizpost),
    path('results',views.results)
]