from django.contrib import admin
from .models import TipoArchivo, Coleccion, ArchivoMultimedia, Comentario

@admin.register(TipoArchivo)
class TipoArchivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'extensiones_permitidas', 'icono')
    search_fields = ('nombre', 'extensiones_permitidas')

@admin.register(Coleccion)
class ColeccionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion', 'publica')
    list_filter = ('publica',)
    search_fields = ('nombre', 'descripcion')

@admin.register(ArchivoMultimedia)
class ArchivoMultimediaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_archivo', 'coleccion', 'fecha_subida', 'destacado')
    list_filter = ('tipo_archivo', 'coleccion', 'destacado')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('fecha_subida', 'tamaño_bytes')
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'descripcion', 'archivo', 'miniatura')
        }),
        ('Clasificación', {
            'fields': ('tipo_archivo', 'coleccion')
        }),
        ('Metadatos', {
            'fields': ('fecha_subida', 'tamaño_bytes', 'duracion_segundos', 'destacado')
        }),
    )

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'archivo', 'fecha_creacion', 'aprobado')
    list_filter = ('aprobado', 'fecha_creacion')
    search_fields = ('autor', 'texto')
    actions = ['aprobar_comentarios']
    
    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)
        self.message_user(request, f"{queryset.count()} comentarios han sido aprobados.")
    aprobar_comentarios.short_description = "Aprobar comentarios seleccionados"
