from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer


# ViewSet para la API de Clientes
# Proporciona todas las operaciones CRUD automaticamente
# GET /api/clientes/ - Lista todos los clientes
# POST /api/clientes/ - Crea un nuevo cliente
# GET /api/clientes/{id}/ - Obtiene un cliente especifico
# PUT /api/clientes/{id}/ - Actualiza un cliente
# DELETE /api/clientes/{id}/ - Elimina un cliente
class ClienteViewSet(viewsets.ModelViewSet):
    # Consulta todos los clientes de la base de datos
    queryset = Cliente.objects.all()
    # Serializador usado para convertir datos
    serializer_class = ClienteSerializer