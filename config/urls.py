"""
URL configuration for encomienda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from config.views import dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('config.api_urls')),
    path('', include('clientes.urls')),
    path('', include('envios.urls')),
    path('', include('rutas.urls')),
    path('', dashboard, name='home'),
]