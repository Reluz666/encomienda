from rest_framework import viewsets
from .models import Empleado, Encomienda, HistorialEstado
from .serializers import EmpleadoSerializer, EncomiendaSerializer, HistorialEstadoSerializer


# ViewSet para la API de Empleados
# Permite gestionar el registro de empleados
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer


# ViewSet para la API de Encomiendas
# Proporciona CRUD completo para las encomiendas
# Incluye filtros personalizados por estado, ruta, remitente, etc.
class EncomiendaViewSet(viewsets.ModelViewSet):
    queryset = Encomienda.objects.all()
    serializer_class = EncomiendaSerializer


# ViewSet para la API de Historial de Estados
# Registra todos los cambios de estado de las encomiendas
# Cada vez que una encomienda cambia de estado se crea un registro
class HistorialEstadoViewSet(viewsets.ModelViewSet):
    queryset = HistorialEstado.objects.all()
    serializer_class = HistorialEstadoSerializer