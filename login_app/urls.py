from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register, name='register_page'),
    path('register/submitregister',views.submitregister, name='register_submit'),
    path('login',views.login, name='login_page'),
    path('login/submitlogin',views.submitlogin, name='login_submit'),
    path('logout', views.logout, name="logout"),
]