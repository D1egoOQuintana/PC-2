from django.contrib import admin
from .models import Lista, Tarea, Etiqueta

@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_creacion',)

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color')
    search_fields = ('nombre',)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'lista', 'estado', 'prioridad', 'fecha_vencimiento', 'completada')
    list_filter = ('estado', 'prioridad', 'completada', 'lista')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha_creacion'
    filter_horizontal = ('etiquetas',)
    actions = ['marcar_como_completadas']
    
    def marcar_como_completadas(self, request, queryset):
        for tarea in queryset:
            tarea.marcar_como_completada()
        self.message_user(request, f"{queryset.count()} tareas marcadas como completadas.")
    
    marcar_como_completadas.short_description = "Marcar tareas seleccionadas como completadas"
