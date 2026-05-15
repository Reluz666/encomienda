# rutas/api.py
from rest_framework.routers import DefaultRouter
from .viewsets import RutaViewSet

router = DefaultRouter()
router.register(r'rutas', RutaViewSet)

urlpatterns = router.urls