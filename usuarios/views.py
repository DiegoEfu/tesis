from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http.response import HttpResponse

# Create your views here.

def bienvenida(request):
    return HttpResponse(request.user)

def register_user(request):
    return render(request, 'registration/register.html', {})