from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from galeria.models import Imagen

class Cliente(models.Model):
    """Cliente que solicita proyectos creativos"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    empresa = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        if self.empresa:
            return f"{self.nombre} {self.apellido} ({self.empresa})"
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']

class Categoria(models.Model):
    """Categoría de los proyectos creativos"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría de proyecto"
        verbose_name_plural = "Categorías de proyectos"
        ordering = ['nombre']

class Proyecto(models.Model):
    """Proyecto creativo principal"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('revision', 'En revisión'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE,
        related_name='proyectos'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='proyectos'
    )
    imagen_principal = models.ForeignKey(
        Imagen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proyectos_principal'
    )
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_entrega = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    presupuesto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    horas_estimadas = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-fecha_inicio']
    
    def esta_retrasado(self):
        if self.fecha_entrega and self.estado not in ('completado', 'cancelado'):
            return timezone.now().date() > self.fecha_entrega
        return False

class Tarea(models.Model):
    """Tareas específicas de un proyecto"""
    PRIORIDAD_CHOICES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
        (4, 'Urgente'),
    ]
    
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    completada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_limite = models.DateField(null=True, blank=True)
    prioridad = models.IntegerField(
        choices=PRIORIDAD_CHOICES,
        default=2
    )
    horas_dedicadas = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['-prioridad', 'fecha_limite']

class Comentario(models.Model):
    """Comentarios sobre los proyectos"""
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    autor = models.CharField(max_length=100)
    texto = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Comentario de {self.autor} en {self.proyecto.titulo}"
    
    class Meta:
        verbose_name = "Comentario de proyecto"
        verbose_name_plural = "Comentarios de proyectos"
        ordering = ['-fecha']
