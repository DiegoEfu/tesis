from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from .models import Persona, Usuario

# Create your views here.

def bienvenida(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/usuarios/login/')

    if request.user.is_authenticated:
        return render(request, 'registration/bienvenida.html', {})
    
    return redirect('/usuarios/login/')

def register_user(request):
    if request.method == 'POST':
        print(request.POST)
        persona = request.POST.get('tipo')
        identificacion = request.POST.get('identificacion')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        ciego = request.POST.get('ciego')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validar

        # Crear
    else:
        return render(request, 'registration/register.html', {})