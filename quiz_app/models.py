import bcrypt
from django.db import models
from login_app.models import User
from django_random_queryset import RandomManager
from questions_app.models import Category, Question

class Score(models.Model):
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    quiz_category = models.ForeignKey(Category, related_name='questions_in_category', on_delete=models.CASCADE)
    quiz_taken_by = models.ForeignKey(User, related_name='quiz_details', on_delete=models.CASCADE)