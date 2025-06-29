from gestorventas.services.ventas_service import VentasService

class ComisionFacade:
    def __init__(self, ventas_service):
        self.ventas_service = ventas_service

    def calcular_comisiones(self, vendedor_id, fecha_inicio, fecha_fin):
        if vendedor_id:
            ventas_totales = self.ventas_service.obtener_ventas_por_vendedor(vendedor_id, fecha_inicio, fecha_fin)
            regla = self.ventas_service.obtener_regla_para_ventas(ventas_totales)
            bono = ventas_totales * regla.cantidadComision if regla else 0

            return [{
                'nombre': f"Vendedor {vendedor_id}",
                'ventas_totales': ventas_totales,
                'meta_venta': regla.metaVenta if regla else 0,
                'comision': regla.cantidadComision if regla else 0,
                'bono': bono,
            }]
        else:
            return self.ventas_service.generar_tabla_vendedores(fecha_inicio, fecha_fin)
