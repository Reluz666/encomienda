from django import forms
from django.core.exceptions import ValidationError
from .models import Empleado, Encomienda, HistorialEstado
from config.choices import EstadoGeneral, EstadoEnvio


# Formulario para registrar o editar empleados
class EmpleadoModelForm(forms.ModelForm):

    class Meta:
        model = Empleado
        fields = [
            'codigo',        # Codigo unico del empleado
            'nombres',       # Nombres completos
            'apellidos',     # Apellidos completos
            'cargo',         # Cargo que desempe�a
            'email',         # Correo electronico
            'telefono',      # Numero de contacto
            'estado',        # Activo o de baja
            'fecha_ingreso',  # Fecha en que ingreso a laborar
        ]
        # Estilos de Bootstrap para cada campo
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

    # Convertir el codigo a mayusculas automaticamente
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper()
        return codigo


# Formulario para registrar o editar encomiendas
class EncomiendaModelForm(forms.ModelForm):

    class Meta:
        model = Encomienda
        fields = [
            'codigo',              # Codigo unico de la encomienda
            'descripcion',         # Descripcion del contenido
            'peso_kg',            # Peso en kilogramos
            'volumen_cm3',        # Volumen opcional
            'remitente',           # Cliente que envia
            'destinatario',        # Cliente que recibe
            'ruta',                # Ruta de envio
            'empleado_registro',   # Empleado que registra
            'estado',              # Estado actual del envio
            'costo_envio',         # Costo total del envio
            'fecha_entrega_est',   # Fecha estimada de entrega
            'fecha_entrega_real',  # Fecha real de entrega
            'observaciones',      # Notas adicionales
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

    # Validacion: el remitente y destinatario no pueden ser la misma persona
    def clean(self):
        cleaned_data = super().clean()
        remitente = cleaned_data.get('remitente')
        destinatario = cleaned_data.get('destinatario')

        if remitente and destinatario and remitente.pk == destinatario.pk:
            raise ValidationError({'destinatario': 'El destinatario no puede ser el mismo que el remitente.'})

        return cleaned_data

    # Convertir el codigo a mayusculas automaticamente
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper()
        return codigo


# Formulario para registrar el historial de cambios de estado
class HistorialEstadoModelForm(forms.ModelForm):

    class Meta:
        model = HistorialEstado
        fields = [
            'encomienda',       # Encomienda que cambio de estado
            'estado_anterior',   # Estado antes del cambio
            'estado_nuevo',      # Nuevo estado
            'observacion',       # Nota sobre el cambio
            'empleado',          # Empleado que realizo el cambio
        ]
        widgets = {
            'encomienda': forms.Select(attrs={'class': 'form-control'}),
            'estado_anterior': forms.Select(attrs={'class': 'form-control'}),
            'estado_nuevo': forms.Select(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observacion del cambio'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
        }

    # Validacion: el nuevo estado no puede ser igual al anterior
    def clean(self):
        cleaned_data = super().clean()
        estado_anterior = cleaned_data.get('estado_anterior')
        estado_nuevo = cleaned_data.get('estado_nuevo')

        if estado_anterior == estado_nuevo:
            raise ValidationError({'estado_nuevo': 'El nuevo estado no puede ser igual al estado anterior.'})

        return cleaned_data