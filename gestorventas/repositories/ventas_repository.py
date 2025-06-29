from gestorventas.models import VentasModel
from django.db.models import Sum

class VentasRepository:
    @staticmethod
    def obtener_ventas(vendedor_id, fecha_inicio, fecha_fin):
        return VentasModel.objects.filter(
            vendedorId_id=vendedor_id,
            fechaVenta__range=(fecha_inicio, fecha_fin)
        ).aggregate(total=Sum('cantidadVenta'))
