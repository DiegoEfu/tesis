from django.db import models

# Create your models here.

estados_inmueble = [
    ("R", "En Revisión"),
    ("A", "Activo"),
    ("T", "Compromiso de Compra"),
    ("D", "Denegado"),
    ("E", "Revisión por Edición"),
    ("C", "Revisión para Cancelación"),
    ("X", "Cancelado")
]

estados_compra = [
    ("E", "Espera de Pago"),
    ("C", "Por Cancelación"),
    ("X", "Cancelada"),
    ("S", "Cita de Formalidades"),
    ("F", "Finalizada"),
]

estados_cita = [
    ("E", "En Espera"),
    ("C", "Cancelada"),
    ("P", "Pendiente por Resultado"),
    ("F", "Finalizada - Visto Bueno"),
    ("X", "Finalizada - Visto Malo"),
]

tipos_construccion = [
    ("Casa Individual",)*2,
    ("Casa Dúplex",)*2,
    ("Casa Tríplex",)*2,
    ("Casa de Villa",)*2,
    ("Apartamento Regular",)*2,
    ("Apartamento PentHouse",)*2,
    ("Terreno",)*2,
]

class Parroquia(models.Model):
    nombre = models.CharField(max_length=50)

class Sector(models.Model):
    nombre = models.CharField(max_length=45)
    parroquia = models.ForeignKey(to=Parroquia, on_delete=models.CASCADE)

class Inmueble(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, default="R", choices=estados_inmueble)
    ano_construccion = models.IntegerField()
    tipo_construccion = models.CharField(max_length=45, default="Casa Individual", choices=tipos_construccion)
    estacionamientos = models.IntegerField()
    tamano = models.DecimalField(decimal_places=2,max_digits=10)
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    amueblado = models.BooleanField()
    descripcion = models.TextField()
    comentarios_internos = models.TextField(default="")
    ubicacion_detallada = models.TextField()
    precio = models.DecimalField(decimal_places=2,max_digits=12)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    pisos = models.IntegerField()
    agua = models.BooleanField()
    electricidad = models.BooleanField()
    internet = models.BooleanField()
    gas = models.BooleanField()
    aseo = models.BooleanField()

    sector = models.ForeignKey(to=Sector, on_delete=models.CASCADE)
    dueno = models.ForeignKey(to='usuarios.Persona',on_delete=models.CASCADE, related_name="dueno")
    agente =  models.ForeignKey(to='usuarios.Persona', on_delete=models.CASCADE, related_name="agente")

    def precio_input(self):
        return str(self.precio).replace(",",".")
    
    def tamano_input(self):
        return str(self.tamano).replace(",",".")
    
    def estado_largo(self):
        for (x,y) in estados_inmueble:
            if(x == self.estado):
                return y
        
        return "DESCONOCIDO"

class Compra(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1,choices=estados_compra,default='C')
    comprador = models.ForeignKey(to='usuarios.Persona', on_delete=models.CASCADE)
    inmueble = models.ForeignKey(to=Inmueble, on_delete=models.CASCADE)

class Cita(models.Model):
    compra = models.ForeignKey(to=Compra, on_delete=models.CASCADE, null=True)
    inmueble = models.ForeignKey(to=Inmueble, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(to='usuarios.Persona', on_delete=models.CASCADE, null=True)
    fecha_asignada = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=estados_cita, default='E')
    resultados = models.TextField(blank=True)

    def estado_largo(self):
        for (x,y) in estados_cita:
            if(x == self.estado):
                return y
        
        return "DESCONOCIDO"