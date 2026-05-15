# clientes/serializers.py
from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(read_only=True)
    esta_activo = serializers.BooleanField(read_only=True)
    total_encomiendas_enviadas = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cliente
        fields = [
            'id',
            'tipo_doc',
            'nro_doc',
            'nombres',
            'apellidos',
            'nombre_completo',
            'telefono',
            'email',
            'direccion',
            'estado',
            'fecha_registro',
            'esta_activo',
            'total_encomiendas_enviadas',
        ]
        read_only_fields = ['fecha_registro']