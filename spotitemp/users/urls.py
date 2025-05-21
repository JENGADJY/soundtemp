from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/',views.edit_profile,name='profile'),
    #path('executer/', views.ma_fonction, name='ma_fonction'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('spotify/refresh/', views.refresh_spotify_token, name='spotify_refresh'),
    path('spotify/recommend/', views.main_dashboard, name='lancer_recommendation'), 
    path('dashboard/', views.main_dashboard, name='main_dashboard'),
    
]
