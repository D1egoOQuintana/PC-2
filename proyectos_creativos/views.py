from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cliente, Categoria, Proyecto, Tarea, Comentario
from .serializers import (
    ClienteSerializer,
    CategoriaSerializer,
    ProyectoListSerializer,
    ProyectoDetailSerializer,
    ProyectoCreateSerializer,
    TareaSerializer,
    TareaListSerializer,
    ComentarioSerializer
)

class ClienteViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'apellido', 'email', 'empresa']
    template_name = None

class CategoriaViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar categorías de proyectos"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
    template_name = None

class ProyectoViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar proyectos"""
    queryset = Proyecto.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descripcion', 'cliente__nombre', 'cliente__apellido']
    ordering_fields = ['fecha_inicio', 'fecha_entrega', 'presupuesto']
    template_name = None
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProyectoDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProyectoCreateSerializer
        return ProyectoListSerializer
    
    @action(detail=True, methods=['get'])
    def tareas(self, request, pk=None):
        """Obtener las tareas de un proyecto específico"""
        proyecto = self.get_object()
        tareas = proyecto.tareas.all()
        serializer = TareaListSerializer(tareas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def comentar(self, request, pk=None):
        """Endpoint para añadir un comentario a un proyecto"""
        proyecto = self.get_object()
        
        datos_comentario = {
            'proyecto': proyecto.id,
            'autor': request.data.get('autor', 'Anónimo'),
            'texto': request.data.get('texto', ''),
        }
        
        serializer = ComentarioSerializer(data=datos_comentario)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def retrasados(self, request):
        """Endpoint para obtener proyectos retrasados"""
        from django.utils import timezone
        from datetime import timedelta
        
        proyectos = Proyecto.objects.filter(
            fecha_entrega__lt=timezone.now().date(),
            estado__in=['pendiente', 'en_proceso', 'revision']
        )
        
        serializer = self.get_serializer(proyectos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_estado(self, request):
        """Endpoint para agrupar proyectos por estado"""
        estado = request.query_params.get('estado')
        if estado:
            proyectos = Proyecto.objects.filter(estado=estado)
        else:
            proyectos = Proyecto.objects.all()
            
        serializer = self.get_serializer(proyectos, many=True)
        return Response(serializer.data)

class TareaViewSet(viewsets.ModelViewSet):
    """API endpoint para ver y editar tareas"""
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha_limite', 'prioridad']
    template_name = None
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TareaListSerializer
        return TareaSerializer
    
    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        """Endpoint para marcar una tarea como completada"""
        tarea = self.get_object()
        tarea.completada = True
        tarea.save()
        serializer = self.get_serializer(tarea)
        return Response(serializer.data)

class ComentarioViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar comentarios de proyectos"""
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['autor', 'texto']
    template_name = None
