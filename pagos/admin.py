from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Cuenta)
admin.site.register(Cambio)
admin.site.register(Pago)