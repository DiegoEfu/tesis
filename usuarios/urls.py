from django.urls import path
from .views import *

urlpatterns = [
    path("register", register_user, name="registro"),
    path("comprobar/correo/", comprobacion_correo, name="comprobar_correo"),
    path("comprobar/cedula/", comprobacion_cedula, name="comprobar_cedula"),
    path("comprobar/telefono/", comprobacion_telefono, name="comprobar_telefono"),
    path("perfil/editar/comprobar/correo/", comprobacion_correo, name="comprobar_correo"),
    path("perfil/editar/comprobar/telefono/", comprobacion_telefono, name="comprobar_telefono"),
    path("agente/", bienvenida_agente, name="bienvenida_agente"),
    path("perfil/", perfil, name="perfil"),
    path("perfil/editar/", edicion_perfil, name="edicion_perfil"),
    path("perfil/cambio_contrasena/", cambio_contrasena, name="cambio_contrasena"),
    path("cerrar_sesion", cerrar_sesion, name="cerrar_sesion")
]