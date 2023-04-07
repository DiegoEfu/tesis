from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

# Create your models here.

class Usuario(AbstractUser):
    username = None
    correo_electronico = models.EmailField("Correo Electrónico", unique=True)
    numero_seguridad = models.CharField("Número Secreto", null=True, max_length=5)

    USERNAME_FIELD = "correo_electronico"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Persona(models.Model):
    tipo = models.CharField(choices=(('V','V'),('E','E'),('J','J'),('G','G')), required=True, null=False, max_length=1)
    identificacion = models.CharField(max_length=9, required=True, null=False )
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateTimeField(null=False)
    puede_ver = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre.title() + " " + self.apellido.title()
    
    def cedula(self):
        return self.tipo + "-" + self.identificacion

