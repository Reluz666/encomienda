from rest_framework import serializers
from .models import Cliente


# Serializador para convertir el modelo Cliente a JSON y viceversa
# Se usa en la API REST para exponer los datos de los clientes
class ClienteSerializer(serializers.ModelSerializer):
    # Campos calculados que se incluyen en la respuesta JSON
    # pero no se pueden modificar directamente
    nombre_completo = serializers.CharField(read_only=True)  # Apellidos, Nombres
    esta_activo = serializers.BooleanField(read_only=True)    # True si esta activo
    total_encomiendas_enviadas = serializers.IntegerField(read_only=True)  # Cuantas encomiendas envio

    class Meta:
        model = Cliente
        fields = [
            'id',                      # Identificador unico
            'tipo_doc',                # Tipo de documento (DNI, RUC, Pasaporte)
            'nro_doc',                 # Numero de documento
            'nombres',                # Nombres del cliente
            'apellidos',               # Apellidos del cliente
            'nombre_completo',         # Campo calculado: Apellidos, Nombres
            'telefono',                # Numero de telefono
            'email',                   # Correo electronico
            'direccion',               # Direccion de vivienda
            'estado',                  # Estado (Activo/De baja)
            'fecha_registro',          # Fecha en que se registro
            'esta_activo',            # Campo calculado: esta activo?
            'total_encomiendas_enviadas',  # Campo calculado: total envios
        ]
        read_only_fields = ['fecha_registro']  # No se puede modificar al crear/editar