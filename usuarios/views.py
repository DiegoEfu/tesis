from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Persona, Usuario
from django.contrib.auth.hashers import make_password
import re
import datetime
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
        errores = []

        # Campos Vacíos
        if(identificacion == ""):
            errores.append("El campo de identificación no puede estar vacío.")
        if(nombre == ""):
            errores.append("El campo de nombres no puede estar vacío.")
        if(apellido == ""):
            errores.append("El campo de apellidos no puede estar vacío.")
        if(fecha_nacimiento == ""):
            errores.append("El campo de fecha de nacimiento no puede estar vacío.")
        if(email == ""):
            errores.append("El campo de correo electrónico no puede estar vacío.")
        if(password == ""):
            errores.append("El campo de contraseña no puede estar vacío.")
        
        # Campos duplicados
        if(Usuario.objects.filter(email=email).exists()):
            errores.append("El email ingresado ya fue utilizado.")
        if(Persona.objects.filter(tipo=persona,identificacion=identificacion).exists()):
            errores.append("Ya hay una persona con esa identificación registrada.")
        
        # Caracteres inválidos
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if(not re.fullmatch(regex,email.strip())):
            errores.append("El correo electrónico ingresado no es válido.")
        regex = r"[A-Za-záéíóúÁÉÍÓÚñÑüÜ\s]+"
        if(not re.fullmatch(regex,nombre.strip())):
            errores.append("El nombre ingresado no es válido.")
        if(not re.fullmatch(regex,apellido.strip())):
            errores.append("El apellido ingresado no es válido.")
        if(datetime.datetime.today() < datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d')):
            errores.append("La fecha de nacimiento debe de ser menor o igual al día actual.")
        
        if(len(password) < 8):
            errores.append("La contraseña debe contener al menos 8 caracteres.")

        if(len(errores) != 0):
            return render(request, 'registration/register.html', {'errores': errores})

        # Crear
        persona = Persona.objects.create(tipo=persona, identificacion=identificacion.strip(), nombre=nombre.strip(), apellido=apellido.strip(), fecha_nacimiento=fecha_nacimiento, puede_ver = not ciego)
        Usuario.objects.create(persona=persona, email=email.strip(), password = make_password(password))

        return redirect('login/')
    else:
        return render(request, 'registration/register.html', {})