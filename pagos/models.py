from django.db import models
from usuarios.models import Persona
from inmuebles.models import Compra
from num2words import num2words

# Create your models here.

bancos = [
    ("0102 - BANCO DE VENEZUELA",)*2,
    ("0104 - VENEZOLANO DE CRÉDITO",)*2,
    ("0105 - BANCO MERCANTIL",)*2,
    ("0108 - BANCO PROVINCIAL",)*2,
    ("0114 - BANCO DEL CARIBE",)*2, 
    ("0115 - BANCO EXTERIOR",)*2,    
    ("0128 - BANCO CARONÍ",)*2, 
    ("0134 - BANESCO",)*2, 
    ("0137 - SOFITASA",)*2, 
    ("0138 - BANCO PLAZA",)*2, 
    ("0151 - FONDO COMÚN",)*2, 
    ("0156 - 100% BANCO",)*2, 
    ("0157 - BANCO DEL SUR",)*2, 
    ("0163 - BANCO DEL TESORO",)*2, 
    ("0166 - BANCO AGRÍCOLA",)*2, 
    ("0168 - BANCRECER",)*2, 
    ("0169 - MIBANCO",)*2, 
    ("0171 - BANCO ACTIVO",)*2, 
    ("0172 - BANCAMIGA",)*2, 
    ("0174 - BANPLUS",)*2, 
    ("0175 - BANCO BICENTENARIO",)*2,
    ("0177 - BANFAN",)*2,
    ("0191 - BANCO NACIONAL DE CRÉDITO",)*2
]

estados = [
    ("P", "Pendiente"),
    ("R", "Rechazado"),
    ("A", "Aprobado")
]

class Cuenta(models.Model):
    numero = models.CharField(max_length=20, null=True)
    banco = models.CharField(max_length=50, choices=bancos)
    persona = models.ForeignKey(to=Persona, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.banco} - {self.numero}"

class Cambio(models.Model):
    fecha = models.DateField(auto_now_add=True)
    tasa = models.DecimalField(max_digits=5, decimal_places=2)

    def tasa_texto(self):
        return num2words(self.tasa, lang="es")
    
    def __str__(self):
        return f"BSD 1 = USD {self.tasa} ({self.pk})"

class Pago(models.Model):
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    comentario = models.TextField()
    estado = models.CharField(max_length=1,choices=estados)
    comentario_cajero = models.TextField()
    referencia = models.CharField(max_length=15)
    cuenta = models.ForeignKey(to=Cuenta, on_delete=models.CASCADE, related_name="cuenta_receptora")
    tasa = models.ForeignKey(to=Cambio, on_delete=models.CASCADE, default=1)
    fecha = models.DateTimeField(auto_now_add=True)
    compra = models.ForeignKey(to=Compra, on_delete=models.CASCADE, related_name="pagos")
    fecha_transaccion = models.DateField()

    def valor_dolar(self):
        return round(self.monto/self.tasa.tasa, 2)
    
    def valor_dolar_texto(self):
        return num2words(round(self.monto/self.tasa.tasa, 2), lang="es")
    
    def monto_texto(self):
        return num2words(self.monto, lang="es")
    
    def estado_largo(self):
        for (x,y) in estados:
            if(x == self.estado):
                return y
        
        return "DESCONOCIDO"
    
    def __str__(self):
        return f"PAGO A LA COMPRA {self.compra.pk} ({self.pk})"
    
    class Meta:
        ordering = ('-fecha',)