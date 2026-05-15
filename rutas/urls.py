from django.urls import path

# URL patterns para el modulo de rutas
from .views import (
    RutaListView,
    RutaCreateView,
    RutaUpdateView,
    RutaDeleteView,
)

app_name = 'rutas'

urlpatterns = [
    # Lista todas las rutas registradas
    path('rutas/', RutaListView.as_view(), name='ruta_list'),
    # Muestra el formulario para crear una nueva ruta
    path('rutas/crear/', RutaCreateView.as_view(), name='ruta_create'),
    # Edita una ruta existente
    path('rutas/<int:pk>/editar/', RutaUpdateView.as_view(), name='ruta_update'),
    # Elimina una ruta existente
    path('rutas/<int:pk>/eliminar/', RutaDeleteView.as_view(), name='ruta_delete'),
]