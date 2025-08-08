from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/',views.register_view,name='register'),
    path('delete/<int:id>',views.delete_task,name='delete'),
    path('update/<int:id>',views.update_task,name='update'),
]
