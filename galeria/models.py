from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    """Categoría para organizar las imágenes"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

class Fotografo(models.Model):
    """Información sobre el fotógrafo o autor de las imágenes"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    biografia = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        verbose_name = "Fotógrafo"
        verbose_name_plural = "Fotógrafos"
        ordering = ['apellido', 'nombre']

class Imagen(models.Model):
    """Modelo principal para almacenar las imágenes"""
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    archivo = models.ImageField(upload_to='galeria/imagenes/')
    fecha_subida = models.DateTimeField(default=timezone.now)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='imagenes'
    )
    fotografo = models.ForeignKey(
        Fotografo, 
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    # Campos adicionales
    ubicacion = models.CharField(max_length=200, blank=True)
    fecha_captura = models.DateField(null=True, blank=True)
    destacada = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"
        ordering = ['-fecha_subida']

class Etiqueta(models.Model):
    """Etiquetas para clasificar imágenes"""
    nombre = models.CharField(max_length=50, unique=True)
    imagenes = models.ManyToManyField(
        Imagen, 
        related_name='etiquetas',
        blank=True
    )
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ['nombre']
