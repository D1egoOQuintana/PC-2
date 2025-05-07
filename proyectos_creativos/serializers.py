from rest_framework import serializers
from .models import Cliente, Categoria, Proyecto, Tarea, Comentario
from galeria.serializers import ImagenListSerializer

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

class TareaListSerializer(serializers.ModelSerializer):
    prioridad_display = serializers.CharField(source='get_prioridad_display', read_only=True)
    
    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'completada', 'fecha_limite', 'prioridad', 'prioridad_display']

class ProyectoListSerializer(serializers.ModelSerializer):
    """Serializador para listar proyectos con información básica"""
    cliente_nombre = serializers.SerializerMethodField()
    categoria_nombre = serializers.CharField(source='categoria.nombre')
    estado_display = serializers.CharField(source='get_estado_display')
    esta_retrasado = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Proyecto
        fields = ['id', 'titulo', 'cliente_nombre', 'categoria_nombre',
                 'fecha_inicio', 'fecha_entrega', 'estado', 'estado_display',
                 'esta_retrasado', 'presupuesto']
    
    def get_cliente_nombre(self, obj):
        return str(obj.cliente)

class ProyectoDetailSerializer(serializers.ModelSerializer):
    """Serializador para ver detalles completos de un proyecto"""
    cliente = ClienteSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    imagen_principal = ImagenListSerializer(read_only=True)
    tareas = TareaListSerializer(many=True, read_only=True)
    comentarios = ComentarioSerializer(many=True, read_only=True)
    estado_display = serializers.CharField(source='get_estado_display')
    esta_retrasado = serializers.SerializerMethodField()
    
    class Meta:
        model = Proyecto
        fields = '__all__'
    
    def get_esta_retrasado(self, obj):
        return obj.esta_retrasado()

class ProyectoCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear o actualizar proyectos"""
    class Meta:
        model = Proyecto
        fields = '__all__'