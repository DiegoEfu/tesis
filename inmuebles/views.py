from django.shortcuts import render, redirect

# Create your views here.

def formulario_inmueble(request):
    # Vista del formulario de creación de inmueble

    # Redirigir si no está autenticado
    # ! Una vez esté listo el formulario hay que eliminar esta y descomentar las siguientes dos líneas:
    # if(not request.user.is_authenticated):
    #     return redirect('/usuarios/login/')

    if(request.method == 'GET'):
        # Construcción del formulario a partir de la plantilla
        return render(request, "formulario_inmueble.html")
    elif(request.method == 'POST'):
        # Validación de completitud de datos
        # Validación de correcta estructura de datos
        # Creación
        pass
