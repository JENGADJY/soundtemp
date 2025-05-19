from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .script.client_mistral import reco
from .script.Spotify_data import diction_genres
from .script.weather_data import weather



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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')


        user.username = username
        user.email = email
        user.save()
        messages.success(request, 'Profil mis à jour avec succès !')
        return redirect('profile')  

    return render(request, 'profile.html', {'user': request.user})

@login_required
def ma_fonction(request):
    if request.method == 'POST':
        return HttpResponse(f"Fonction exécutée avec succès.{reco(diction_genres,weather)},Fonction exécutée")
    return HttpResponse("Méthode non autorisée.", status=405)