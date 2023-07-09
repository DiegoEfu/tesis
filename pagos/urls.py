from django.urls import path
from .views import *

urlpatterns = [
    path("registro/<int:pk>/", formulario_pago, name="formulario_registro_pago"),
    path("aprobar/<int:pk>/", formulario_aprobar_pago, name="formulario_aprobar_pago"),
    path("cuenta/registro/", formulario_cuenta, name="formulario_registro_cuenta"),
]