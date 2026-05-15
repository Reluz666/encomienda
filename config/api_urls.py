from rest_framework.routers import DefaultRouter
from clientes.viewsets import ClienteViewSet
from rutas.viewsets import RutaViewSet
from envios.viewsets import EmpleadoViewSet, EncomiendaViewSet, HistorialEstadoViewSet


# Configuracion del router de la API REST
# Automatically creates URLs for CRUD operations:
# GET, POST /api/clientes/
# GET, PUT, DELETE /api/clientes/{id}/
# Same pattern for all registered viewsets
router = DefaultRouter()

# Registrar los viewsets con sus nombres en la API
router.register(r'clientes', ClienteViewSet)          # API de clientes
router.register(r'rutas', RutaViewSet)                # API de rutas
router.register(r'empleados', EmpleadoViewSet)        # API de empleados
router.register(r'encomiendas', EncomiendaViewSet)    # API de encomiendas
router.register(r'historial-estados', HistorialEstadoViewSet)  # API de historial

urlpatterns = router.urls