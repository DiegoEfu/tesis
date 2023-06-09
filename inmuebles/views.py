from django.shortcuts import render, redirect
from .models import Parroquia, Sector

# Create your views here.

def formulario_inmueble(request):
    # Vista del formulario de creación de inmueble

    # Redirigir si no está autenticado
    # ! Una vez esté listo el formulario hay que eliminar esta y descomentar las siguientes dos líneas:
    # if(not request.user.is_authenticated):
    #     return redirect('/usuarios/login/')

    if(request.method == 'GET'):
        # Construcción del formulario a partir de la plantilla
        context = {}
        context['construcciones'] = ["Casa Individual", "Casa Dúplex", "Casa Tríplex",
            "Casa de Villa", "Apartamento Regular", "Apartamento PentHouse"]
        context['parroquias'] = Parroquia.objects.all()
        context['sectores'] = Sector.objects.filter(parroquia = context['parroquias'].first())
        return render(request, "formulario_inmueble.html", context=context)
    elif(request.method == 'POST'):
        # Validación de completitud de datos
        # Validación de correcta estructura de datos
        # Creación
        pass
