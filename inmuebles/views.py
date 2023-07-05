from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Parroquia, Sector, Inmueble, tipos_construccion
from usuarios.models import Persona

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
    elif "dúplex":
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "dúplex") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "dúplex")
    elif "tríplex":
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "tríplex") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "tríplex")
    elif "villa":
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "villa") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "villa")
    elif "penthouse":
        posibles_inmuebles = posibles_inmuebles.filter(estado = "A", tipo_construccion__icontains = "penthouse") if posibles_inmuebles else Inmueble.objects.filter(estado = "A", tipo_construccion__icontains = "penthouse")

    return posibles_inmuebles

def encuentra_coincidencia(array, a_buscar):
    for i,x in enumerate(array):
        if x == a_buscar:
            return i
    
    return -1