from django.db import models
from config.choices import EstadoGeneral
from envios.querysets import RutaQuerySet


# Modelo para representar las rutas de envio disponibles
class Ruta(models.Model):
    # Manager personalizado con metodos de consulta reutilizables
    objects = RutaQuerySet.as_manager()

    # Codigo identificador de la ruta (ej: R001)
    codigo       = models.CharField(max_length=10, unique=True)
    # Ciudad de origen de la ruta
    origen       = models.CharField(max_length=100)
    # Ciudad de destino de la ruta
    destino      = models.CharField(max_length=100)
    # Descripcion opcional de la ruta (paradas intermedias, etc)
    descripcion  = models.TextField(blank=True, null=True)
    # Precio base del envio por esta ruta
    precio_base  = models.DecimalField(max_digits=10, decimal_places=2)
    # Dias aproximados de entrega por esta ruta
    dias_entrega = models.PositiveIntegerField(default=1)
    # Estado de la ruta (Activa o Inactiva)
    estado       = models.IntegerField(
        choices=EstadoGeneral.choices,
        default=EstadoGeneral.ACTIVO
    )

    def __str__(self):
        return f'{self.codigo}: {self.origen} → {self.destino}'

    class Meta:
        db_table          = 'rutas'
        verbose_name      = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering          = ['origen', 'destino']