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

    vendedores, datos_ventas = VentasService.cargar_vendedores_y_ventas()

    contexto = {
        'form': form,
        'vendedores': vendedores,
        'ventas': datos_ventas,
        'mensaje': mensaje,
    }
    return render(request, 'gestorventas/registrar_venta.html', contexto)

from gestorventas.facade.comision_fasade import ComisionFacade
from gestorventas.services.ventas_service import VentasService

def calcular_comisiones(request):
    fachada = ComisionFacade(VentasService())
    contexto = {
        'vendedores': VendedorModel.objects.all(),
        'tabla_vendedores': [],
        'mensaje': ''
    }

    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        vendedor_id = request.POST.get("vendedor")

        try:
            contexto['tabla_vendedores'] = fachada.calcular_comisiones(vendedor_id, fecha_inicio, fecha_fin)
        except Exception as e:
            contexto['mensaje'] = f"Error al procesar los datos: {e}"

    return render(request, "gestorventas/calcular_bono.html", contexto)
