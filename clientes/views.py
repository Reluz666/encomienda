from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ClienteModelForm
from .models import Cliente


# Vista para listar todos los clientes registrados
class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/list.html'
    context_object_name = 'clientes'  # Nombre para usar en la plantilla
    paginate_by = 10  # Mostrar 10 clientes por pagina
    ordering = ['-id']  # Ordenar del mas reciente al mas antiguo


# Vista para registrar un nuevo cliente
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:cliente_list')  # Redirigir despues de guardar

    # Agregar titulos contextuales para la plantilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Cliente'
        context['titulo_pagina'] = 'Crear Cliente'
        return context


# Vista para editar un cliente existente
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Cliente'
        context['titulo_pagina'] = 'Editar Cliente'
        return context


# Vista para eliminar un cliente
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/confirm_delete.html'
    success_url = reverse_lazy('clientes:cliente_list')
    context_object_name = 'cliente'  # Nombre del objeto en la plantilla