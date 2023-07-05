from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Parroquia, Sector, Inmueble, Cita, tipos_construccion
from usuarios.models import Persona
from datetime import datetime, timedelta

# Vistas:

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
        nombre = request.POST.get('nombre')
        ano_construccion = request.POST.get('ano')
        tipo_construccion = request.POST.get('tipo_construccion')
        tiene_estacionamiento = request.POST.get('estacionamiento')
        tamano = request.POST.get('tamano')
        habitaciones = request.POST.get('habitaciones')
        banos = request.POST.get('banos')
        amueblado = request.POST.get('amueblado')
        descripcion = request.POST.get('descripcion')
        ubicacion_detallada = request.POST.get('ubicacion_detallada') 
        precio = request.POST.get('precio')    
        sector = request.POST.get('sector')

        errores = []

        if(not nombre):
            errores.append("Debe especificar un nombre.")
        
        if(not ano_construccion):
            errores.append("Debe especificar un año.")

        if(not tipo_construccion):
            errores.append("Debe especificar un tipo seleccionado.")

        if(not tamano):
            errores.append("Debe especificar tamaño.")

        if(not habitaciones):
            errores.append("Debe especificar habitaciones.")

        if(not banos):
            errores.append("Debe especificar baños.")

        if(not descripcion):
            errores.append("Debe especificar descripción.")

        if(not banos):
            errores.append("Debe especificar baños.")

        if(not ubicacion_detallada):
            errores.append("Debe especificar una ubicación detallada.")

        if(not precio):
            errores.append("Debe especificar un precio.")

        if(not sector):
            errores.append("Debe especificar un sector.")

        # Validación de correcta estructura de datos
        
        if(float(precio) <= 0):
            errores.append("El precio debe ser mayor a cero.")
        
        if(float(tamano) <= 0):
            errores.append("El tamaño debe ser mayor a 0.")

        # Creación

        if(len(errores) != 0):
            return render(request, 'inmuebles/formulario_inmueble.html', {'errores': errores, 'previo': request.POST})

        Inmueble.objects.create(
            nombre = nombre,
            ano_construccion = ano_construccion,
            tipo_construccion = tipos_construccion[tipo_construccion-1],
            tiene_estacionamiento = bool(tiene_estacionamiento),
            tamano = tamano,
            banos = banos,
            habitaciones = habitaciones,
            amueblado = bool(amueblado),
            descripcion = descripcion,
            ubicacion_detallada = ubicacion_detallada,
            precio = precio,
            sector = Sector.objects.get(pk=sector),
            dueno = request.user.persona if request.user.is_authenticated else Persona.objects.first(),
            agente = Persona.objects.first() #! CAMBIAR PARA UN AGENTE ALEATORIO
        )

def get_sectores(request, id):
    return JsonResponse({'res': list(Sector.objects.filter(parroquia__id = id).values())})

def resultados(request):
    if request.method == 'GET':
        resultados = buscar_coincidencias(request.session['busqueda'])
        return render(request, 'resultados.html', context={'resultados': resultados, 'busqueda': request.session['busqueda']})
    elif request.method == 'POST':
        busqueda = request.POST.get('busqueda').strip().lower()
        request.session['busqueda'] = busqueda

        return redirect('/inmuebles/resultados/')

def detallar_inmueble(request, pk):
    if(request.method == 'GET'):
        return render(request, "detalle_inmueble.html", context={'inmueble': Inmueble.objects.get(pk=pk)})
    elif(request.method == 'POST'):
        busqueda = request.POST.get('busqueda').strip().lower()
        request.session['busqueda'] = busqueda

        return redirect('/inmuebles/resultados/')

def aprobar_inmueble(request, pk):
    if request.method == "GET":
        return render(request, 'aprobacion_inmueble.html', context={'inmueble': Inmueble.objects.get(pk = pk),
                                                                    'construcciones': tipos_construccion})
    elif request.method == "POST":
        print(request.POST)
        nombre = request.POST.get('nombre')
        ano_construccion = request.POST.get('ano')
        tipo_construccion = request.POST.get('tipo_construccion')
        tiene_estacionamiento = bool(request.POST.get('estacionamiento'))
        tamano = request.POST.get('tamano')
        habitaciones = request.POST.get('habitaciones')
        banos = request.POST.get('banos')
        amueblado = bool(request.POST.get('amueblado'))
        descripcion = request.POST.get('descripcion')
        ubicacion_detallada = request.POST.get('ubicacion_detallada') 
        precio = request.POST.get('precio')
        comentarios_internos = request.POST.get('comentarios_internos')

        errores = []

        if(not nombre):
            errores.append("Debe especificar un nombre.")
        
        if(not ano_construccion):
            errores.append("Debe especificar un año.")

        if(not tipo_construccion):
            errores.append("Debe especificar un tipo seleccionado.")

        if(not tamano):
            errores.append("Debe especificar tamaño.")

        if(not habitaciones):
            errores.append("Debe especificar habitaciones.")

        if(not banos):
            errores.append("Debe especificar baños.")

        if(not descripcion):
            errores.append("Debe especificar descripción.")

        if(not banos):
            errores.append("Debe especificar baños.")

        if(not ubicacion_detallada):
            errores.append("Debe especificar una ubicación detallada.")

        if(not precio):
            errores.append("Debe especificar un precio.")

        # Validación de correcta estructura de datos
        
        if(float(precio) <= 0):
            errores.append("El precio debe ser mayor a cero.")
        
        if(float(tamano) <= 0):
            errores.append("El tamaño debe ser mayor a 0.")

        # Creación

        if(len(errores) != 0):
            return render(request, 'inmuebles/formulario_inmueble.html', {'errores': errores, 'previo': request.POST})

        inmueble = Inmueble.objects.get(pk=pk)
        inmueble.nombre = nombre
        inmueble.ano_construccion = ano_construccion
        inmueble.tipo_construccion = tipo_construccion
        inmueble.tiene_estacionamiento = tiene_estacionamiento
        inmueble.tamano = tamano
        inmueble.habitaciones = habitaciones
        inmueble.banos = banos
        inmueble.amueblado = amueblado
        inmueble.descripcion = descripcion
        inmueble.comentarios_internos = comentarios_internos
        inmueble.ubicacion_detallada = ubicacion_detallada
        inmueble.precio = precio

        if('aprobado' in request.POST.keys()):
            inmueble.estado = 'A'
        else:
            inmueble.estado = 'D'

        inmueble.save()

        return redirect('/')

def seleccionar_dia_cita(request, pk):
    if(request.method == 'GET'):
        inmueble = Inmueble.objects.get(pk=pk)
        dias_disponibles = []
        fecha = datetime.today() + timedelta(days=1)

        while len(dias_disponibles) < 7:
            if(fecha.weekday() < 5):
                print(fecha.weekday())
                dia_a_comparar = datetime(fecha.year,fecha.month,fecha.day)
                if(inmueble.agente.citas_agente().filter(fecha_asignada = dia_a_comparar).count() < 3):
                    if(request.user.persona.citas_cliente().filter(fecha_asignada = dia_a_comparar).count() < 3):
                        dias_disponibles.append({'fecha': fecha, 
                                                'dia_semana': 'Lunes' if fecha.weekday() == 0 else
                                                'Martes' if fecha.weekday() == 1 else 
                                                'Miércoles' if fecha.weekday() == 2 else
                                                'Jueves' if fecha.weekday() == 3 else 'Viernes'})

            fecha += timedelta(days=1)

        return render(request, 'seleccion_dia_cita.html', context={'dias': dias_disponibles, 'inmueble': inmueble})

    elif(request.method == 'POST'):
        request.session['fecha_cita_escogida'] = request.POST['dia_escogido']
        return redirect(f'/inmuebles/cita/hora/{pk}')

def seleccionar_hora_cita(request, pk):
    if(request.method == "GET"):
        inmueble = Inmueble.objects.get(pk=pk)
        horas_disponibles = []
        fecha = datetime.strptime(request.session['fecha_cita_escogida'], '%d-%m-%Y')

        if(not inmueble.agente.citas_agente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 8).exists()):
            if(not request.user.persona.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 8).exists()):
                horas_disponibles.append(fecha + timedelta(hours=8))
        
        if(not inmueble.agente.citas_agente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 10).exists()):
            if(not request.user.persona.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 10).exists()):
                horas_disponibles.append(fecha + timedelta(hours=10))

        if(not inmueble.agente.citas_agente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 13).exists()):
            if(not request.user.persona.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 13).exists()):
                horas_disponibles.append(fecha + timedelta(hours=13))

        if(not inmueble.agente.citas_agente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 16).exists()):
            if(not request.user.persona.citas_cliente().filter(fecha_asignada__day = fecha.day, fecha_asignada__month = fecha.month, fecha_asignada__year = fecha.year, fecha_asignada__hour = 16).exists()):
                horas_disponibles.append(fecha + timedelta(hours=16))

        return render(request, 'seleccion_horas_cita.html', context={'fecha': fecha, 'inmueble': inmueble, 'horas': horas_disponibles})
    elif(request.method == "POST"):
        hora_escogida = datetime.strptime(request.session['fecha_cita_escogida'], '%d-%m-%Y') + timedelta(hours=int(request.POST['hora_escogida']))
        cita = Cita.objects.create(
            compra = None,
            inmueble = Inmueble.objects.get(pk=pk),
            persona = request.user.persona,
            fecha_asignada = hora_escogida
        )

        return redirect(f'/inmuebles/cita/creada/{cita.pk}')

# Funciones Auxiliares:

def buscar_coincidencias(busqueda):
    posibles_inmuebles = None

    # Por Ubicación

    for sector in Sector.objects.all():
        if sector.nombre.lower() in busqueda:
            posibles_inmuebles = Inmueble.objects.filter(estado = "A", sector = sector.pk) # Se colocan posibles inmuebles en ese sector
        
        if not posibles_inmuebles:
            for parroquia in Parroquia.objects.all():
                if parroquia.nombre in busqueda:
                    posibles_inmuebles = Inmueble.objects.filter(estado = "A", sector__parroquia__nombre = parroquia.pk)

    # Por metros cuadrados
    if "metros cuadrados" in busqueda:
        separado = busqueda.split(" ")
        indice = encuentra_coincidencia(separado, "metros")
        
        if indice != -1:
            if separado[indice - 1].isnumeric():
                posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tamano__gte = separado[indice-1]) if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tamano__gte = separado[indice-1])

    # Por baños
    if "baños" in busqueda:
        separado = busqueda.split(" ")
        indice = encuentra_coincidencia(separado, "baños")
            
        if indice != -1:
            if separado[indice - 1].isnumeric():
                posibles_inmuebles = posibles_inmuebles.filter(estado = "A", banos__gte = separado[indice-1]) if posibles_inmuebles else Inmueble.objects.filter(estado = "A", banos__gte = separado[indice-1])
    elif "baño" in busqueda:
        separado = busqueda.split(" ")
        indice = encuentra_coincidencia(separado, "baño")
            
        if indice != -1:
            if separado[indice - 1].isnumeric():
                posibles_inmuebles = posibles_inmuebles.filter(estado = "A", banos__gte = separado[indice-1]) if posibles_inmuebles else Inmueble.objects.filter(estado = "A", banos__gte = separado[indice-1])

    # Por baños
    if "habitaciones" in busqueda:
        separado = busqueda.split(" ")
        indice = encuentra_coincidencia(separado, "habitaciones")
            
        if indice != -1:
            if separado[indice - 1].isnumeric():
                posibles_inmuebles = posibles_inmuebles.filter(estado = "A", habitaciones__gte = separado[indice-1]) if posibles_inmuebles else Inmueble.objects.filter(estado = "A", habitaciones__gte = separado[indice-1])
    elif "habitacion" in busqueda:
        separado = busqueda.split(" ")
        indice = encuentra_coincidencia(separado, "habitacion")
            
        if indice != -1:
            if separado[indice - 1].isnumeric():
                posibles_inmuebles = posibles_inmuebles.filter(estado = "A", habitaciones__gte = separado[indice-1]) if posibles_inmuebles else Inmueble.objects.filter(estado = "A", habitaciones__gte = separado[indice-1])

    # Amueblado
    if "amueblado" in busqueda:
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", amueblado = True) if posibles_inmuebles else Inmueble.objects.filter(estado = "A", amueblado = True)
    elif "no amueblado" in busqueda:
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", amueblado = False) if posibles_inmuebles else Inmueble.objects.filter(estado = "A", amueblado = False)

    # Tipo de vivienda:
    if "casa" in busqueda:
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "casa") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "casa")
    elif "apartamento" in busqueda:
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "apartamento") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "apartamento")
    elif "individual" in busqueda:
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "individual") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "individual")
    elif "dúplex" in busqueda:
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "dúplex") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "dúplex")
    elif "tríplex" in busqueda:
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "tríplex") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "tríplex")
    elif "villa" in busqueda:
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "villa") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "villa")
    elif "penthouse" in busqueda:
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "penthouse") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "penthouse")

    return posibles_inmuebles

def encuentra_coincidencia(array, a_buscar):
    for i,x in enumerate(array):
        if x == a_buscar:
            return i
    
    return -1