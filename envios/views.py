from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import EncomiendaModelForm
from .models import Encomienda


class EncomiendaListView(ListView):
    """Vista generica para listar encomiendas."""
    model = Encomienda
    template_name = 'envios/list.html'
    context_object_name = 'encomiendas'
    paginate_by = 10
    ordering = ['-id']


class EncomiendaCreateView(CreateView):
    """Vista generica para crear una nueva encomienda."""
    model = Encomienda
    form_class = EncomiendaModelForm
    template_name = 'envios/form.html'
    success_url = reverse_lazy('envios:encomienda_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Encomienda'
        context['titulo_pagina'] = 'Crear Encomienda'
        return context


class EncomiendaUpdateView(UpdateView):
    """Vista generica para actualizar una encomienda existente."""
    model = Encomienda
    form_class = EncomiendaModelForm
    template_name = 'envios/form.html'
    success_url = reverse_lazy('envios:encomienda_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Encomienda'
        context['titulo_pagina'] = 'Editar Encomienda'
        return context


class EncomiendaDeleteView(DeleteView):
    """Vista generica para eliminar una encomienda."""
    model = Encomienda
    template_name = 'envios/confirm_delete.html'
    success_url = reverse_lazy('envios:encomienda_list')
    context_object_name = 'encomienda'