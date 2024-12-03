from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'nombre', 'apellidos', 'numero_telefono', 'numero_factura']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cédula'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'numero_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Teléfono'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Factura'}),
        }


    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if Cliente.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError("Ya existe un cliente con esta cédula registrada.")
        return cedula

    def clean_numero_factura(self):
        numero_factura = self.cleaned_data.get('numero_factura')
        if Cliente.objects.filter(numero_factura=numero_factura).exists():
            raise forms.ValidationError("Ya existe un cliente con este número de factura registrado.")
        return numero_factura

    def clean_numero_telefono(self):
        numero_telefono = self.cleaned_data.get('numero_telefono')
        if Cliente.objects.filter(numero_telefono=numero_telefono).exists():
            raise forms.ValidationError("Ya existe un cliente con este número de teléfono registrado.")
        return numero_telefono
