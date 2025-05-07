from rest_framework import serializers
from .models import TipoArchivo, Coleccion, ArchivoMultimedia, Comentario

class TipoArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoArchivo
        fields = '__all__'

class ColeccionSerializer(serializers.ModelSerializer):
    num_archivos = serializers.SerializerMethodField()
    
    class Meta:
        model = Coleccion
        fields = '__all__'
    
    def get_num_archivos(self, obj):
        return obj.archivos.count()

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

class ArchivoMultimediaListSerializer(serializers.ModelSerializer):
    """Serializador para listar archivos multimedia con información básica"""
    tipo_archivo_nombre = serializers.StringRelatedField(source='tipo_archivo')
    coleccion_nombre = serializers.StringRelatedField(source='coleccion')
    
    class Meta:
        model = ArchivoMultimedia
        fields = ['id', 'titulo', 'archivo', 'miniatura', 'fecha_subida', 
                  'tipo_archivo_nombre', 'coleccion_nombre', 'destacado']

class ArchivoMultimediaDetailSerializer(serializers.ModelSerializer):
    """Serializador para mostrar detalles completos de un archivo multimedia"""
    tipo_archivo = TipoArchivoSerializer(read_only=True)
    coleccion = ColeccionSerializer(read_only=True)
    comentarios = serializers.SerializerMethodField()
    
    class Meta:
        model = ArchivoMultimedia
        fields = '__all__'
    
    def get_comentarios(self, obj):
        # Solo mostrar comentarios aprobados
        comentarios = obj.comentarios.filter(aprobado=True)
        return ComentarioSerializer(comentarios, many=True).data

class ArchivoMultimediaCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear archivos multimedia"""
    class Meta:
        model = ArchivoMultimedia
        fields = '__all__'
    
    def validate(self, data):
        """Validación adicional para asegurar que el archivo cumple con el tipo requerido"""
        if 'archivo' in data and 'tipo_archivo' in data:
            archivo = data['archivo']
            tipo_archivo = data['tipo_archivo']
            extensiones_permitidas = tipo_archivo.extensiones_permitidas.split(',')
            
            # Obtener la extensión del archivo (sin el punto)
            extension = archivo.name.split('.')[-1].lower()
            
            if extension not in extensiones_permitidas:
                raise serializers.ValidationError(
                    f"El archivo no tiene una extensión permitida para este tipo. "
                    f"Extensiones permitidas: {', '.join(extensiones_permitidas)}"
                )
        
        return data