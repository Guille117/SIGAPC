from django.shortcuts import render

def log (request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')