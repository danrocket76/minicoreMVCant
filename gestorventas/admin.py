from django.contrib import admin
from .models import VentasModel, VendedorModel, ReglasModel
# Register your models here.
admin.site.register(VentasModel)
admin.site.register(VendedorModel)
admin.site.register(ReglasModel)