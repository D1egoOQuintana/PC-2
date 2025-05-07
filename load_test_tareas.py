"""
Script para cargar datos de prueba en el Sistema de Gestión de Tareas
Ejecutar con: python manage.py shell < load_test_tareas.py
"""

import os
import django
import datetime
import random
from django.utils import timezone
from django.db.utils import IntegrityError

# Configuración inicial
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PC2.settings")
django.setup()

# Importar modelos del Sistema de Gestión de Tareas
from Sistema_de_Gestión_de_Tareas.models import Lista, Etiqueta, Tarea

# Función para mostrar progreso
def print_step(message):
    print(f"\n{'='*10} {message} {'='*10}")

# Función para crear objeto manejando duplicados
def create_or_get(model, **kwargs):
    """Crea un objeto o devuelve uno existente si hay conflicto de unicidad"""
    try:
        return model.objects.create(**kwargs)
    except IntegrityError:
        unique_fields = []
        for field in kwargs:
            if "nombre" in field:
                unique_fields.append((field, kwargs[field]))
        
        # Buscar por posibles campos únicos
        for field, value in unique_fields:
            filter_kwargs = {field: value}
            obj = model.objects.filter(**filter_kwargs).first()
            if obj:
                return obj
                
        # Si llegamos aquí, intentamos crear con un sufijo aleatorio para campos únicos
        for field, value in unique_fields:
            if isinstance(value, str):
                kwargs[field] = f"{value}_{random.randint(1, 9999)}"
        
        try:
            return model.objects.create(**kwargs)
        except IntegrityError:
            # Último recurso
            return model.objects.first()

print_step("INICIANDO CARGA DE DATOS DE PRUEBA PARA SISTEMA DE GESTIÓN DE TAREAS")

# ---------- Limpiar datos existentes ----------
print("Limpiando datos existentes...")
Tarea.objects.all().delete()
Lista.objects.all().delete()
Etiqueta.objects.all().delete()

# ---------- Crear 10 Listas ----------
print_step("Creando Listas")
listas = []
lista_nombres = [
    "Trabajo",
    "Personal",
    "Compras",
    "Proyecto Alpha",
    "Estudio",
    "Hogar",
    "Salud",
    "Viaje a Cancún",
    "Desarrollo Web",
    "Reuniones"
]

lista_descripciones = [
    "Tareas relacionadas con el trabajo",
    "Cosas personales por hacer",
    "Lista de compras pendientes",
    "Tareas para el proyecto Alpha",
    "Materias y cursos que estudiar",
    "Tareas de mantenimiento del hogar",
    "Citas médicas y medicamentos",
    "Planificación del viaje a Cancún",
    "Proyecto de desarrollo web personal",
    "Agenda de reuniones y eventos"
]

for i, (nombre, desc) in enumerate(zip(lista_nombres, lista_descripciones)):
    # Crear fechas escalonadas para tener variedad
    dias_atras = i * 2
    fecha_creacion = timezone.now() - datetime.timedelta(days=dias_atras)
    
    lista = create_or_get(
        Lista,
        nombre=nombre,
        descripcion=desc,
        fecha_creacion=fecha_creacion
    )
    listas.append(lista)
    print(f"✓ Lista creada: {lista.nombre}")

# ---------- Crear 10 Etiquetas ----------
print_step("Creando Etiquetas")
etiquetas = []
etiqueta_datos = [
    {"nombre": "urgente", "color": "#FF0000"},  # Rojo
    {"nombre": "importante", "color": "#FFA500"},  # Naranja
    {"nombre": "pendiente", "color": "#FFFF00"},  # Amarillo
    {"nombre": "proyecto", "color": "#008000"},  # Verde
    {"nombre": "cliente", "color": "#0000FF"},  # Azul
    {"nombre": "personal", "color": "#800080"},  # Púrpura
    {"nombre": "estudio", "color": "#FF00FF"},  # Magenta
    {"nombre": "hogar", "color": "#A52A2A"},  # Marrón
    {"nombre": "reunión", "color": "#00FFFF"},  # Cian
    {"nombre": "viaje", "color": "#008080"}   # Verde azulado
]

for dato in etiqueta_datos:
    etiqueta = create_or_get(Etiqueta, **dato)
    etiquetas.append(etiqueta)
    print(f"✓ Etiqueta creada: {etiqueta.nombre} ({etiqueta.color})")

# ---------- Crear 30 Tareas (3 por cada lista) ----------
print_step("Creando Tareas")
tareas = []

# Títulos y descripciones por categoría para hacer tareas más realistas
tareas_por_categoria = {
    "Trabajo": [
        {"titulo": "Preparar presentación", "descripcion": "Presentación para reunión del equipo", "prioridad": 3},
        {"titulo": "Enviar informe", "descripcion": "Informe mensual de avances", "prioridad": 4},
        {"titulo": "Llamar cliente", "descripcion": "Actualización sobre el proyecto", "prioridad": 2}
    ],
    "Personal": [
        {"titulo": "Comprar regalos", "descripcion": "Regalos para cumpleaños de Sara", "prioridad": 2},
        {"titulo": "Renovar documentos", "descripcion": "Pasaporte y licencia", "prioridad": 3},
        {"titulo": "Ejercicio semanal", "descripcion": "Rutina de 3 días", "prioridad": 1}
    ],
    "Compras": [
        {"titulo": "Comprar alimentos", "descripcion": "Frutas, verduras y carne", "prioridad": 3},
        {"titulo": "Material de oficina", "descripcion": "Bolígrafos, papel y carpetas", "prioridad": 1},
        {"titulo": "Regalo aniversario", "descripcion": "Buscar algo especial", "prioridad": 4}
    ],
    "Proyecto Alpha": [
        {"titulo": "Diseñar wireframes", "descripcion": "Pantallas principales de la aplicación", "prioridad": 3},
        {"titulo": "Reunión de planificación", "descripcion": "Definir próximos sprints", "prioridad": 2},
        {"titulo": "Revisar presupuesto", "descripcion": "Actualizar gastos y proyecciones", "prioridad": 4}
    ],
    "Estudio": [
        {"titulo": "Estudiar Python", "descripcion": "Capítulos 5-8 del libro", "prioridad": 2},
        {"titulo": "Preparar examen", "descripcion": "Repaso de temas principales", "prioridad": 4},
        {"titulo": "Entregar trabajo", "descripcion": "Ensayo sobre IA", "prioridad": 3}
    ],
    "Hogar": [
        {"titulo": "Reparar grifo", "descripcion": "Fuga en el baño principal", "prioridad": 3},
        {"titulo": "Pintar habitación", "descripcion": "Comprar pintura y rodillos", "prioridad": 1},
        {"titulo": "Ordenar garaje", "descripcion": "Clasificar herramientas y reciclar", "prioridad": 2}
    ],
    "Salud": [
        {"titulo": "Cita médico", "descripcion": "Revisión anual", "prioridad": 3},
        {"titulo": "Comprar medicinas", "descripcion": "Renovar receta", "prioridad": 4},
        {"titulo": "Plan dieta semanal", "descripcion": "Preparar menús saludables", "prioridad": 2}
    ],
    "Viaje a Cancún": [
        {"titulo": "Reservar hotel", "descripcion": "Buscar opciones todo incluido", "prioridad": 4},
        {"titulo": "Comprar billetes", "descripcion": "Vuelos para semana de vacaciones", "prioridad": 4},
        {"titulo": "Planificar excursiones", "descripcion": "Buscar las mejores opciones", "prioridad": 2}
    ],
    "Desarrollo Web": [
        {"titulo": "Diseñar UI", "descripcion": "Pantallas principales de la aplicación", "prioridad": 3},
        {"titulo": "Implementar backend", "descripcion": "API REST y base de datos", "prioridad": 4},
        {"titulo": "Pruebas", "descripcion": "Testing de funcionalidades principales", "prioridad": 3}
    ],
    "Reuniones": [
        {"titulo": "Reunión departamento", "descripcion": "Sala de conferencias 3", "prioridad": 3},
        {"titulo": "Llamada cliente", "descripcion": "Actualización proyecto", "prioridad": 3},
        {"titulo": "Team building", "descripcion": "Actividad de equipo mensual", "prioridad": 1}
    ]
}

estados = ['pendiente', 'en_proceso', 'completada', 'cancelada']
estado_weights = [0.5, 0.3, 0.15, 0.05]  # Probabilidades para estados

total_tareas = 0

for lista in listas:
    # Obtener tareas específicas para esta categoría
    categoria_tareas = tareas_por_categoria.get(lista.nombre, [])
    
    # Si no hay tareas específicas, crear genéricas
    if not categoria_tareas:
        categoria_tareas = [
            {"titulo": f"Tarea 1 de {lista.nombre}", "descripcion": "Descripción de la tarea 1", "prioridad": 2},
            {"titulo": f"Tarea 2 de {lista.nombre}", "descripcion": "Descripción de la tarea 2", "prioridad": 3},
            {"titulo": f"Tarea 3 de {lista.nombre}", "descripcion": "Descripción de la tarea 3", "prioridad": 1}
        ]
    
    for i, tarea_data in enumerate(categoria_tareas):
        # Generar fechas más realistas
        dias_vencimiento = random.randint(1, 30)
        fecha_vencimiento = timezone.now().date() + datetime.timedelta(days=dias_vencimiento)
        
        # Determinar estado basado en probabilidades
        estado = random.choices(estados, weights=estado_weights)[0]
        
        # Determinar si está completada basado en el estado
        completada = estado == 'completada'
        fecha_completada = timezone.now() if completada else None
        
        # Crear tarea
        tarea = create_or_get(
            Tarea,
            titulo=tarea_data["titulo"],
            descripcion=tarea_data["descripcion"],
            lista=lista,
            fecha_vencimiento=fecha_vencimiento,
            prioridad=tarea_data["prioridad"],
            estado=estado,
            completada=completada,
            fecha_completada=fecha_completada
        )
        
        # Asignar etiquetas aleatorias (entre 1 y 3)
        num_etiquetas = random.randint(1, 3)
        for etiqueta in random.sample(etiquetas, num_etiquetas):
            tarea.etiquetas.add(etiqueta)
        
        tareas.append(tarea)
        total_tareas += 1
        print(f"✓ Tarea creada: {tarea.titulo} (Lista: {lista.nombre}, Estado: {tarea.estado}, Prioridad: {tarea.prioridad})")

# ---------- Resumen ----------
print_step("CARGA DE DATOS COMPLETADA")
print(f"\nSe han creado:")
print(f"- {len(listas)} listas")
print(f"- {len(etiquetas)} etiquetas")
print(f"- {total_tareas} tareas")
print("\nPuedes acceder a la API en:")
print("- http://127.0.0.1:8000/tareas/api/")
print("- Listas: http://127.0.0.1:8000/tareas/api/listas/")
print("- Tareas: http://127.0.0.1:8000/tareas/api/tareas/")
print("- Etiquetas: http://127.0.0.1:8000/tareas/api/etiquetas/")
print("\nO desde la API raíz general en http://127.0.0.1:8000/")