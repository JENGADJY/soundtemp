from django.shortcuts import render

def accueil(request):
    return render(request, 'accueil.html')

def profile(request):
    return render(request,'profile.html')

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')


def main_dashboard(request):
    return render(request,'LAPAGE.html')
