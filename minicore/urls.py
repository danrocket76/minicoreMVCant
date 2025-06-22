"""
URL configuration for minicore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render 
from gestorventas.views import calcular_comisiones, registrar_venta, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('calcular-comisiones/', calcular_comisiones, name='calcular_comisiones'),
    path('registrar-venta/', registrar_venta, name='registrar_venta'),
    path('ventas-exito/', lambda request: render(request, 'ventas_exito.html'), name='ventas_exito'),
]

