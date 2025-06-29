from gestorventas.repositories.ventas_repository import VentasRepository
from gestorventas.models import ReglasModel, VendedorModel

class VentasService:
    @staticmethod
    def obtener_ventas_por_vendedor(vendedor_id, fecha_inicio, fecha_fin):
        ventas = VentasRepository.obtener_ventas(vendedor_id, fecha_inicio, fecha_fin)
        return ventas['total'] if ventas['total'] else 0

    @staticmethod
    def obtener_regla_para_ventas(ventas_totales):
        return ReglasModel.objects.filter(metaVenta__lte=ventas_totales).order_by('-metaVenta').first()

    @staticmethod
    def generar_tabla_vendedores(fecha_inicio, fecha_fin):
        vendedores = VendedorModel.objects.all()
        tabla_vendedores = []

        for vendedor in vendedores:
            ventas_totales = VentasService.obtener_ventas_por_vendedor(vendedor.vendedorId, fecha_inicio, fecha_fin)
            regla = VentasService.obtener_regla_para_ventas(ventas_totales)
            bono = ventas_totales * regla.cantidadComision if regla else 0

            tabla_vendedores.append({
                'nombre': f"{vendedor.nombreVendedor} {vendedor.apellidoVendedor}",
                'ventas_totales': ventas_totales,
                'meta_venta': regla.metaVenta if regla else 0,
                'comision': regla.cantidadComision if regla else 0,
                'bono': bono,
            })
        return tabla_vendedores
