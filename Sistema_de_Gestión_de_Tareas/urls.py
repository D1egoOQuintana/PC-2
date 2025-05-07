from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuramos el router para las vistas basadas en ViewSet
router = DefaultRouter()
router.register('listas', views.ListaViewSet, basename='tareas-lista')
router.register('tareas', views.TareaViewSet, basename='tareas-tarea')
router.register('etiquetas', views.EtiquetaViewSet, basename='tareas-etiqueta')

urlpatterns = [
    # URLs generadas automáticamente por el router
    path('api/', include(router.urls)),
]