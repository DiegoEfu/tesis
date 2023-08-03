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
    path("cita/creada/<int:pk>/", cita_creada, name="cita_creada"),
    path("cita/resultados/<int:pk>/", resultados_cita, name="consultar_citas_agente"), # TODO
    
    # Comprar
    path("comprar/<int:pk>/", comprar_inmueble, name="comprar_inmueble"),
    path("compra_realizada/<int:pk>/", compra_realizada, name="compra_realizada"),
    path("cancelar/compra/<int:pk>/", cancelar_compra, name="cancelar_compra"),

    # Consultas
    path('consultar/compras/', consultar_compras, name="consultar_compras"),
    path('consultar/publicaciones/', consultar_publicaciones, name="consultar_publicaciones"),
    path('consultar/citas/', consultar_citas, name="consultar_citas"),
    path('consultar/ventas/', consultar_ventas, name="consultar_ventas"),
    path('consultar/pagos/ventas/<int:pk>/', consultar_pagos_ventas, name="consultar_pagos_ventas"),
    path('consultar/pagos/compras/<int:pk>/', consultar_pagos_compras, name="consultar_pagos_compra")
]