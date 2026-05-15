from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ClienteModelForm
from .models import Cliente


class ClienteListView(ListView):
    """Vista generica para listar clientes."""
    model = Cliente
    template_name = 'clientes/list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    ordering = ['-id']


class ClienteCreateView(CreateView):
    """Vista generica para crear un nuevo cliente."""
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Cliente'
        context['titulo_pagina'] = 'Crear Cliente'
        return context


class ClienteUpdateView(UpdateView):
    """Vista generica para actualizar un cliente existente."""
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Cliente'
        context['titulo_pagina'] = 'Editar Cliente'
        return context


class ClienteDeleteView(DeleteView):
    """Vista generica para eliminar un cliente."""
    model = Cliente
    template_name = 'clientes/confirm_delete.html'
    success_url = reverse_lazy('clientes:cliente_list')
    context_object_name = 'cliente'