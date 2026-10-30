
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Marca(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre


class Celular(models.Model):

    ESTADOS = [
        ('disponible', 'Disponible'),
        ('agotado', 'Agotado'),
        ('descontinuado', 'Descontinuado'),
    ]

    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        related_name='celulares'
    )

    codigo = models.SlugField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    precio = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='disponible'
    )

    imagen = models.ImageField(
        upload_to='celulares/',
        blank=True,
        null=True
    )

    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    @property
    def disponible(self):
        return (
            self.activo
            and self.estado == 'disponible'
            and self.stock > 0
        )

    @property
    def precio_formateado(self):
        return f"{self.precio:,}".replace(",", ".")

class Perfil(models.Model):

    ROLES = [
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    rut = models.CharField(max_length=15, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='cliente'
    )

    def __str__(self):
        return self.usuario.username
