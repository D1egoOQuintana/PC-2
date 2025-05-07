from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TipoArchivo, Coleccion, ArchivoMultimedia, Comentario
from .serializers import (
    TipoArchivoSerializer,
    ColeccionSerializer,
    ArchivoMultimediaListSerializer,
    ArchivoMultimediaDetailSerializer,
    ArchivoMultimediaCreateSerializer,
    ComentarioSerializer
)

# Create your views here.

class TipoArchivoViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar tipos de archivos"""
    queryset = TipoArchivo.objects.all()
    serializer_class = TipoArchivoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'extensiones_permitidas']
    template_name = None

class ColeccionViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar colecciones"""
    queryset = Coleccion.objects.all()
    serializer_class = ColeccionSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'descripcion']
    filterset_fields = ['publica']
    template_name = None

    @action(detail=True, methods=['get'])
    def archivos(self, request, pk=None):
        """Obtener todos los archivos de una colección específica"""
        coleccion = self.get_object()
        archivos = coleccion.archivos.all()
        serializer = ArchivoMultimediaListSerializer(archivos, many=True)
        return Response(serializer.data)

class ArchivoMultimediaViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar archivos multimedia"""
    queryset = ArchivoMultimedia.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descripcion']
    filterset_fields = ['tipo_archivo', 'coleccion', 'destacado']
    ordering_fields = ['fecha_subida', 'titulo', 'tamaño_bytes', 'duracion_segundos']
    template_name = None
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArchivoMultimediaDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ArchivoMultimediaCreateSerializer
        return ArchivoMultimediaListSerializer
    
    @action(detail=False, methods=['get'])
    def destacados(self, request):
        """Endpoint adicional para obtener solo los archivos destacados"""
        archivos = ArchivoMultimedia.objects.filter(destacado=True)
        serializer = self.get_serializer(archivos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def comentar(self, request, pk=None):
        """Endpoint para añadir un comentario a un archivo"""
        archivo = self.get_object()
        
        # Crear un nuevo comentario (sin aprobar por defecto)
        datos_comentario = {
            'archivo': archivo.id,
            'autor': request.data.get('autor', 'Anónimo'),
            'texto': request.data.get('texto', ''),
            'aprobado': False  # Por defecto, los comentarios requieren aprobación
        }
        
        serializer = ComentarioSerializer(data=datos_comentario)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ComentarioViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar comentarios"""
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['archivo', 'aprobado']
    template_name = None

    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        """Endpoint para aprobar un comentario"""
        comentario = self.get_object()
        comentario.aprobado = True
        comentario.save()
        serializer = self.get_serializer(comentario)
        return Response(serializer.data)
