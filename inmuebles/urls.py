from django.urls import path
from .views import *

urlpatterns = [
    # Inmuebles
    path("creacion/", formulario_inmueble, name="formulario_creacion_inmueble"),
    path("resultados/", resultados, name="resultados"),
    path("detallar/<int:pk>/", detallar_inmueble, name="detalle_inmueble"),
    path("creacion/sectores/<int:id>/", get_sectores, name="get_sectores"),
    path("aprobar/<int:pk>/", aprobar_inmueble, name="aprobar_inmueble"),
    path("edicion/<int:pk>/", editar_inmueble, name="editar_inmueble"),

    # Citas
    path("cita/dia/<int:pk>/", seleccionar_dia_cita, name="seleccionar_dia_cita"),
    path("cita/hora/<int:pk>/", seleccionar_hora_cita, name="seleccionar_hora_cita"),
    path("cita/creada/<int:pk>/", cita_creada, name="cita_creada"),
    path("cita/resultados/<int:pk>/", resultados_cita, name="consultar_citas_agente"), # TODO
    
    # Comprar
    path("comprar/<int:pk>/", comprar_inmueble, name="comprar_inmueble"),
    path("compra_realizada/<int:pk>/", compra_realizada, name="compra_realizada"),
    path("cancelar/compra/<int:pk>/", cancelar_compra, name="cancelar_compra"),
    path("cancelar/venta/<int:pk>/", cancelar_venta, name="cancelar_venta"),
    path("cancelar/publicacion/<int:pk>/", cancelar_publicacion, name="cancelar_publicacion"),

    # Consultas
    path('consultar/compras/', consultar_compras, name="consultar_compras"),
    path('consultar/publicaciones/', consultar_publicaciones, name="consultar_publicaciones"),
    path('consultar/citas/', consultar_citas, name="consultar_citas"),
    path('consultar/ventas/', consultar_ventas, name="consultar_ventas"),
    path('consultar/pagos/ventas/<int:pk>/', consultar_pagos_ventas, name="consultar_pagos_ventas"),
    path('consultar/pagos/compras/<int:pk>/', consultar_pagos_compras, name="consultar_pagos_compra"),

    # Agentes
    path('agente/consultar/asignadas/', consultar_asignadas, name="consultar_asignadas"),
    path('agente/consultar/finalizadas/', consultar_finalizadas, name="consultar_finalizadas"),
    path('agente/consultar/revision/', consultar_revision, name="consultar_revision"),

    path('agente/citas/asignadas/', consultar_citas_pendientes, name="consultar_citas_pendientes"),
    path('agente/citas/finalizadas/', consultar_citas_finalizadas, name="consultar_citas_finalizadas"),

    path('agente/ventas/asignadas/', consultar_ventas_revision, name="consultar_ventas_revision"),
    path('agente/ventas/finalizadas/', consultar_ventas_cerradas, name="consultar_ventas_cerradas"),

    path('agente/edicion/<int:pk>/', edicion_inmueble_agente, name="edicion_inmueble_agente"),
    path('agente/cancelacion/<int:pk>/', cancelacion_inmueble_agente, name="cancelacion_inmueble_agente"),
    path('agente/pagos/<int:pk>/', consultar_pagos_venta_activa, name="consultar_pagos_venta_activa"),
    path('agente/edicion/revisar/<int:pk>/', revision_edicion_inmueble, name="revision_edicion_inmueble"),
]