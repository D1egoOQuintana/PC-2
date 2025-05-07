from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Lista(models.Model):
    """Modelo para las listas de tareas"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Lista"
        verbose_name_plural = "Listas"
        ordering = ['fecha_creacion']

class Etiqueta(models.Model):
    """Modelo para las etiquetas que pueden aplicarse a tareas"""
    nombre = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#1976D2", help_text="Color en formato hexadecimal")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ['nombre']

class Tarea(models.Model):
    """Modelo para tareas individuales"""
    PRIORIDAD_CHOICES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
        (4, 'Urgente'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='tareas')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    prioridad = models.IntegerField(
        choices=PRIORIDAD_CHOICES,
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    completada = models.BooleanField(default=False)
    fecha_completada = models.DateTimeField(null=True, blank=True)
    etiquetas = models.ManyToManyField(Etiqueta, related_name='tareas', blank=True)
    
    def __str__(self):
        return self.titulo
    
    def marcar_como_completada(self):
        self.completada = True
        self.estado = 'completada'
        self.fecha_completada = timezone.now()
        self.save()
    
    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['-prioridad', 'fecha_vencimiento']
