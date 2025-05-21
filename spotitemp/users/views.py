import os
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dotenv import load_dotenv
import urllib.parse
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile
from django.contrib.auth.models import User
from .spotify_utils import get_valid_spotify_token, recommendation
from .spotify_utils import refresh_spotify_token


load_dotenv()
client_id=os.getenv("SPOTIFY_CLIENT")
client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès !")
            return redirect('/accueil/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('/accueil/')
        else:
            messages.error(request, "Nom d’utilisateur ou mot de passe incorrect")
    
    return render(request, 'login.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        access_token = request.POST.get('access_token')
        refresh_token = request.POST.get('refresh_token')

        if refresh_token:
            response = requests.post(
                'https://accounts.spotify.com/api/token',
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': os.getenv("SPOTIFY_CLIENT"),
                    'client_secret': os.getenv("SPOTIFY_CLIENT_SECRET"),
                }
            )

            if response.status_code == 200:
                access_token = response.json().get('access_token')
                messages.success(request, "Access token mis à jour avec succès depuis Spotify !")
            else:
                messages.error(request, "Erreur lors du rafraîchissement du token Spotify.")

        user.username = username
        user.email = email
        user.save()


        return redirect('profile')

    return render(request, 'profile.html', {'user': request.user})

#permet d'exeecuter
# @login_required
# def ma_fonction(request):
#     if request.method == 'POST':
#        return HttpResponse(f"Fonction exécutée avec succès.{recommendation(user)},Fonction exécutée")
#     return HttpResponse("Méthode non autorisée.", status=405)



@login_required
def spotify_login(request):
    scope = "user-read-email user-read-private user-top-read"
    auth_url = "https://accounts.spotify.com/authorize"
    
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "show_dialog": "true",
    }

    url = auth_url + "?" + urllib.parse.urlencode(params)
    return redirect(url)

@login_required  
def spotify_callback(request):
    code = request.GET.get('code')
    
    if not code:
        return HttpResponse("Erreur : code d'autorisation manquant", status=400)

    token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(token_url, data=payload)
    if response.status_code != 200:
        return HttpResponse("Erreur lors de la récupération du token Spotify", status=400)
    token_info = response.json()

    access_token = token_info.get('access_token')
    refresh_token = token_info.get('refresh_token')
    expires_in = token_info.get('expires_in')

    # Récupérer l’utilisateur connecté Django
    user = request.user

    # Mettre à jour ou créer UserProfile lié
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.access_token = access_token
    profile.refresh_token = refresh_token
    profile.expires_at = timezone.now() + timedelta(seconds=expires_in)  # expiration calculée
    profile.save()

    # Rediriger vers la page profil ou autre
    return redirect('/profile/')


@login_required
def main_dashboard(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    recommendation_result=None

    access_token = get_valid_spotify_token(user)

    if request.method == "POST":

        recommendation_result = recommendation(user)

    return render(request, "LAPAGE.html", {
        "token_status": "valid",
        "access_token": access_token,
        "recommendation": recommendation_result,
    })


# @login_required
# def get_spotify_profile(request):
#     access_token = get_valid_spotify_token(request.user)
#     if not access_token:
#         return render(request, 'error.html', {'message': "Impossible d’obtenir un token Spotify valide."})

#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }

#     response = requests.get("https://api.spotify.com/v1/me", headers=headers)

#     if response.status_code != 200:
#         return render(request, 'error.html', {'message': "Erreur lors de l'appel à l'API Spotify."})

#     data = response.json()
#     return render(request, 'spotify_profile.html', {'spotify_data': data})


# @login_required
# def refresh_and_show_spotify_profile(request):
#     access_token = get_valid_spotify_token(request.user)

#     if not access_token:
#         return render(request, 'error.html', {'message': "Impossible de récupérer un token Spotify valide."})

#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }

#     response = requests.get("https://api.spotify.com/v1/me", headers=headers)

#     if response.status_code != 200:
#         return render(request, 'error.html', {'message': "Erreur lors de l’appel à l’API Spotify."})

#     data = response.json()
#     return render(request, 'spotify_profile.html', {'spotify_data': data})


