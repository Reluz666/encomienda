# envios/api.py
from rest_framework.routers import DefaultRouter
from .viewsets import EmpleadoViewSet, EncomiendaViewSet, HistorialEstadoViewSet

router = DefaultRouter()
router.register(r'empleados', EmpleadoViewSet)
router.register(r'encomiendas', EncomiendaViewSet)
router.register(r'historial-estados', HistorialEstadoViewSet)

urlpatterns = router.urls