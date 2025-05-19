from django.urls import path,include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/',views.edit_profile,name='profile'),
    path('executer/', views.ma_fonction, name='ma_fonction'),
]
