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
        return self.correo_electronico