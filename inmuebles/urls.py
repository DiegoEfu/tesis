from django.urls import path
from .views import *

urlpatterns = [
    path("creacion/", formulario_inmueble, name="formulario_creacion_inmueble"),
    path("creacion/sectores/<int:id>/", get_sectores, name="get_sectores")
]