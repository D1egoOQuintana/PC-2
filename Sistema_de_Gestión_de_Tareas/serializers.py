from rest_framework import serializers
from .models import Lista, Tarea, Etiqueta

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

class TareaListSerializer(serializers.ModelSerializer):
    """Serializador para listar tareas con información básica"""
    prioridad_nombre = serializers.CharField(source='get_prioridad_display', read_only=True)
    estado_nombre = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'fecha_vencimiento', 'prioridad', 'prioridad_nombre', 
                  'estado', 'estado_nombre', 'completada']

class TareaDetailSerializer(serializers.ModelSerializer):
    """Serializador para ver detalles completos de una tarea"""
    prioridad_nombre = serializers.CharField(source='get_prioridad_display', read_only=True)
    estado_nombre = serializers.CharField(source='get_estado_display', read_only=True)
    etiquetas = EtiquetaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tarea
        fields = '__all__'

class TareaCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear o actualizar tareas"""
    class Meta:
        model = Tarea
        fields = '__all__'

class ListaSerializer(serializers.ModelSerializer):
    """Serializador básico para listas"""
    class Meta:
        model = Lista
        fields = '__all__'

class ListaDetailSerializer(serializers.ModelSerializer):
    """Serializador para ver detalles de una lista con sus tareas"""
    tareas = TareaListSerializer(many=True, read_only=True)
    total_tareas = serializers.SerializerMethodField()
    tareas_completadas = serializers.SerializerMethodField()
    
    class Meta:
        model = Lista
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 
                  'tareas', 'total_tareas', 'tareas_completadas']
    
    def get_total_tareas(self, obj):
        return obj.tareas.count()
    
    def get_tareas_completadas(self, obj):
        return obj.tareas.filter(completada=True).count()

class TareaEtiquetaSerializer(serializers.Serializer):
    """Serializador para asignar etiquetas a tareas"""
    etiqueta_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="Lista de IDs de etiquetas para asignar a la tarea"
    )