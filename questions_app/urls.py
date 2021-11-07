from django.urls import path
from . import views

urlpatterns = [
    path('new',views.questionnew, name='new_question_temp'),
    path('create', views.questioncreate, name="create_question"),
    path('edit/<int:question_id>',views.questionedit),
    path('update/<int:question_id>', views.questionupdate),
    path('delete/<int:question_id>', views.questiondelete),
    path('category/create', views.categorycreate, name="create_category")
]

