from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_factura = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.cedula}"


class Premio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    probabilidad = models.FloatField(help_text="Probabilidad de ganar este premio (en porcentaje)")
    estado = models.BooleanField(default=True)  # Activo/Inactivo

    def __str__(self):
        return self.nombre


class Ganador(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    premio = models.ForeignKey(Premio, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.nombre} {self.cliente.apellidos} - {self.premio.nombre}"
