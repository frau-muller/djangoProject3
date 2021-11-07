from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard',views.dashboard),
    path('stats',views.stats),
    path('stats/comment',views.comment),
    path('stats/reply',views.reply),
    path('user',views.user, name="user_page"),
    path('admin/',views.admin, name="admin_page"),
    path('admin/setadmin/<int:admin_id>',views.setadmin),
    path('admin/removeadmin/<int:admin_id>',views.removeadmin),
    path('admin/delete/<int:user_id>',views.deleteuser)
]


