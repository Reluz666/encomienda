from django.urls import path

from .views import (
    EncomiendaListView,
    EncomiendaCreateView,
    EncomiendaUpdateView,
    EncomiendaDeleteView,
)

app_name = 'envios'

urlpatterns = [
    path('envios/', EncomiendaListView.as_view(), name='encomienda_list'),
    path('envios/crear/', EncomiendaCreateView.as_view(), name='encomienda_create'),
    path('envios/<int:pk>/editar/', EncomiendaUpdateView.as_view(), name='encomienda_update'),
    path('envios/<int:pk>/eliminar/', EncomiendaDeleteView.as_view(), name='encomienda_delete'),
]