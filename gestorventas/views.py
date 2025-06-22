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
        'ventas_por_vendedor': [],
        'mensaje': '',
        'vendedores': VendedorModel.objects.all(),
    }

    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        vendedor_id = request.POST.get("vendedor")

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            regla = ReglasModel.objects.first()

            if not regla:
                contexto['mensaje'] = "No se ha configurado ninguna regla de comisión."
                return render(request, "gestorventas/calcular_bono.html", contexto)

            if vendedor_id:  
                ventas = VentasModel.objects.filter(
                    vendedorId=vendedor_id,
                    fechaVenta__range=(fecha_inicio, fecha_fin)
                ).aggregate(total=Sum('cantidadVenta'))

                ventas_totales = ventas['total'] if ventas['total'] else 0
                bono = ventas_totales * regla.cantidadComision if ventas_totales >= regla.metaVenta else 0

                vendedor = VendedorModel.objects.get(pk=vendedor_id)
                contexto['ventas_por_vendedor'].append({
                    'nombre': f"{vendedor.nombreVendedor} {vendedor.apellidoVendedor}",
                    'ventas_totales': ventas_totales,
                    'bono': bono,
                })
            else:  
                todos_los_vendedores = VendedorModel.objects.all()
                for vendedor in todos_los_vendedores:
                    ventas = VentasModel.objects.filter(
                        vendedorId=vendedor.vendedorId,
                        fechaVenta__range=(fecha_inicio, fecha_fin)
                    ).aggregate(total=Sum('cantidadVenta'))

                    ventas_totales = ventas['total'] if ventas['total'] else 0
                    bono = ventas_totales * regla.cantidadComision if ventas_totales >= regla.metaVenta else 0

                    contexto['ventas_por_vendedor'].append({
                        'nombre': f"{vendedor.nombreVendedor} {vendedor.apellidoVendedor}",
                        'ventas_totales': ventas_totales,
                        'bono': bono,
                    })

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
    