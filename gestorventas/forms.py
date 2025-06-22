from django import forms
from .models import VentasModel

class VentaForm(forms.ModelForm):
    class Meta:
        model = VentasModel
        fields = ['vendedorId', 'cantidadVenta', 'fechaVenta']
        widgets = {
            'fechaVenta': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'vendedorId': 'Vendedor',
            'cantidadVenta': 'Cantidad Vendida',
            'fechaVenta': 'Fecha de Venta',
        }
