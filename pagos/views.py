from django.shortcuts import render
from .models import bancos, Cuenta, Pago, Cambio

# Create your views here.

def formulario_pago(request):
    # Vista del formulario de registro de pago

    # Redirigir si no está autenticado
    # ! Una vez esté listo el formulario hay que eliminar esta y descomentar las siguientes dos líneas:
    # if(not request.user.is_authenticated):
    #     return redirect('/usuarios/login/')

    if(request.method == 'GET'):
        # Construcción del formulario a partir de la plantilla
        context = {}
        context['cuentas_cliente'] = Cuenta.objects.filter(persona = request.user.persona)
        context['cuentas_empresa'] = Cuenta.objects.filter(persona__pk = 3)
        return render(request, "formulario_pago.html")
    elif(request.method == 'POST'):
        # Validación de completitud de datos
        print(request.POST)
        emisora = request.POST.get('emisora')
        receptora = request.POST.get('receptora')
        referencia = request.POST.get('referencia')
        monto = request.POST.get('monto')
        comentario = request.POST.get('comentario')

        errores = []

        if(not emisora):
            errores.append("No hay una cuenta emisora seleccionada.")
        
        if(not receptora):
            errores.append("No hay una cuenta receptora seleccionada.")
        
        if(not referencia):
            errores.append("No se ingresó un número de referencia.")
        
        if(not monto):
            errores.append("No se ingresó un monto de pago.")

        # Validación de correcta estructura de datos

        if(not Cuenta.objects.filter(pk=emisora).exists()):
            errores.append("La cuenta emisora no existe")
        elif(Cuenta.objects.get(pk=emisora).persona != request.user.persona):
            errores.append("La cuenta emisora no pertenece al usuario.")
        
        if(not Cuenta.objects.filter(pk=receptora).exists()):
            errores.append("La cuenta receptora no existe.")
        elif(Cuenta.objects.get(pk=emisora).persona.pk != 3):
            errores.append("La cuenta receptora no pertenece a Inmobiliaria Villarreal CA.")

        if(float(monto) < 1):
            errores.append("El monto debe ser mayor a un bolívar.")

        # Creación

        Pago.objects.create(
            estado = "P",
            receptora = Cuenta.objects.get(pk=receptora),
            emisora = Cuenta.objects.get(pk=emisora),
            referencia = referencia,
            monto = monto,
            comentario = comentario,
            tasa = Cambio.objects.last()
        )

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