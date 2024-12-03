from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_telefono = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{7,15}$',
                message="El número de teléfono debe contener entre 7 y 15 dígitos, y puede incluir un '+' inicial."
            )
        ]
    )  # Campo obligatorio
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    numero_factura = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9-]+$',
                'El número de factura debe contener solo letras, números y guiones.'
            )
        ]
    )

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.cedula}"


class Premio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    probabilidad = models.FloatField(help_text="Probabilidad de ganar este premio (en porcentaje)")
    estado = models.BooleanField(default=True)  # Activo/Inactivo

    def __str__(self):
        return self.nombre

    def is_active(self):
        return self.estado

    def clean(self):
        if self.probabilidad < 0 or self.probabilidad > 100:
            raise ValidationError("La probabilidad debe estar entre 0 y 100.")


class Ganador(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    premio = models.ForeignKey(Premio, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha']),
        ]

    def __str__(self):
        return f"{self.cliente.nombre} {self.cliente.apellidos} - {self.premio.nombre} (Ganado el {self.fecha.strftime('%Y-%m-%d')})"
