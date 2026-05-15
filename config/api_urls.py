# config/api_urls.py
from rest_framework.routers import DefaultRouter
from clientes.viewsets import ClienteViewSet
from rutas.viewsets import RutaViewSet
from envios.viewsets import EmpleadoViewSet, EncomiendaViewSet, HistorialEstadoViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'rutas', RutaViewSet)
router.register(r'empleados', EmpleadoViewSet)
router.register(r'encomiendas', EncomiendaViewSet)
router.register(r'historial-estados', HistorialEstadoViewSet)

urlpatterns = router.urls