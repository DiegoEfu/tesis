from django.shortcuts import render
from .models import bancos, Cuenta

# Create your views here.

def formulario_pago(request):
    # Vista del formulario de registro de pago

    # Redirigir si no está autenticado
    # ! Una vez esté listo el formulario hay que eliminar esta y descomentar las siguientes dos líneas:
    # if(not request.user.is_authenticated):
    #     return redirect('/usuarios/login/')

    if(request.method == 'GET'):
        # Construcción del formulario a partir de la plantilla
        return render(request, "formulario_pago.html")
    elif(request.method == 'POST'):
        # Validación de completitud de datos
        # Validación de correcta estructura de datos
        # Creación
        pass

def formulario_cuenta(request):
    # Vista del formulario de registro de pago

    # Redirigir si no está autenticado
    # ! Una vez esté listo el formulario hay que eliminar esta y descomentar las siguientes dos líneas:
    # if(not request.user.is_authenticated):
    #     return redirect('/usuarios/login/')

    if(request.method == 'GET'):
        # Construcción del formulario a partir de la plantilla
        return render(request, "formulario_cuenta.html", {"bancos": bancos})
    elif(request.method == 'POST'):
        print(request.POST)
        banco = request.POST.get('banco')
        numero = request.POST.get('numero')

        # Validación de completitud de datos
        errores = []

        if(not banco):
            errores.append("Debe de escoger un banco")
        
        if(not numero):
            errores.append("Debe de ingresar un número de cuenta")

        # Validación de correcta estructura de datos

        if(banco and numero):
            if(numero[:4] != banco[:4]):
                errores.append("El número de cuenta debe de coincidir con el banco.")
            
            if(len(numero) < 20):
                errores.append("El número de cuenta debe estar en formato de 20 dígitos")

        # Creación

        if(not len(errores)):
            Cuenta.objects.create(
                banco = banco,
                numero = numero,
                persona = request.user.persona
            )
        else:
            return render(request, "formulario_cuenta.html", {"bancos": bancos, "errores": errores})