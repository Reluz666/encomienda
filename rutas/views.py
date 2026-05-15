from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import RutaModelForm
from .models import Ruta


# Vista para listar todas las rutas registradas
class RutaListView(ListView):
    model = Ruta
    template_name = 'rutas/list.html'
    context_object_name = 'rutas'  # Variable para iterar en la plantilla
    paginate_by = 10  # Mostrar 10 rutas por pagina
    ordering = ['-id']  # Ordenar del mas reciente al mas antiguo


# Vista para registrar una nueva ruta
class RutaCreateView(CreateView):
    model = Ruta
    form_class = RutaModelForm
    template_name = 'rutas/form.html'
    success_url = reverse_lazy('rutas:ruta_list')  # Redirigir despues de guardar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Ruta'
        context['titulo_pagina'] = 'Crear Ruta'
        return context


# Vista para editar una ruta existente
class RutaUpdateView(UpdateView):
    model = Ruta
    form_class = RutaModelForm
    template_name = 'rutas/form.html'
    success_url = reverse_lazy('rutas:ruta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Ruta'
        context['titulo_pagina'] = 'Editar Ruta'
        return context


# Vista para eliminar una ruta (confirmacion)
class RutaDeleteView(DeleteView):
    model = Ruta
    template_name = 'rutas/confirm_delete.html'
    success_url = reverse_lazy('rutas:ruta_list')
    context_object_name = 'ruta'  # Nombre del objeto en la plantilla