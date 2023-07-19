from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportes.pdfs import generar_pdf
from reportes.mp3 import cita_formalidades_mp3
import os
from .models import bancos, Cuenta, Pago, Cambio
from inmuebles.models import Compra, Cita
from decimal import Decimal
from random import randint
from datetime import timedelta, datetime

# Create your views here.

def formulario_pago(request, pk):
    # Vista del formulario de registro de pago

    compra = Compra.objects.get(pk=pk)

    # Redirigir si no está autenticado
    # ! Una vez esté listo el formulario hay que eliminar esta y descomentar las siguientes dos líneas:
    # if(not request.user.is_authenticated):
    #     return redirect('/usuarios/login/')

    if(request.method == 'GET'):
        # Construcción del formulario a partir de la plantilla
        context = {}
        context['cuentas_empresa'] = Cuenta.objects.filter(persona__pk = 3)
        context['tasa_dolar'] = Cambio.objects.latest('fecha').tasa
        return render(request, "formulario_pago.html",context=context)
    elif(request.method == 'POST'):
        # Validación de completitud de datos
        receptora = request.POST.get('receptora')
        referencia = request.POST.get('referencia')
        moneda = request.POST.get('moneda')
        monto = request.POST.get('monto')
        comentario = request.POST.get('comentario')
        fecha_transaccion = request.POST.get('fecha_transaccion')

        errores = []
        
        if(not receptora):
            errores.append("No hay una cuenta receptora seleccionada.")
        
        if(not referencia):
            errores.append("No se ingresó un número de referencia.")
        
        if(not monto):
            errores.append("No se ingresó un monto de pago.")
        
        if(not fecha_transaccion):
            errores.append("Debe seleccionar fecha de la transacción.")

        # Validación de correcta estructura de datos

        if(Pago.objects.exclude(estado='R').filter(cuenta = receptora, referencia = referencia, fecha_transaccion=fecha_transaccion).exists()):
            errores.append("Ya hay un pago aprobado con estos datos.")
        
        if(not Cuenta.objects.filter(pk=receptora).exists()):
            errores.append("La cuenta receptora no existe.")

        elif(Cuenta.objects.get(pk=receptora).persona.pk != 3):
            errores.append("La cuenta receptora no pertenece a Inmobiliaria Villarreal CA.")

        if(float(monto) < 1):
            errores.append("El monto debe ser mayor a un bolívar.")

        # Creación

        tasa = Cambio.objects.latest('fecha')

        Pago.objects.create(
            estado = "P",
            cuenta = Cuenta.objects.get(pk=receptora),
            referencia = referencia,
            monto = Decimal(monto),
            comentario = comentario,
            fecha_transaccion = fecha_transaccion,
            tasa = tasa,
            compra = compra
        )

        return redirect('/')

def formulario_aprobar_pago(request, pk):
    pago = Pago.objects.get(pk=pk)

    if(request.method == 'GET'):
        return render(request, 'aprobar_pago.html', context={'pago': pago})
    elif(request.method == 'POST'):
        if(request.POST.get('tipo') == 'mp3'):
            cita_formalidades = pago.compra.citas.first()
            file_path = cita_formalidades_mp3(cita_formalidades)

            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/mp3")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        elif(request.POST.get('tipo') == 'pdf'):
            cita_formalidades = pago.compra.citas.first()
            response = generar_pdf(request, 'reporte_cita_formalidades', cita_formalidades, "CITA FORMALIZACIÓN DE VENTA")
            response['Content-Disposition'] = f'attachment; filename=REPORTE_FORMALIZACION_{cita_formalidades.pk}.pdf'
            return response

        comentario_cajero = request.POST.get('comentario_cajero')
        estado = request.POST.get('estado')

        errores = []

        if(not comentario_cajero):
            errores.append("El cajero debe añadir un comentario.")

        if(not estado):
            errores.append("Debe aprobar o rechazar el pago.")
        
        pago.estado = estado
        pago.comentario_cajero = comentario_cajero
        pago.save()

        if(pago.compra.monto_cancelado() >= pago.compra.inmueble.precio):
            compra = pago.compra
            compra.inmueble.estado = 'S'
            compra.inmueble.save()

            inmueble = compra.inmueble
            dias_disponibles = []
            fecha = datetime.today() + timedelta(days=1)

            while len(dias_disponibles) < 7:
                if(fecha.weekday() < 5):
                    dia_a_comparar = datetime(fecha.year,fecha.month,fecha.day)
                    if(inmueble.agente.citas_agente().filter(fecha_asignada = dia_a_comparar).count() < 3):
                        if(compra.comprador.citas_cliente().filter(fecha_asignada = dia_a_comparar).count() < 3):
                            if(inmueble.dueno.citas_cliente().filter(fecha_asignada = dia_a_comparar).count() < 3):
                                dias_disponibles.append(fecha)

                fecha += timedelta(days=1)

            fecha = dias_disponibles[randint(0,4)]
            horas_disponibles = []
            fecha = datetime.strptime(request.session['fecha_cita_escogida'], '%d-%m-%Y')

            if(not inmueble.agente.citas_agente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 8).exists()):
                if(not compra.comprador.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 8).exists()):
                    if(not inmueble.dueno.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 8).exists()):
                     horas_disponibles.append(fecha + timedelta(hours=8))
            
            if(not inmueble.agente.citas_agente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 10).exists()):
                if(not compra.comprador.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 10).exists()):
                    if(not inmueble.dueno.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 10).exists()):
                        horas_disponibles.append(fecha + timedelta(hours=10))

            if(not inmueble.agente.citas_agente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 13).exists()):
                if(not compra.comprador.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 13).exists()):
                    if(not inmueble.dueno.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 13).exists()):
                        horas_disponibles.append(fecha + timedelta(hours=13))

            if(not inmueble.agente.citas_agente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 16).exists()):
                if(not compra.comprador.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 16).exists()):
                    if(not inmueble.dueno.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 16).exists()):
                        horas_disponibles.append(fecha + timedelta(hours=16))

            fecha = hours=horas_disponibles[randint(0,len(horas_disponibles)-1)]

            cita_formalidades = Cita.objects.create(
                compra = compra,
                fecha_asignada = fecha
            )

            return render(request, "pago_completado.html", context={'cita': cita_formalidades})

        return redirect("/")

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