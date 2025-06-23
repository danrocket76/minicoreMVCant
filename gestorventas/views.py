from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import VentasModel, ReglasModel, VendedorModel
from datetime import datetime
from .forms import VentaForm
# Create your views here.

def index(request):
    return render(request, 'gestorventas/index.html')

def ventas_exito(request):
    return render(request, 'gestorventas/ventas_exito.html')

def registrar_venta(request):
    mensaje = ""
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(ventas_exito)  
        else:
            mensaje = "Formulario inválido. Revisa los datos ingresados."
    else:
        form = VentaForm()

    vendedores, datos_ventas = cargar_vendedores_y_ventas()

    contexto = {
        'form': form,
        'vendedores': vendedores,
        'ventas': datos_ventas,
        'mensaje': mensaje,
    }
    return render(request, 'gestorventas/registrar_venta.html', contexto)

def calcular_comisiones(request):
    contexto = {
        'vendedores': VendedorModel.objects.all(),
        'ventas_totales': 0,
        'meta_venta': 0,
        'comision': 0,
        'bono': 0,
        'vendedor': None,
        'mensaje': '',
        'tabla_vendedores': []
    }

    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        vendedor_id = request.POST.get("vendedor")

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

            if vendedor_id:
                ventas = VentasModel.objects.filter(
                    vendedorId_id=vendedor_id,
                    fechaVenta__range=(fecha_inicio, fecha_fin)
                ).aggregate(total=Sum('cantidadVenta'))

                ventas_totales = ventas['total'] if ventas['total'] else 0

                regla = ReglasModel.objects.filter(metaVenta__lte=ventas_totales).order_by('-metaVenta').first()

                if regla:
                    bono = ventas_totales * regla.cantidadComision
                    vendedor = VendedorModel.objects.get(pk=vendedor_id)
                    contexto['tabla_vendedores'] = [{
                        'nombre': f"{vendedor.nombreVendedor} {vendedor.apellidoVendedor}",
                        'ventas_totales': ventas_totales,
                        'meta_venta': regla.metaVenta,
                        'comision': regla.cantidadComision,
                        'bono': bono,
                    }]
                else:
                    contexto['mensaje'] = "No se encontró una regla de comisión aplicable o el periodo seleccionado no registra ventas."

            else:
                vendedores = VendedorModel.objects.all()
                tabla_vendedores = []

                for vendedor in vendedores:
                    ventas = VentasModel.objects.filter(
                        vendedorId_id=vendedor.vendedorId,
                        fechaVenta__range=(fecha_inicio, fecha_fin)
                    ).aggregate(total=Sum('cantidadVenta'))

                    ventas_totales = ventas['total'] if ventas['total'] else 0

                    regla = ReglasModel.objects.filter(metaVenta__lte=ventas_totales).order_by('-metaVenta').first()

                    if regla:
                        bono = ventas_totales * regla.cantidadComision
                    else:
                        bono = 0

                    tabla_vendedores.append({
                        'nombre': f"{vendedor.nombreVendedor} {vendedor.apellidoVendedor}",
                        'ventas_totales': ventas_totales,
                        'meta_venta': regla.metaVenta if regla else 0,
                        'comision': regla.cantidadComision if regla else 0,
                        'bono': bono,
                    })

                contexto['tabla_vendedores'] = tabla_vendedores

        except Exception as e:
            contexto['mensaje'] = f"Error al procesar los datos: {e}"

    return render(request, "gestorventas/calcular_bono.html", contexto)

def cargar_vendedores_y_ventas():
    vendedores = VendedorModel.objects.all()
    ventas = VentasModel.objects.select_related('vendedorId').order_by('-fechaVenta')

    datos_ventas = []
    for venta in ventas:
        datos_ventas.append({
            'vendedor_nombre': f"{venta.vendedorId.nombreVendedor} {venta.vendedorId.apellidoVendedor}",
            'cantidadVenta': venta.cantidadVenta,
            'fechaVenta': venta.fechaVenta,
        })

    return vendedores, datos_ventas
    