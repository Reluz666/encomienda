from django.db import models
from config.choices import EstadoGeneral, TipoDocumento
from envios.querysets import ClienteQuerySet


# Modelo para gestionar la informacion de los clientes
class Cliente(models.Model):
    # Manager personalizado para agregar metodos de consulta
    objects = ClienteQuerySet.as_manager()

    # Tipo de documento de identidad (DNI, RUC, Pasaporte)
    tipo_doc  = models.CharField(
        max_length=3,
        choices=TipoDocumento.choices,
        default=TipoDocumento.DNI
    )
    # Numero de documento (unico por cliente)
    nro_doc   = models.CharField(max_length=15, unique=True)
    # Nombres y apellidos completos
    nombres   = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    # Datos de contacto (opcionales)
    telefono  = models.CharField(max_length=15, blank=True, null=True)
    email     = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    # Estado del cliente (activo o de baja)
    estado    = models.IntegerField(
        choices=EstadoGeneral.choices,
        default=EstadoGeneral.ACTIVO
    )
    # Fecha automatica de registro del cliente
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Devuelve el nombre completo en formato "Apellidos, Nombres"
    @property
    def nombre_completo(self):
        return f'{self.apellidos}, {self.nombres}'

    # Verifica si el cliente esta activo
    @property
    def esta_activo(self):
        return self.estado == EstadoGeneral.ACTIVO

    # Cuenta cuanta encomiendas ha enviado este cliente
    @property
    def total_encomiendas_enviadas(self):
        return self.envios_como_remitente.count()

    # Representacion en texto del cliente
    def __str__(self):
        return f'{self.nro_doc} - {self.apellidos}, {self.nombres}'

    # Configuracion de la tabla en la base de datos
    class Meta:
        db_table          = 'clientes'
        verbose_name      = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering          = ['apellidos', 'nombres']