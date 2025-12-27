from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from django.utils import timezone



class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    matricula = models.CharField(max_length=10, unique=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.matricula})"





class Membresia(models.Model):
    TIPOS = [
        ('MENSUAL', 'Mensual'),
        ('TRIMESTRAL', 'Trimestral'),
        ('ANUAL', 'Anual'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha_inicio = models.DateField(default=now)
    fecha_fin = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.fecha_fin:
            if self.tipo == 'MENSUAL':
                self.fecha_fin = self.fecha_inicio + timedelta(days=31)
            elif self.tipo == 'TRIMESTRAL':
                self.fecha_fin = self.fecha_inicio + timedelta(days=91)
            elif self.tipo == 'ANUAL':
                self.fecha_fin = self.fecha_inicio + timedelta(days=366)
        super().save(*args, **kwargs)
    
    def esta_vencida(self):
        return now().date() > self.fecha_fin
    
    def dias_restantes(self):
        hoy = timezone.now().date()
        return (self.fecha_fin - hoy).days

    def esta_por_vencer(self):
        return 0 < self.dias_restantes() <= 3


    def __str__(self):
        return f"{self.cliente.nombre} - {self.tipo}"
    
    



class Pago(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    membresia = models.ForeignKey(
        Membresia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_pago = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.nombre} - ${self.monto}"
    

class RegistroEntrada(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} - {self.fecha_hora}"
