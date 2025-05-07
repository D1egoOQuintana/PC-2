from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class TipoArchivo(models.Model):
    """Clasificación del tipo de archivo multimedia"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    extensiones_permitidas = models.CharField(
        max_length=200,
        help_text='Extensiones separadas por comas (ej: mp4,avi,mov)'
    )
    icono = models.CharField(
        max_length=50, 
        blank=True,
        help_text='Clase CSS para el icono (ej: fa-video)'
    )

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Tipo de Archivo"
        verbose_name_plural = "Tipos de Archivos"
        ordering = ['nombre']

class Coleccion(models.Model):
    """Agrupación de archivos multimedia"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    publica = models.BooleanField(default=True)
    miniatura = models.ImageField(
        upload_to='colecciones/miniaturas/', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Colección"
        verbose_name_plural = "Colecciones"
        ordering = ['-fecha_creacion']

class ArchivoMultimedia(models.Model):
    """Modelo principal para almacenar archivos multimedia"""
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(
        upload_to='multimedia/archivos/',
        validators=[FileExtensionValidator(
            allowed_extensions=['mp4', 'avi', 'mov', 'mp3', 'wav', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']
        )]
    )
    miniatura = models.ImageField(
        upload_to='multimedia/miniaturas/', 
        blank=True, 
        null=True
    )
    fecha_subida = models.DateTimeField(default=timezone.now)
    tipo_archivo = models.ForeignKey(
        TipoArchivo, 
        on_delete=models.CASCADE,
        related_name='archivos'
    )
    coleccion = models.ForeignKey(
        Coleccion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='archivos'
    )
    tamaño_bytes = models.BigIntegerField(default=0)
    duracion_segundos = models.IntegerField(null=True, blank=True)
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Archivo Multimedia"
        verbose_name_plural = "Archivos Multimedia"
        ordering = ['-fecha_subida']

class Comentario(models.Model):
    """Comentarios sobre los archivos multimedia"""
    archivo = models.ForeignKey(
        ArchivoMultimedia, 
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    autor = models.CharField(max_length=100)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"Comentario de {self.autor} en {self.archivo.titulo}"

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-fecha_creacion']
