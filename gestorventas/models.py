from django.db import models

# Create your models here.
class VendedorModel(models.Model):
    vendedorId = models.AutoField(primary_key= True)
    nombreVendedor = models.CharField(max_length=100, null= False, blank=False,verbose_name='Nombre del Vendedor')
    apellidoVendedor = models.CharField(max_length=100, null= False, blank=False, verbose_name='Apellido del Vendedor')
    
    
    def __str__(self):
        return f"{self.nombreVendedor} {self.apellidoVendedor}"
    
class VentasModel(models.Model):
    ventaId = models.AutoField(primary_key=True)
    fechaVenta = models.DateField( null= False, auto_now=False, auto_now_add=False, verbose_name='Fecha de la Venta')
    cantidadVenta = models.DecimalField(max_digits=10,decimal_places = 2,verbose_name='Cantidad Vendida en Dolares')
    vendedorId = models.ForeignKey(VendedorModel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Venta {self.ventaId} - {self.cantidadVenta} - {self.fechaVenta} {VendedorModel.nombreVendedor}"
    
class ReglasModel(models.Model):
    reglaId = models.AutoField(primary_key=True)
    metaVenta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad de Venta para Comision')
    cantidadComision=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad de Comision en Porcentaje')
    
    def __str__(self):
        return f"Regla {self.reglaId} - Meta: {self.metaVenta} - Comision: {self.cantidadComision}"