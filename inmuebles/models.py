from django.db import models
from usuarios.models import Persona

# Create your models here.

estados_inmueble = [
    ("R", "En Revisión"),
    ("A", "Activo"),
    ("D", "Denegado"),
    ("E", "Revisión por Edición"),
    ("C", "Revisión para Cancelación")
]

estados_compra = [
    ("P", "Primera Cita"),
    ("E", "Espera de Pago"),
    ("C", "Por Cancelación"),
    ("X", "Cancelada"),
    ("S", "Segunda Cita"),
    ("F", "Finalizada"),
]

estados_cita = [
    ("E", "En Espera"),
    ("C", "Cancelada"),
    ("P", "Pendiente por Resultado"),
    ("F", "Finalizada"),
]

tipos_construccion = [
    ("Casa Individual",)*2,
    ("Casa Dúplex",)*2,
    ("Casa Triplex",)*2,
    ("Casa de Villa",)*2,
    ("Apartamento Regular",)*2,
    ("Apartamento PentHouse",)*2,
]

class Sector(models.Model):
    nombre = models.CharField(max_length=45)

class Inmueble(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, default="R", choices=estados_inmueble)
    ano_construccion = models.IntegerField()
    tipo_construccion = models.CharField(max_length=45, default="Casa Individual", choices=tipos_construccion)
    tiene_estacionamiento = models.BooleanField()
    tamano = models.DecimalField(decimal_places=2,max_digits=10)
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    amueblado = models.BooleanField()
    descripcion = models.TextField()
    comentarios_internos = models.TextField()
    ubicacion_detallada = models.TextField()
    precio = models.DecimalField(decimal_places=2,max_digits=12)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    sector = models.ForeignKey(to=Sector, on_delete=models.CASCADE)
    dueno = models.ForeignKey(to=Persona,on_delete=models.CASCADE, related_name="dueno")
    agente =  models.ForeignKey(to=Persona, on_delete=models.CASCADE, related_name="agente")

class Compra(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1,choices=estados_compra)
    comprador = models.ForeignKey(to=Persona, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(to=Inmueble, on_delete=models.CASCADE)

class Cita(models.Model):
    compra = models.ForeignKey(to=Compra, on_delete=models.CASCADE)
    fecha_asignada = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=estados_cita)
    resultados = models.TextField()
