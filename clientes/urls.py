from django.urls import path

# URL patterns para el modulo de clientes
from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
)

app_name = 'clientes'

urlpatterns = [
    # Lista todos los clientes registrados
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    # Muestra el formulario para crear un nuevo cliente
    path('clientes/crear/', ClienteCreateView.as_view(), name='cliente_create'),
    # Edita un cliente existente
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    # Elimina un cliente existente
    path('clientes/<int:pk>/eliminar/', ClienteDeleteView.as_view(), name='cliente_delete'),
]