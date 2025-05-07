from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuramos el router para las vistas basadas en ViewSet
router = DefaultRouter()
router.register('clientes', views.ClienteViewSet, basename='proyectos-cliente')
router.register('categorias', views.CategoriaViewSet, basename='proyectos-categoria')
router.register('proyectos', views.ProyectoViewSet, basename='proyectos-proyecto')
router.register('tareas', views.TareaViewSet, basename='proyectos-tarea')
router.register('comentarios', views.ComentarioViewSet, basename='proyectos-comentario')

urlpatterns = [
    # URLs generadas automáticamente por el router
    path('api/', include(router.urls)),
]