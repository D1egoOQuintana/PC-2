from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuramos el router para las vistas basadas en ViewSet
router = DefaultRouter()
router.register('categorias', views.CategoriaViewSet, basename='galeria-categoria')
router.register('fotografos', views.FotografoViewSet, basename='galeria-fotografo')
router.register('etiquetas', views.EtiquetaViewSet, basename='galeria-etiqueta')
router.register('imagenes', views.ImagenViewSet, basename='galeria-imagen')

urlpatterns = [
    # URLs generadas automáticamente por el router
    path('api/', include(router.urls)),
]