from django.contrib import admin
from .models import Categoria, Fotografo, Imagen, Etiqueta

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion')
    search_fields = ('nombre',)

@admin.register(Fotografo)
class FotografoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email')

@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'fotografo', 'fecha_subida', 'destacada')
    list_filter = ('categoria', 'fotografo', 'destacada')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('fecha_subida',)
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'descripcion', 'archivo')
        }),
        ('Clasificación', {
            'fields': ('categoria', 'fotografo')
        }),
        ('Metadatos', {
            'fields': ('fecha_subida', 'fecha_captura', 'ubicacion', 'destacada')
        }),
    )

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    filter_horizontal = ('imagenes',)
