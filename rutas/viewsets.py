from rest_framework import viewsets
from .models import Ruta
from .serializers import RutaSerializer


# ViewSet para la API de Rutas
# Proporciona operaciones CRUD para gestionar las rutas de envio
# GET /api/rutas/ - Lista todas las rutas
# POST /api/rutas/ - Crea una nueva ruta
# GET /api/rutas/{id}/ - Obtiene una ruta especifica
# PUT /api/rutas/{id}/ - Actualiza una ruta
# DELETE /api/rutas/{id}/ - Elimina una ruta
class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer