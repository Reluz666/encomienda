from rest_framework import serializers
from .models import Ruta


# Serializador para el modelo Ruta
# Convierte los datos de las rutas a formato JSON para la API
class RutaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ruta
        fields = [
            'id',              # Identificador unico de la ruta
            'codigo',          # Codigo de la ruta (ej: R001)
            'origen',          # Ciudad de origen
            'destino',         # Ciudad de destino
            'descripcion',     # Descripcion de la ruta
            'precio_base',     # Precio base del envio
            'dias_entrega',    # Dias estimados para la entrega
            'estado',         # Estado de la ruta (Activo/Inactivo)
        ]