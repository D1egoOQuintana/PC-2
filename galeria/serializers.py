from rest_framework import serializers
from .models import Categoria, Fotografo, Imagen, Etiqueta

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class FotografoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotografo
        fields = '__all__'

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

class ImagenListSerializer(serializers.ModelSerializer):
    """Serializador para listar imágenes con información básica"""
    fotografo_nombre = serializers.StringRelatedField(source='fotografo')
    categoria_nombre = serializers.StringRelatedField(source='categoria')
    
    class Meta:
        model = Imagen
        fields = ['id', 'titulo', 'archivo', 'fecha_subida', 
                  'fotografo_nombre', 'categoria_nombre', 'destacada']

class ImagenDetailSerializer(serializers.ModelSerializer):
    """Serializador para mostrar detalles de una imagen con información completa"""
    fotografo = FotografoSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    etiquetas = EtiquetaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Imagen
        fields = '__all__'

class ImagenCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear imágenes"""
    class Meta:
        model = Imagen
        fields = '__all__'