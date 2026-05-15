from rest_framework import serializers
from .models import Empleado, Encomienda, HistorialEstado
from clientes.models import Cliente
from rutas.models import Ruta
from clientes.serializers import ClienteSerializer
from rutas.serializers import RutaSerializer


# Serializador para el modelo Empleado
# Convierte los datos del empleado a formato JSON
class EmpleadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empleado
        fields = [
            'id',              # Identificador unico
            'codigo',          # Codigo interno del empleado
            'nombres',         # Nombres completos
            'apellidos',       # Apellidos completos
            'cargo',           # Cargo que desempen~a
            'email',           # Correo electronico
            'telefono',        # Numero de contacto
            'estado',          # Estado (Activo/De baja)
            'fecha_ingreso',   # Fecha de ingreso a laborar
        ]


# Serializador para el modelo Encomienda
# Incluye relaciones anidadas con cliente y ruta
class EncomiendaSerializer(serializers.ModelSerializer):
    # Relación con remitente - en lectura muestra datos completos
    remitente = ClienteSerializer(read_only=True)
    # En escritura solo se necesita el ID del remitente
    remitente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(),
        source='remitente',
        write_only=True
    )
    # Relación con destinatario - en lectura muestra datos completos
    destinatario = ClienteSerializer(read_only=True)
    destinatario_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(),
        source='destinatario',
        write_only=True
    )
    # Relación con ruta
    ruta = RutaSerializer(read_only=True)
    ruta_id = serializers.PrimaryKeyRelatedField(
        queryset=Ruta.objects.all(),
        source='ruta',
        write_only=True
    )
    # Relación con empleado que registro
    empleado_registro = EmpleadoSerializer(read_only=True)
    empleado_registro_id = serializers.PrimaryKeyRelatedField(
        queryset=Empleado.objects.all(),
        source='empleado_registro',
        write_only=True
    )
    # Campos calculados (solo lectura)
    esta_entregada = serializers.BooleanField(read_only=True)
    esta_en_transito = serializers.BooleanField(read_only=True)
    dias_en_transito = serializers.IntegerField(read_only=True)
    tiene_retraso = serializers.BooleanField(read_only=True)
    descripcion_corta = serializers.CharField(read_only=True)

    class Meta:
        model = Encomienda
        fields = [
            'id',                          # Identificador unico
            'codigo',                       # Codigo de la encomienda
            'descripcion',                  # Descripcion del contenido
            'peso_kg',                      # Peso en kilogramos
            'volumen_cm3',                  # Volumen (opcional)
            'remitente',                    # Datos completos del remitente
            'remitente_id',                 # ID del remitente (escritura)
            'destinatario',                 # Datos completos del destinatario
            'destinatario_id',              # ID del destinatario (escritura)
            'ruta',                         # Datos completos de la ruta
            'ruta_id',                      # ID de la ruta (escritura)
            'empleado_registro',            # Datos del empleado que registro
            'empleado_registro_id',         # ID del empleado (escritura)
            'estado',                       # Estado actual del envio
            'costo_envio',                  # Costo total del envio
            'fecha_registro',              # Fecha de registro (自动)
            'fecha_entrega_est',           # Fecha estimada de entrega
            'fecha_entrega_real',           # Fecha real de entrega
            'observaciones',                # Notas adicionales
            'esta_entregada',               # Campo calculado
            'esta_en_transito',            # Campo calculado
            'dias_en_transito',            # Campo calculado
            'tiene_retraso',               # Campo calculado
            'descripcion_corta',           # Campo calculado
        ]
        # Campos que no se pueden modificar una vez creados
        read_only_fields = [
            'codigo',
            'costo_envio',
            'fecha_registro',
            'empleado_registro',
        ]


# Serializador para el historial de cambios de estado
# Registra cada cambio que sufre una encomienda
class HistorialEstadoSerializer(serializers.ModelSerializer):
    # Datos completos del empleado que hizo el cambio
    empleado = EmpleadoSerializer(read_only=True)
    # ID del empleado para escritura
    empleado_id = serializers.PrimaryKeyRelatedField(
        queryset=Empleado.objects.all(),
        source='empleado',
        write_only=True
    )
    # ID de la encomienda para escritura
    encomienda_id = serializers.PrimaryKeyRelatedField(
        queryset=Encomienda.objects.all(),
        source='encomienda',
        write_only=True
    )

    class Meta:
        model = HistorialEstado
        fields = [
            'id',                  # Identificador unico del registro
            'encomienda_id',       # ID de la encomienda
            'estado_anterior',     # Estado antes del cambio
            'estado_nuevo',        # Nuevo estado
            'observacion',         # Nota sobre el cambio
            'empleado',            # Datos del empleado que hizo el cambio
            'empleado_id',         # ID del empleado (escritura)
            'fecha_cambio',        # Fecha y hora del cambio
        ]
        read_only_fields = ['fecha_cambio']  # Se genera automaticamente