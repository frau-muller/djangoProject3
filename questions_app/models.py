import bcrypt
from django.db import models
from login_app.models import User
from django_random_queryset import RandomManager


class QuestionManager(models.Manager):
    def validateQuestion(self, post_data):
        errors = {}
        if len(post_data['question']) == 0 or len(post_data['answer']) == 0:
            errors['all'] = 'Please type a question and an answer'
        else:
            if len(post_data['question']) < 5:
                errors['question'] = 'question should be at least 5 characters'
        return errors

    def validateStartQuiz(self, post_data):
        error = ''
        if post_data['number_of_questions'] == '' or post_data.get('category', '') == '':
            error = 'Please make sure that you select the category and number of questions'
        return error


class CategoryManager(models.Manager):
    def validateCategory(self, post_data):
        error = ''
        if post_data['new_category'] == '':
            error = 'Please type a category'
        return error


class Category(models.Model):
    title = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # questions_in_group = a list of questions that belong to a specific group   FROM Question
    # questions_in_category = a list of categories for the score table           FROM Score

    objects = CategoryManager()

    def __repr__(self):
        return f'<Category object: ID:{self.id} title:{self.title}'


class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    belong_category = models.ForeignKey(Category, related_name='questions_in_group', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='written_by', on_delete=models.CASCADE)

    objects = QuestionManager()

    def __repr__(self):
        return f'<Question object: ID:{self.id} category={self.belong_category} question:{self.question} answer={self.answer} category={self.belong_category.title}'