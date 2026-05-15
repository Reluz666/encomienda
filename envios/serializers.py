# envios/serializers.py
from rest_framework import serializers
from .models import Empleado, Encomienda, HistorialEstado
from clientes.models import Cliente
from rutas.models import Ruta
from clientes.serializers import ClienteSerializer
from rutas.serializers import RutaSerializer


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = [
            'id',
            'codigo',
            'nombres',
            'apellidos',
            'cargo',
            'email',
            'telefono',
            'estado',
            'fecha_ingreso',
        ]


class EncomiendaSerializer(serializers.ModelSerializer):
    remitente = ClienteSerializer(read_only=True)
    remitente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(),
        source='remitente',
        write_only=True
    )
    destinatario = ClienteSerializer(read_only=True)
    destinatario_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(),
        source='destinatario',
        write_only=True
    )
    ruta = RutaSerializer(read_only=True)
    ruta_id = serializers.PrimaryKeyRelatedField(
        queryset=Ruta.objects.all(),
        source='ruta',
        write_only=True
    )
    empleado_registro = EmpleadoSerializer(read_only=True)
    empleado_registro_id = serializers.PrimaryKeyRelatedField(
        queryset=Empleado.objects.all(),
        source='empleado_registro',
        write_only=True
    )
    # Propiedades solo lectura
    esta_entregada = serializers.BooleanField(read_only=True)
    esta_en_transito = serializers.BooleanField(read_only=True)
    dias_en_transito = serializers.IntegerField(read_only=True)
    tiene_retraso = serializers.BooleanField(read_only=True)
    descripcion_corta = serializers.CharField(read_only=True)

    class Meta:
        model = Encomienda
        fields = [
            'id',
            'codigo',
            'descripcion',
            'peso_kg',
            'volumen_cm3',
            'remitente',
            'remitente_id',
            'destinatario',
            'destinatario_id',
            'ruta',
            'ruta_id',
            'empleado_registro',
            'empleado_registro_id',
            'estado',
            'costo_envio',
            'fecha_registro',
            'fecha_entrega_est',
            'fecha_entrega_real',
            'observaciones',
            'esta_entregada',
            'esta_en_transito',
            'dias_en_transito',
            'tiene_retraso',
            'descripcion_corta',
        ]
        read_only_fields = [
            'codigo',
            'costo_envio',
            'fecha_registro',
            'empleado_registro',
        ]


class HistorialEstadoSerializer(serializers.ModelSerializer):
    empleado = EmpleadoSerializer(read_only=True)
    empleado_id = serializers.PrimaryKeyRelatedField(
        queryset=Empleado.objects.all(),
        source='empleado',
        write_only=True
    )
    # Alias para escritura directa de encomienda
    encomienda_id = serializers.PrimaryKeyRelatedField(
        queryset=Encomienda.objects.all(),
        source='encomienda',
        write_only=True
    )

    class Meta:
        model = HistorialEstado
        fields = [
            'id',
            'encomienda_id',
            'estado_anterior',
            'estado_nuevo',
            'observacion',
            'empleado',
            'empleado_id',
            'fecha_cambio',
        ]
        read_only_fields = ['fecha_cambio']