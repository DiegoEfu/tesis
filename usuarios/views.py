from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.http.response import HttpResponse

# Create your views here.

def bienvenida(request):
    if request.method == 'POST':
        logout()
        return redirect('/usuarios/login/')

    if request.user.is_authenticated:
        return render(request, 'registration/bienvenida.html', {})
    
    return redirect('/usuarios/login/')

def register_user(request):
    return render(request, 'registration/register.html', {})