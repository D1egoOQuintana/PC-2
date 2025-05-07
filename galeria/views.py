from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Fotografo, Imagen, Etiqueta
from .serializers import (
    CategoriaSerializer, 
    FotografoSerializer, 
    ImagenListSerializer,
    ImagenDetailSerializer,
    ImagenCreateSerializer,
    EtiquetaSerializer
)

# API ViewSets
class CategoriaViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar categorías"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class FotografoViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar fotógrafos"""
    queryset = Fotografo.objects.all()
    serializer_class = FotografoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'apellido', 'email']

class EtiquetaViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar etiquetas"""
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class ImagenViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar imágenes"""
    queryset = Imagen.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Quitamos DjangoFilterBackend
    search_fields = ['titulo', 'descripcion', 'fotografo__nombre', 'categoria__nombre']
    ordering_fields = ['fecha_subida', 'titulo']
    template_name = None  # Esto evita que busque la plantilla de filtros
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ImagenDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ImagenCreateSerializer
        return ImagenListSerializer
    
    @action(detail=False, methods=['get'])
    def destacadas(self, request):
        """Endpoint adicional para obtener solo las imágenes destacadas"""
        imagenes = Imagen.objects.filter(destacada=True)
        serializer = self.get_serializer(imagenes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request, categoria_id=None):
        """Endpoint adicional para filtrar por categoría"""
        categoria_id = request.query_params.get('categoria_id')
        if categoria_id:
            imagenes = Imagen.objects.filter(categoria_id=categoria_id)
        else:
            imagenes = Imagen.objects.all()
        serializer = self.get_serializer(imagenes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_fotografo(self, request, fotografo_id=None):
        """Endpoint adicional para filtrar por fotógrafo"""
        fotografo_id = request.query_params.get('fotografo_id')
        if fotografo_id:
            imagenes = Imagen.objects.filter(fotografo_id=fotografo_id)
        else:
            imagenes = Imagen.objects.all()
        serializer = self.get_serializer(imagenes, many=True)
        return Response(serializer.data)
