from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import EncomiendaModelForm
from .models import Encomienda


# Vista para listar todas las encomiendas registradas
class EncomiendaListView(ListView):
    model = Encomienda
    template_name = 'envios/list.html'
    context_object_name = 'encomiendas'  # Variable para iterar en la plantilla
    paginate_by = 10  # Mostrar 10 encomiendas por pagina
    ordering = ['-id']  # Ordenar del mas reciente al mas antiguo


# Vista para registrar una nueva encomienda
class EncomiendaCreateView(CreateView):
    model = Encomienda
    form_class = EncomiendaModelForm
    template_name = 'envios/form.html'
    # Redirigir a la lista despues de guardar exitosamente
    success_url = reverse_lazy('envios:encomienda_list')

    # Agregar informacion contextual al contexto de la plantilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Encomienda'
        context['titulo_pagina'] = 'Crear Encomienda'
        return context


# Vista para editar una encomienda existente
class EncomiendaUpdateView(UpdateView):
    model = Encomienda
    form_class = EncomiendaModelForm
    template_name = 'envios/form.html'
    success_url = reverse_lazy('envios:encomienda_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Encomienda'
        context['titulo_pagina'] = 'Editar Encomienda'
        return context


# Vista para eliminar una encomienda (confirmacion)
class EncomiendaDeleteView(DeleteView):
    model = Encomienda
    template_name = 'envios/confirm_delete.html'
    success_url = reverse_lazy('envios:encomienda_list')
    context_object_name = 'encomienda'  # Nombre del objeto en la plantilla