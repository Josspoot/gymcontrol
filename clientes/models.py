from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    matricula = models.CharField(max_length=20, unique=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def membresia_activa(self):
        hoy = timezone.now().date()
        return self.membresia_set.filter(
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy,
            activa=True
        ).exists()

    def __str__(self):
        return f"{self.nombre} ({self.matricula})"


class Membresia(models.Model):
    TIPOS = [
        ('VISITA', 'Visita'),
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
            if self.tipo == 'VISITA':
                self.fecha_fin = self.fecha_inicio + timedelta(days=0)
            elif self.tipo == 'MENSUAL':
                self.fecha_fin = self.fecha_inicio + timedelta(days=30)
            elif self.tipo == 'TRIMESTRAL':
                self.fecha_fin = self.fecha_inicio + timedelta(days=90)
            elif self.tipo == 'ANUAL':
                self.fecha_fin = self.fecha_inicio + timedelta(days=360)
        super().save(*args, **kwargs)

    def esta_vencida(self):
        return now().date() > self.fecha_fin

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
    membresia_activa = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cliente} - {self.fecha_hora}"
