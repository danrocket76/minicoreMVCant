from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import VentasModel, ReglasModel, VendedorModel
from datetime import datetime
from .forms import VentaForm
# Create your views here.

def index(request):
    return render(request, 'index.html')


def registrar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la venta en la base de datos
            return redirect('ventas_exito')  # Redirige a una página de éxito
    else:
        form = VentaForm()

    return render(request, 'registrar_venta.html', {'form': form})


def calcular_comisiones(request):
    contexto = {
    'ventas_totales': 0,
    'meta_venta': 0,
    'comision': 0,
    'bono': 0,
    'vendedor': None,
    'mensaje': ''
}

    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        vendedor_id = request.POST.get("vendedor_id")
        
        try:
            
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            
            
            ventas = VentasModel.objects.filter(
                vendedor_id=vendedor_id,
                fecha__range=(fecha_inicio, fecha_fin)
            ).aggregate(total=Sum('cantidad'))
            
            ventas_totales = ventas['total'] if ventas['total'] else 0

            
            regla = ReglasModel.objects.first()  
            
            if not regla:
                contexto['mensaje'] = "No se ha configurado ninguna regla de comisión."
            elif ventas_totales >= regla.meta_venta:
                
                comision = regla.comision
                if comision <= 1:
                    bono = ventas_totales * comision
                    vendedor = VendedorModel.objects.get(pk=vendedor_id)
                    contexto.update({
                        'ventas_totales': ventas_totales,
                        'meta_venta': regla.meta_venta,
                        'comision': comision,
                        'bono': bono,
                        'vendedor': vendedor,
                    })
                else:
                    contexto['mensaje'] = "La comisión configurada excede el límite permitido."
            else:
                contexto['mensaje'] = "No se alcanzó la meta de ventas para calcular el bono."
        except Exception as e:
            contexto['mensaje'] = f"Error al procesar los datos: {e}"

    return render(request, "calcular_bono.html", contexto)
