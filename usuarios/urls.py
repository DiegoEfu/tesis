from django.urls import path
from .views import *

urlpatterns = [
    path("register", register_user, name="registro"),
    path("comprobar/correo/", comprobacion_correo, name="comprobar_correo"),
    path("comprobar/cedula/", comprobacion_cedula, name="comprobar_cedula"),
    path("agente/", bienvenida_agente, name="bienvenida_agente"),
]