from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Vista personalizada para mostrar todas las APIs disponibles
class ApiRoot(APIView):
    """
    Vista raíz que muestra todas las APIs disponibles en el proyecto
    """
    def get(self, request, format=None):
        # Enlaces a las API de galería
        galeria_endpoints = {
            "categorias": reverse('galeria-categoria-list', request=request, format=format),
            "fotografos": reverse('galeria-fotografo-list', request=request, format=format),
            "etiquetas": reverse('galeria-etiqueta-list', request=request, format=format),
            "imagenes": reverse('galeria-imagen-list', request=request, format=format),
        }
        
        # Enlaces a las API de gestor_multimedia
        multimedia_endpoints = {
            "tipos": reverse('multimedia-tipo-list', request=request, format=format),
            "colecciones": reverse('multimedia-coleccion-list', request=request, format=format),
            "archivos": reverse('multimedia-archivo-list', request=request, format=format),
            "comentarios": reverse('multimedia-comentario-list', request=request, format=format),
        }
        
        # Enlaces a las API de proyectos_creativos
        proyectos_endpoints = {
            "clientes": reverse('proyectos-cliente-list', request=request, format=format),
            "categorias": reverse('proyectos-categoria-list', request=request, format=format),
            "proyectos": reverse('proyectos-proyecto-list', request=request, format=format),
            "tareas": reverse('proyectos-tarea-list', request=request, format=format),
            "comentarios": reverse('proyectos-comentario-list', request=request, format=format),
        }
        
        # Enlaces a la API de ejemplo
        try:
            ejemplo_endpoints = {
                "productos": reverse('producto-list', request=request, format=format),
            }
        except:
            ejemplo_endpoints = {}
        
        # Enlaces a la API de gestión de tareas
        tareas_endpoints = {
            "listas": reverse('tareas-lista-list', request=request, format=format),
            "tareas": reverse('tareas-tarea-list', request=request, format=format),
            "etiquetas": reverse('tareas-etiqueta-list', request=request, format=format),
        }
        
        # Agrupar todos los endpoints por aplicación
        return Response({
            "galeria_api": galeria_endpoints,
            "multimedia_api": multimedia_endpoints,
            "proyectos_api": proyectos_endpoints,
            "ejemplo_api": ejemplo_endpoints,
            "tareas_api": tareas_endpoints,
        })

# La prioridad de las URLs importa, colocamos las más específicas primero
urlpatterns = [
    path('', ApiRoot.as_view(), name='api-root'),  # Root URL ahora muestra la API raíz
    path('admin/', admin.site.urls),
    path('api/', ApiRoot.as_view()),  # También mantener la URL /api/ como alternativa
    path('Ejemplo/', include('Ejemplo.urls')),
    path('galeria/', include('galeria.urls')),
    path('multimedia/', include('gestor_multimedia.urls')),
    path('proyectos/', include('proyectos_creativos.urls')),
    path('tareas/', include('Sistema_de_Gestión_de_Tareas.urls')),
]

# Añadimos esto para servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
