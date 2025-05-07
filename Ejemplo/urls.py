from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoListView, ProductoViewSet

# Configurar un router para usar ViewSet (enfoque recomendado para DRF)
router = DefaultRouter()
router.register('productos', ProductoViewSet, basename='producto')

urlpatterns = [
    # Usar el router para las APIs
    path('api/', include(router.urls)),
    
    # Mantener vista basada en clase si se accede directamente a /Ejemplo/
    path('', lambda request: router.get_api_root_view()(request)),
]
