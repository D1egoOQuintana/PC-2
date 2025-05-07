from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lista, Tarea, Etiqueta
from .serializers import (
    ListaSerializer, 
    ListaDetailSerializer, 
    TareaListSerializer, 
    TareaDetailSerializer,
    TareaCreateSerializer,
    EtiquetaSerializer,
    TareaEtiquetaSerializer
)

class ListaViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar listas"""
    queryset = Lista.objects.all()
    serializer_class = ListaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'descripcion']
    template_name = None
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ListaDetailSerializer
        return ListaSerializer
    
    @action(detail=True, methods=['get'])
    def tareas(self, request, pk=None):
        """Endpoint para listar todas las tareas de una lista específica"""
        lista = self.get_object()
        tareas = lista.tareas.all()
        serializer = TareaListSerializer(tareas, many=True)
        return Response(serializer.data)

class TareaViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar tareas"""
    queryset = Tarea.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['titulo', 'descripcion']
    filterset_fields = {
        'estado': ['exact'],
        'prioridad': ['exact', 'gte', 'lte'],
        'completada': ['exact'],
        'fecha_vencimiento': ['exact', 'gte', 'lte'],
        'lista': ['exact']
    }
    ordering_fields = ['fecha_vencimiento', 'prioridad', 'fecha_creacion']
    template_name = None
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TareaDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TareaCreateSerializer
        return TareaListSerializer
    
    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        """Endpoint para marcar una tarea como completada"""
        tarea = self.get_object()
        if tarea.completada:
            return Response({'mensaje': 'Esta tarea ya está completada'}, status=status.HTTP_400_BAD_REQUEST)
        
        tarea.marcar_como_completada()
        serializer = TareaDetailSerializer(tarea)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def asignar_etiquetas(self, request, pk=None):
        """Endpoint para asignar etiquetas a una tarea"""
        tarea = self.get_object()
        serializer = TareaEtiquetaSerializer(data=request.data)
        
        if serializer.is_valid():
            etiqueta_ids = serializer.validated_data.get('etiqueta_ids', [])
            etiquetas = Etiqueta.objects.filter(id__in=etiqueta_ids)
            
            # Verificar que todas las etiquetas existan
            if len(etiquetas) != len(etiqueta_ids):
                return Response(
                    {'error': 'Alguna de las etiquetas solicitadas no existe'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Asignar etiquetas a la tarea
            tarea.etiquetas.set(etiquetas)
            return Response(TareaDetailSerializer(tarea).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def filtrar(self, request):
        """Endpoint avanzado para filtrar tareas por múltiples criterios"""
        queryset = self.queryset
        
        # Filtrar por estado
        estado = request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtrar por prioridad
        prioridad = request.query_params.get('prioridad', None)
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
            
        # Filtrar por fecha de vencimiento
        fecha_desde = request.query_params.get('fecha_desde', None)
        if fecha_desde:
            queryset = queryset.filter(fecha_vencimiento__gte=fecha_desde)
            
        fecha_hasta = request.query_params.get('fecha_hasta', None)
        if fecha_hasta:
            queryset = queryset.filter(fecha_vencimiento__lte=fecha_hasta)
        
        # Filtrar por completada
        completada = request.query_params.get('completada', None)
        if completada is not None:
            completada = completada.lower() == 'true'
            queryset = queryset.filter(completada=completada)
            
        # Filtrar por etiqueta
        etiqueta_id = request.query_params.get('etiqueta', None)
        if etiqueta_id:
            queryset = queryset.filter(etiquetas__id=etiqueta_id)
            
        # Serializar y devolver resultados
        serializer = TareaListSerializer(queryset, many=True)
        return Response(serializer.data)

class EtiquetaViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar etiquetas"""
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
    template_name = None
    
    @action(detail=True, methods=['get'])
    def tareas(self, request, pk=None):
        """Endpoint para obtener todas las tareas con esta etiqueta"""
        etiqueta = self.get_object()
        tareas = etiqueta.tareas.all()
        serializer = TareaListSerializer(tareas, many=True)
        return Response(serializer.data)
