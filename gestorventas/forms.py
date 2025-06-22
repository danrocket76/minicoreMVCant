from django import forms
from .models import VentasModel

class VentaForm(forms.ModelForm):
    class Meta:
        model = VentasModel
        fields = ['vendedor', 'cantidad', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'vendedor': 'Vendedor',
            'cantidad': 'Cantidad Vendida',
            'fecha': 'Fecha de Venta',
        }