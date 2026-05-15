from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import RutaModelForm
from .models import Ruta


class RutaListView(ListView):
    """Vista generica para listar rutas."""
    model = Ruta
    template_name = 'rutas/list.html'
    context_object_name = 'rutas'
    paginate_by = 10
    ordering = ['-id']


class RutaCreateView(CreateView):
    """Vista generica para crear una nueva ruta."""
    model = Ruta
    form_class = RutaModelForm
    template_name = 'rutas/form.html'
    success_url = reverse_lazy('rutas:ruta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Ruta'
        context['titulo_pagina'] = 'Crear Ruta'
        return context


class RutaUpdateView(UpdateView):
    """Vista generica para actualizar una ruta existente."""
    model = Ruta
    form_class = RutaModelForm
    template_name = 'rutas/form.html'
    success_url = reverse_lazy('rutas:ruta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Ruta'
        context['titulo_pagina'] = 'Editar Ruta'
        return context


class RutaDeleteView(DeleteView):
    """Vista generica para eliminar una ruta."""
    model = Ruta
    template_name = 'rutas/confirm_delete.html'
    success_url = reverse_lazy('rutas:ruta_list')
    context_object_name = 'ruta'