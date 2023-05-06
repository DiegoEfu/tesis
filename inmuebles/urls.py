from django.urls import path
from .views import *

urlpatterns = [
    path("creacion/", formulario_inmueble, name="formulario_creacion_inmueble"),
]