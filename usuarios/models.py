from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

# Create your models here.

class Persona(models.Model):
    tipo = models.CharField(choices=(('V','V'),('E','E'),('J','J'),('G','G')), null=False, max_length=1)
    identificacion = models.CharField(max_length=9, null=False )
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateTimeField(null=False)
    numero_telefono = models.CharField(null=False, max_length=11)
    puede_ver = models.BooleanField(default=False)
    cargo = models.CharField(choices=(("A","Administrador"), ("G", "Agente Inmobiliario"), ("C", "Comprador")))

    def __str__(self):
        return self.nombre.title() + " " + self.apellido.title()
    
    def cedula(self):
        return self.tipo + "-" + self.identificacion

class Usuario(AbstractUser):
    username = None
    email = models.EmailField("Correo Electrónico", unique=True)
    persona = models.OneToOneField(to='usuarios.Persona', on_delete=models.CASCADE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
