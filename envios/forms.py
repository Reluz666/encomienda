from django import forms
from django.core.exceptions import ValidationError
from .models import Empleado, Encomienda, HistorialEstado
from config.choices import EstadoGeneral, EstadoEnvio


class EmpleadoModelForm(forms.ModelForm):
    """Formulario para el modelo Empleado."""

    class Meta:
        model = Empleado
        fields = [
            'codigo',
            'nombres',
            'apellidos',
            'cargo',
            'email',
            'telefono',
            'estado',
            'fecha_ingreso',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo de empleado'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper()
        return codigo


class EncomiendaModelForm(forms.ModelForm):
    """Formulario para el modelo Encomienda."""

    class Meta:
        model = Encomienda
        fields = [
            'codigo',
            'descripcion',
            'peso_kg',
            'volumen_cm3',
            'remitente',
            'destinatario',
            'ruta',
            'empleado_registro',
            'estado',
            'costo_envio',
            'fecha_entrega_est',
            'fecha_entrega_real',
            'observaciones',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo de encomienda'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripcion del contenido'}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'volumen_cm3': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remitente': forms.Select(attrs={'class': 'form-control'}),
            'destinatario': forms.Select(attrs={'class': 'form-control'}),
            'ruta': forms.Select(attrs={'class': 'form-control'}),
            'empleado_registro': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'costo_envio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'fecha_entrega_est': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_entrega_real': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observaciones'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        remitente = cleaned_data.get('remitente')
        destinatario = cleaned_data.get('destinatario')

        if remitente and destinatario and remitente.pk == destinatario.pk:
            raise ValidationError({'destinatario': 'El destinatario no puede ser el mismo que el remitente.'})

        return cleaned_data

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper()
        return codigo


class HistorialEstadoModelForm(forms.ModelForm):
    """Formulario para el modelo HistorialEstado."""

    class Meta:
        model = HistorialEstado
        fields = [
            'encomienda',
            'estado_anterior',
            'estado_nuevo',
            'observacion',
            'empleado',
        ]
        widgets = {
            'encomienda': forms.Select(attrs={'class': 'form-control'}),
            'estado_anterior': forms.Select(attrs={'class': 'form-control'}),
            'estado_nuevo': forms.Select(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observacion del cambio'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        estado_anterior = cleaned_data.get('estado_anterior')
        estado_nuevo = cleaned_data.get('estado_nuevo')

        if estado_anterior == estado_nuevo:
            raise ValidationError({'estado_nuevo': 'El nuevo estado no puede ser igual al estado anterior.'})

        return cleaned_data
