from django.contrib import admin
from .models import Cliente, Categoria, Proyecto, Tarea, Comentario

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'empresa', 'email', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email', 'empresa')
    list_filter = ('fecha_registro',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'categoria', 'estado', 'fecha_inicio', 'fecha_entrega', 'presupuesto')
    list_filter = ('estado', 'categoria')
    search_fields = ('titulo', 'descripcion', 'cliente__nombre', 'cliente__apellido')
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'descripcion', 'imagen_principal')
        }),
        ('Cliente y categoría', {
            'fields': ('cliente', 'categoria')
        }),
        ('Fechas y estado', {
            'fields': ('fecha_inicio', 'fecha_entrega', 'estado')
        }),
        ('Presupuesto y tiempo', {
            'fields': ('presupuesto', 'horas_estimadas')
        }),
    )

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proyecto', 'completada', 'prioridad', 'fecha_limite')
    list_filter = ('completada', 'prioridad', 'fecha_limite')
    search_fields = ('titulo', 'descripcion', 'proyecto__titulo')
    actions = ['marcar_completadas']
    
    def marcar_completadas(self, request, queryset):
        queryset.update(completada=True)
        self.message_user(request, f"{queryset.count()} tareas han sido marcadas como completadas.")
    marcar_completadas.short_description = "Marcar tareas seleccionadas como completadas"

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'proyecto', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('autor', 'texto', 'proyecto__titulo')
