from rest_framework import serializers
from .models import Ruta


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = [
            'id',
            'codigo',
            'origen',
            'destino',
            'descripcion',
            'precio_base',
            'dias_entrega',
            'estado',
        ]