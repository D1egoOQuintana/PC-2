from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuramos el router para las vistas basadas en ViewSet
router = DefaultRouter()
router.register('tipos', views.TipoArchivoViewSet, basename='multimedia-tipo')
router.register('colecciones', views.ColeccionViewSet, basename='multimedia-coleccion')
router.register('archivos', views.ArchivoMultimediaViewSet, basename='multimedia-archivo')
router.register('comentarios', views.ComentarioViewSet, basename='multimedia-comentario')

urlpatterns = [
    # URLs generadas automáticamente por el router
    path('api/', include(router.urls)),
]