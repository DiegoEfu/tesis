from django.urls import path
from .views import *

urlpatterns = [
    # Inmuebles
    path("creacion/", formulario_inmueble, name="formulario_creacion_inmueble"),
    path("resultados/", resultados, name="resultados"),
    path("detallar/<int:pk>/", detallar_inmueble, name="detalle_inmueble"),
    path("creacion/sectores/<int:id>/", get_sectores, name="get_sectores"),
    path("aprobar/<int:pk>/", aprobar_inmueble, name="aprobar_inmueble"),

    # Citas
    path("cita/dia/<int:pk>/", seleccionar_dia_cita, name="seleccionar_dia_cita"),
    path("cita/hora/<int:pk>/", seleccionar_hora_cita, name="seleccionar_hora_cita"),
]