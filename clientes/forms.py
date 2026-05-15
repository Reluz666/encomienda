from django import forms
from .models import Cliente
from config.choices import TipoDocumento, EstadoGeneral


# Formulario para crear y editar clientes
# Utiliza ModelForm para mapear automaticamente los campos del modelo
class ClienteModelForm(forms.ModelForm):

    class Meta:
        model = Cliente
        # Campos que se mostraran en el formulario
        fields = [
            'tipo_doc',    # Tipo de documento (DNI, RUC, Pasaporte)
            'nro_doc',     # Numero de documento
            'nombres',     # Nombres del cliente
            'apellidos',   # Apellidos del cliente
            'telefono',    # Telefono de contacto
            'email',       # Correo electronico
            'direccion',   # Direccion de vivienda
            'estado',      # Estado del cliente (Activo/Baja)
        ]
        # Estilos CSS para cada campo usando Bootstrap
        widgets = {
            'tipo_doc': forms.Select(attrs={'class': 'form-control'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nro. de documento'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@ejemplo.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Direccion'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    # Validacion personalizada para el numero de documento
    # Verifica que el DNI tenga 8 digitos o el RUC 11 digitos
    def clean_nro_doc(self):
        nro_doc = self.cleaned_data.get('nro_doc')
        if nro_doc:
            tipo_doc = self.cleaned_data.get('tipo_doc')
            if tipo_doc == TipoDocumento.DNI and len(nro_doc) != 8:
                raise forms.ValidationError('El DNI debe tener 8 digitos.')
            elif tipo_doc == TipoDocumento.RUC and len(nro_doc) != 11:
                raise forms.ValidationError('El RUC debe tener 11 digitos.')
        return nro_doc

    # Validacion para el correo electronico
    # Verifica que no exista otro cliente con el mismo email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            existente = Cliente.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
            if existente:
                raise forms.ValidationError('Este email ya esta registrado.')
        return email
