from django.urls import path
from .views import *

urlpatterns = [
    path("registro/", formulario_pago, name="formulario_registro_pago"),
    path("cuenta/registro/", formulario_cuenta, name="formulario_registro_cuenta"),
]