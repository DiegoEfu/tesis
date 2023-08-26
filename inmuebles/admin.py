from django.contrib import admin
from .models import *

# Aquí se encuentra el registro de los modelos del administrador

admin.site.register(Inmueble)
admin.site.register(Compra)  
admin.site.register(Cita)
admin.site.register(Parroquia)
admin.site.register(Sector)