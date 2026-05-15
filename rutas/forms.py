from django import forms
from django.core.validators import MinValueValidator
from .models import Ruta
from config.choices import EstadoGeneral


class RutaModelForm(forms.ModelForm):
    """Formulario para el modelo Ruta."""

    class Meta:
        model = Ruta
        fields = [
            'codigo',
            'origen',
            'destino',
            'descripcion',
            'precio_base',
            'dias_entrega',
            'estado',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo de ruta'}),
            'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad de origen'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad de destino'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripcion de la ruta'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'dias_entrega': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper()
        return codigo

    def clean_precio_base(self):
        precio = self.cleaned_data.get('precio_base')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio base no puede ser negativo.')
        return precio

    def clean_dias_entrega(self):
        dias = self.cleaned_data.get('dias_entrega')
        if dias is not None and dias < 1:
            raise forms.ValidationError('Los dias de entrega deben ser al menos 1.')
        return dias
