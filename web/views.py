from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def contacto(request):
    return render(request, 'contac.html')

def serv(request):
    return render(request, 'servicios.html')

def ubi(request):
    return render(request, 'ubicacion.html')