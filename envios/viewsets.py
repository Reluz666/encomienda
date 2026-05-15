from rest_framework import viewsets
from .models import Empleado, Encomienda, HistorialEstado
from .serializers import EmpleadoSerializer, EncomiendaSerializer, HistorialEstadoSerializer


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer


class EncomiendaViewSet(viewsets.ModelViewSet):
    queryset = Encomienda.objects.all()
    serializer_class = EncomiendaSerializer


class HistorialEstadoViewSet(viewsets.ModelViewSet):
    queryset = HistorialEstado.objects.all()
    serializer_class = HistorialEstadoSerializer