from django.urls import path

from .views import (
    RutaListView,
    RutaCreateView,
    RutaUpdateView,
    RutaDeleteView,
)

app_name = 'rutas'

urlpatterns = [
    path('rutas/', RutaListView.as_view(), name='ruta_list'),
    path('rutas/crear/', RutaCreateView.as_view(), name='ruta_create'),
    path('rutas/<int:pk>/editar/', RutaUpdateView.as_view(), name='ruta_update'),
    path('rutas/<int:pk>/eliminar/', RutaDeleteView.as_view(), name='ruta_delete'),
]