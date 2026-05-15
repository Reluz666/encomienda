from django.shortcuts import render
from clientes.models import Cliente
from rutas.models import Ruta
from envios.models import Encomienda, Empleado
from django.contrib.auth.decorators import login_required


def dashboard(request):
    stats = {
        'total_clientes': Cliente.objects.count(),
        'total_rutas': Ruta.objects.count(),
        'total_encomiendas': Encomienda.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'encomiendas_pendientes': Encomienda.objects.filter(estado='PE').count(),
        'encomiendas_en_transito': Encomienda.objects.filter(estado='TR').count(),
        'encomiendas_entregadas': Encomienda.objects.filter(estado='EN').count(),
    }

    recent_encomiendas = Encomienda.objects.select_related(
        'remitente', 'destinatario', 'ruta'
    ).order_by('-fecha_registro')[:5]

    context = {
        'stats': stats,
        'recent_encomiendas': recent_encomiendas,
    }
    return render(request, 'dashboard.html', context)