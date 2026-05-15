from django import forms
from django.core.validators import MinValueValidator
from .models import Ruta
from config.choices import EstadoGeneral


# Formulario para crear y editar rutas de envio
class RutaModelForm(forms.ModelForm):

    class Meta:
        model = Ruta
        fields = [
            'codigo',       # Codigo unico de la ruta (ej: R001)
            'origen',       # Ciudad de origen
            'destino',      # Ciudad de destino
            'descripcion',  # Descripcion opcional de la ruta
            'precio_base',  # Precio base del envio
            'dias_entrega', # Dias estimados para la entrega
            'estado',       # Estado de la ruta (Activa/Inactiva)
        ]
        # Estilos de Bootstrap para cada campo
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo de ruta'}),
            'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad de origen'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad de destino'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripcion de la ruta'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'dias_entrega': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    # Convertir el codigo a mayusculas automaticamente
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper()
        return codigo

    # Validacion: el precio base no puede ser negativo
    def clean_precio_base(self):
        precio = self.cleaned_data.get('precio_base')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio base no puede ser negativo.')
        return precio

    # Validacion: los dias de entrega deben ser al menos 1
    def clean_dias_entrega(self):
        dias = self.cleaned_data.get('dias_entrega')
        if dias is not None and dias < 1:
            raise forms.ValidationError('Los dias de entrega deben ser al menos 1.')
        return dias