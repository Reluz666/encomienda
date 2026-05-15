# clientes/api.py
from rest_framework.routers import DefaultRouter
from .viewsets import ClienteViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)

urlpatterns = router.urls