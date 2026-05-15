from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from config.choices import EstadoGeneral, EstadoEnvio
from clientes.models import Cliente
from rutas.models import Ruta
from .validators import validar_peso_positivo, validar_codigo_encomienda
from .querysets import EncomiendaQuerySet


# Modelo para los empleados de la empresa de encomiendas
class Empleado(models.Model):
    codigo        = models.CharField(max_length=10, unique=True)  # Codigo interno del empleado
    nombres       = models.CharField(max_length=100)
    apellidos     = models.CharField(max_length=100)
    cargo         = models.CharField(max_length=80)  # Cargo que ocupa (ej: Repartidor, Administrador)
    email         = models.EmailField(unique=True)  # Email unico para inicio de sesion
    telefono      = models.CharField(max_length=15, blank=True, null=True)
    estado        = models.IntegerField(
        choices=EstadoGeneral.choices,
        default=EstadoGeneral.ACTIVO
    )
    fecha_ingreso = models.DateField()  # Fecha en que ingreso a trabajar

    def __str__(self):
        return f'{self.codigo} - {self.apellidos}, {self.nombres}'

    class Meta:
        db_table          = 'empleados'
        verbose_name      = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering          = ['apellidos']


# Modelo principal para las encomiendas o paquetes
class Encomienda(models.Model):
    # Manager personalizado con metodos de consulta reutilizables
    objects = EncomiendaQuerySet.as_manager()

    # Datos de identificacion de la encomienda
    codigo      = models.CharField(
        max_length=20,
        unique=True,
        validators=[validar_codigo_encomienda]  # Validacion: debe empezar con ENC-
    )
    descripcion = models.TextField()  # Descripcion del contenido del paquete
    peso_kg     = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            validar_peso_positivo,  # El peso debe ser mayor a 0
            MinValueValidator(0.01, message='El peso mínimo es 0.01 kg')
        ]
    )
    volumen_cm3 = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True  # Volumen opcional del paquete
    )

    # Relaciones con otras entidades
    # Quien envia el paquete
    remitente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT,
        related_name='envios_como_remitente'
    )
    # Quien recibe el paquete
    destinatario = models.ForeignKey(
        Cliente, on_delete=models.PROTECT,
        related_name='envios_como_destinatario'
    )
    # Ruta por la que viaja el paquete
    ruta = models.ForeignKey(
        Ruta, on_delete=models.PROTECT,
        related_name='encomiendas'
    )
    # Empleado que registro la encomienda
    empleado_registro = models.ForeignKey(
        Empleado, on_delete=models.PROTECT,
        related_name='encomiendas_registradas'
    )

    # Estado actual del envio y fechas importantes
    estado     = models.CharField(
        max_length=2,
        choices=EstadoEnvio.choices,
        default=EstadoEnvio.PENDIENTE  # Por defecto inicia como Pendiente
    )
    costo_envio = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    fecha_registro     = models.DateTimeField(auto_now_add=True)  # Se llena solo al crear
    fecha_entrega_est  = models.DateField(null=True, blank=True)  # Fecha estimada de entrega
    fecha_entrega_real = models.DateField(null=True, blank=True)  # Fecha real de entrega
    observaciones      = models.TextField(blank=True, null=True)

    # Metodos de ayuda para verificar estado
    @property
    def esta_entregada(self):
        return self.estado == EstadoEnvio.ENTREGADO

    @property
    def esta_en_transito(self):
        return self.estado == EstadoEnvio.EN_TRANSITO

    # Calcula los dias que lleva el paquete en transito
    @property
    def dias_en_transito(self):
        if not self.fecha_registro:
            return 0
        delta = timezone.now().date() - self.fecha_registro.date()
        return delta.days

    # Verifica si el envio tiene retraso respecto a la fecha estimada
    @property
    def tiene_retraso(self):
        if not self.fecha_entrega_est or self.esta_entregada:
            return False
        return timezone.now().date() > self.fecha_entrega_est

    # Devuelve una version corta de la descripcion (max 50 caracteres)
    @property
    def descripcion_corta(self):
        return self.descripcion[:50] + '...' if len(self.descripcion) > 50 else self.descripcion

    # Validaciones que se ejecutan antes de guardar
    def clean(self):
        errors = {}
        # El remitente y destinatario no pueden ser la misma persona
        if self.remitente_id and self.destinatario_id:
            if self.remitente_id == self.destinatario_id:
                errors['destinatario'] = ValidationError(
                    'El destinatario no puede ser el mismo que el remitente.'
                )
        # La fecha estimada no puede ser en el pasado
        if self.fecha_entrega_est:
            if self.fecha_entrega_est < timezone.now().date():
                errors['fecha_entrega_est'] = ValidationError(
                    'La fecha de entrega estimada no puede ser en el pasado.'
                )
        # La fecha real no puede ser antes que la estimada
        if self.fecha_entrega_est and self.fecha_entrega_real:
            if self.fecha_entrega_real < self.fecha_entrega_est:
                errors['fecha_entrega_real'] = ValidationError(
                    'La fecha de entrega real no puede ser antes de la estimada.'
                )
        if errors:
            raise ValidationError(errors)

    # Ejecutar validaciones antes de guardar
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # Metodo para cambiar el estado de la encomienda
    # Crea automaticamente un registro en el historial
    def cambiar_estado(self, nuevo_estado, empleado, observacion=''):
        if nuevo_estado == self.estado:
            raise ValueError(
                f'La encomienda ya se encuentra en estado {self.get_estado_display()}'
            )
        estado_anterior = self.estado
        self.estado = nuevo_estado
        # Si se marca como entregado, registrar la fecha actual
        if nuevo_estado == EstadoEnvio.ENTREGADO:
            self.fecha_entrega_real = timezone.now().date()
        self.save()
        # Crear registro en el historial de cambios
        HistorialEstado.objects.create(
            encomienda=self,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            empleado=empleado,
            observacion=observacion
        )
        return self

    # Calcula el costo del envio segun el peso y la ruta
    def calcular_costo(self):
        PRECIO_POR_KG_EXTRA = 2.50  # Precio adicional por cada kg extra
        PESO_BASE = 5.0  # Kg incluidos en el precio base
        costo = self.ruta.precio_base
        if self.peso_kg > PESO_BASE:
            costo += (self.peso_kg - PESO_BASE) * PRECIO_POR_KG_EXTRA
        return round(costo, 2)

    # Metodo de clase para crear una encomienda con codigo automatico
    @classmethod
    def crear_con_costo_calculado(cls, remitente, destinatario, ruta,
                                   empleado, descripcion, peso_kg, **kwargs):
        import uuid
        from datetime import timedelta
        # Generar codigo unico: ENC-20260514-ABC123
        codigo = f'ENC-{timezone.now().strftime("%Y%m%d")}-{str(uuid.uuid4())[:6].upper()}'
        # Calcular fecha estimada segun dias de entrega de la ruta
        fecha_est = timezone.now().date() + timedelta(days=ruta.dias_entrega)
        encomienda = cls(
            codigo=codigo,
            descripcion=descripcion,
            peso_kg=peso_kg,
            remitente=remitente,
            destinatario=destinatario,
            ruta=ruta,
            empleado_registro=empleado,
            fecha_entrega_est=fecha_est,
            **kwargs
        )
        # Calcular automaticamente el costo segun peso y ruta
        encomienda.costo_envio = encomienda.calcular_costo()
        encomienda.save()
        return encomienda

    def __str__(self):
        return f'{self.codigo} [{self.get_estado_display()}]'

    class Meta:
        db_table          = 'encomiendas'
        verbose_name      = 'Encomienda'
        verbose_name_plural = 'Encomiendas'
        ordering          = ['-fecha_registro']


# Modelo para registrar el historial de cambios de estado de cada encomienda
class HistorialEstado(models.Model):
    # Encomienda a la que pertenece este cambio
    encomienda = models.ForeignKey(
        Encomienda, on_delete=models.CASCADE,
        related_name='historial'
    )
    # Estados anterior y nuevo del envio
    estado_anterior = models.CharField(max_length=2, choices=EstadoEnvio.choices)
    estado_nuevo    = models.CharField(max_length=2, choices=EstadoEnvio.choices)
    # Observacion opcional sobre el cambio
    observacion     = models.TextField(blank=True, null=True)
    # Empleado que realizo el cambio
    empleado = models.ForeignKey(
        Empleado, on_delete=models.PROTECT,
        related_name='cambios_estado'
    )
    # Fecha y hora automatica del cambio
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.encomienda.codigo}: {self.estado_anterior}→{self.estado_nuevo}'

    class Meta:
        db_table = 'historial_estados'
        ordering = ['-fecha_cambio']