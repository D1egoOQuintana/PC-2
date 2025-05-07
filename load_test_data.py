"""
Script para cargar datos de prueba en todas las aplicaciones
Ejecutar con: python manage.py shell < load_test_data.py
"""

import os
import django
import datetime
import random
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError

# Configuración inicial
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PC2.settings")
django.setup()

# Importar modelos
from galeria.models import Categoria as GaleriaCategoria, Fotografo, Imagen, Etiqueta
from gestor_multimedia.models import TipoArchivo, Coleccion, ArchivoMultimedia, Comentario as MultimediaComentario
from proyectos_creativos.models import Cliente, Categoria as ProyectoCategoria, Proyecto, Tarea, Comentario as ProyectoComentario

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
            if "email" in field or "nombre" in field:
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
                if "@" in value:  # es un email
                    name, domain = value.split("@")
                    kwargs[field] = f"{name}_{random.randint(1, 9999)}@{domain}"
                else:
                    kwargs[field] = f"{value}_{random.randint(1, 9999)}"
        
        try:
            return model.objects.create(**kwargs)
        except IntegrityError:
            # Último recurso
            return model.objects.first()

print_step("INICIANDO CARGA DE DATOS DE PRUEBA")

# ---------- Datos para la app Galeria ----------
print_step("Creando datos para Galeria")

# Categorías
categorias_galeria = []
categoria_names = ["Naturaleza", "Arquitectura", "Retrato"]
categoria_descs = [
    "Fotografías de paisajes y entornos naturales",
    "Fotografías de edificios y espacios arquitectónicos",
    "Fotografías de personas y retratos profesionales"
]

for i, (nombre, desc) in enumerate(zip(categoria_names, categoria_descs)):
    categoria = create_or_get(GaleriaCategoria, nombre=nombre, descripcion=desc)
    categorias_galeria.append(categoria)

print("✓ Categorías de galería creadas")

# Fotógrafos
fotografos = []
fotografo_data = [
    {
        "nombre": "Ana",
        "apellido": "Martínez",
        "email": "ana.martinez@ejemplo.com",
        "biografia": "Fotógrafa especializada en paisajes naturales con más de 10 años de experiencia."
    },
    {
        "nombre": "Carlos",
        "apellido": "Rodríguez",
        "email": "carlos.rodriguez@ejemplo.com",
        "biografia": "Fotógrafo urbano apasionado por la arquitectura moderna y los espacios públicos."
    },
    {
        "nombre": "Elena",
        "apellido": "Gómez",
        "email": "elena.gomez@ejemplo.com",
        "biografia": "Especializada en retratos y fotografía de estudio."
    }
]

for data in fotografo_data:
    fotografo = create_or_get(Fotografo, **data)
    fotografos.append(fotografo)

print("✓ Fotógrafos creados")

# Etiquetas
etiquetas = []
etiqueta_names = [
    "paisaje", "montaña", "cielo", "agua", "edificio", 
    "moderno", "antiguo", "persona", "retrato", "arte",
    "color", "blanco y negro", "urbano", "rural", "atardecer"
]

for tag in etiqueta_names:
    try:
        etiqueta = Etiqueta.objects.create(nombre=tag)
        etiquetas.append(etiqueta)
    except IntegrityError:
        etiqueta = Etiqueta.objects.get(nombre=tag)
        etiquetas.append(etiqueta)

print(f"✓ {len(etiquetas)} etiquetas creadas")

# ---------- Datos para la app Gestor Multimedia ----------
print_step("Creando datos para Gestor Multimedia")

# Tipos de archivo
tipos_archivo = []
tipo_data = [
    {
        "nombre": "Video",
        "descripcion": "Archivos de video en diferentes formatos",
        "extensiones_permitidas": "mp4,avi,mov,webm",
        "icono": "fa-video"
    },
    {
        "nombre": "Audio",
        "descripcion": "Archivos de audio en diferentes formatos",
        "extensiones_permitidas": "mp3,wav,ogg,flac",
        "icono": "fa-music"
    },
    {
        "nombre": "Documento",
        "descripcion": "Documentos de texto y presentaciones",
        "extensiones_permitidas": "pdf,doc,docx,ppt,pptx,txt",
        "icono": "fa-file-pdf"
    }
]

for data in tipo_data:
    tipo = create_or_get(TipoArchivo, **data)
    tipos_archivo.append(tipo)

print("✓ Tipos de archivo creados")

# Colecciones
colecciones = []
coleccion_data = [
    {
        "nombre": "Proyecto Marketing Digital",
        "descripcion": "Archivos relacionados con la campaña de marketing digital Q2 2025",
        "publica": True
    },
    {
        "nombre": "Presentaciones Corporativas",
        "descripcion": "Presentaciones para eventos y reuniones corporativas",
        "publica": True
    },
    {
        "nombre": "Recursos de Audio",
        "descripcion": "Música y efectos de sonido para producciones audiovisuales",
        "publica": False
    }
]

for data in coleccion_data:
    coleccion = create_or_get(Coleccion, **data)
    colecciones.append(coleccion)

print("✓ Colecciones creadas")

# ---------- Datos para la app Proyectos Creativos ----------
print_step("Creando datos para Proyectos Creativos")

# Clientes
clientes = []
cliente_data = [
    {
        "nombre": "María",
        "apellido": "López",
        "empresa": "Innovatech",
        "email": "maria.lopez@innovatech.com",
        "telefono": "555-1234"
    },
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "empresa": "Diseño Global",
        "email": "juan.perez@disenoglobal.com",
        "telefono": "555-5678"
    },
    {
        "nombre": "Laura",
        "apellido": "García",
        "email": "laura.garcia@gmail.com",
        "telefono": "555-9012"
    }
]

for data in cliente_data:
    cliente = create_or_get(Cliente, **data)
    clientes.append(cliente)

print("✓ Clientes creados")

# Categorías de proyectos
categorias_proyecto = []
cat_proyecto_data = [
    {
        "nombre": "Diseño Gráfico",
        "descripcion": "Proyectos de diseño gráfico, identidad visual y branding"
    },
    {
        "nombre": "Desarrollo Web",
        "descripcion": "Proyectos de desarrollo de sitios web y aplicaciones web"
    },
    {
        "nombre": "Marketing Digital",
        "descripcion": "Proyectos de estrategias de marketing digital y social media"
    }
]

for data in cat_proyecto_data:
    categoria = create_or_get(ProyectoCategoria, **data)
    categorias_proyecto.append(categoria)

print("✓ Categorías de proyectos creadas")

# Proyectos
proyectos = []

if clientes and categorias_proyecto:
    proyecto_data = [
        {
            "titulo": "Rediseño de Marca Innovatech",
            "descripcion": "Actualización completa de la identidad visual de Innovatech.",
            "cliente": clientes[0],
            "categoria": categorias_proyecto[0],
            "fecha_inicio": timezone.now().date(),
            "fecha_entrega": timezone.now().date() + datetime.timedelta(days=30),
            "estado": "en_proceso",
            "presupuesto": 5000.00,
            "horas_estimadas": 80
        },
        {
            "titulo": "Portal E-commerce Diseño Global",
            "descripcion": "Desarrollo de tienda online para los productos de Diseño Global.",
            "cliente": clientes[1] if len(clientes) > 1 else clientes[0],
            "categoria": categorias_proyecto[1] if len(categorias_proyecto) > 1 else categorias_proyecto[0],
            "fecha_inicio": timezone.now().date() - datetime.timedelta(days=15),
            "fecha_entrega": timezone.now().date() + datetime.timedelta(days=45),
            "estado": "en_proceso",
            "presupuesto": 8500.00,
            "horas_estimadas": 120
        },
        {
            "titulo": "Campaña Redes Sociales Verano",
            "descripcion": "Planificación y ejecución de campaña de marketing en redes sociales.",
            "cliente": clientes[2] if len(clientes) > 2 else clientes[0],
            "categoria": categorias_proyecto[2] if len(categorias_proyecto) > 2 else categorias_proyecto[0],
            "fecha_inicio": timezone.now().date() - datetime.timedelta(days=5),
            "fecha_entrega": timezone.now().date() + datetime.timedelta(days=15),
            "estado": "pendiente",
            "presupuesto": 3500.00,
            "horas_estimadas": 60
        }
    ]

    for data in proyecto_data:
        proyecto = create_or_get(Proyecto, **data)
        proyectos.append(proyecto)

print("✓ Proyectos creados")

# Tareas para los proyectos
tareas = []

if proyectos:
    # Tareas para el primer proyecto
    tareas_proyecto1 = [
        {
            "titulo": "Investigación de competencia",
            "descripcion": "Análisis de la identidad visual de competidores directos",
            "completada": True,
            "prioridad": 3,
            "proyecto": proyectos[0],
            "horas_dedicadas": 8.5
        },
        {
            "titulo": "Propuestas de logotipo",
            "descripcion": "Diseño de 3 propuestas de logotipo basadas en la investigación",
            "completada": False,
            "prioridad": 4,
            "proyecto": proyectos[0],
            "horas_dedicadas": 12.0
        },
        {
            "titulo": "Manual de marca",
            "descripcion": "Creación del manual de identidad visual",
            "completada": False,
            "prioridad": 2,
            "proyecto": proyectos[0],
            "fecha_limite": timezone.now().date() + datetime.timedelta(days=25)
        }
    ]

    for tarea_data in tareas_proyecto1:
        tarea = create_or_get(Tarea, **tarea_data)
        tareas.append(tarea)

    if len(proyectos) > 1:
        # Tareas para el segundo proyecto
        tareas_proyecto2 = [
            {
                "titulo": "Wireframes y prototipo",
                "descripcion": "Diseño de wireframes y prototipo navegable del e-commerce",
                "completada": True,
                "prioridad": 3,
                "proyecto": proyectos[1],
                "horas_dedicadas": 20.0,
                "fecha_limite": timezone.now().date() - datetime.timedelta(days=5)
            },
            {
                "titulo": "Desarrollo Frontend",
                "descripcion": "Implementación HTML, CSS y JavaScript del portal",
                "completada": False,
                "prioridad": 4,
                "proyecto": proyectos[1],
                "horas_dedicadas": 15.0,
                "fecha_limite": timezone.now().date() + datetime.timedelta(days=10)
            },
            {
                "titulo": "Integración pasarela de pagos",
                "descripcion": "Configuración e integración del sistema de pagos",
                "completada": False,
                "prioridad": 3,
                "proyecto": proyectos[1],
                "fecha_limite": timezone.now().date() + datetime.timedelta(days=30)
            }
        ]

        for tarea_data in tareas_proyecto2:
            tarea = create_or_get(Tarea, **tarea_data)
            tareas.append(tarea)

print("✓ Tareas creadas")

# Comentarios en los proyectos
comentarios = []

if proyectos:
    comentario_data = [
        {
            "proyecto": proyectos[0],
            "autor": "María (Cliente)",
            "texto": "Me gustaría ver más opciones utilizando tonos azules en el logotipo.",
            "fecha": timezone.now() - datetime.timedelta(days=2)
        },
        {
            "proyecto": proyectos[0],
            "autor": "Carlos (Diseñador)",
            "texto": "De acuerdo. Prepararé 2 propuestas adicionales con variaciones en azul para la próxima reunión.",
            "fecha": timezone.now() - datetime.timedelta(days=1)
        }
    ]

    for data in comentario_data:
        comentario = create_or_get(ProyectoComentario, **data)
        comentarios.append(comentario)

    if len(proyectos) > 1:
        comentario = create_or_get(ProyectoComentario, 
            proyecto=proyectos[1],
            autor="Juan (Cliente)",
            texto="El prototipo se ve genial. Podemos avanzar con el desarrollo.",
            fecha=timezone.now() - datetime.timedelta(days=6)
        )
        comentarios.append(comentario)

print("✓ Comentarios de proyectos creados")

print_step("CARGA DE DATOS COMPLETADA")
print("\nAhora puedes acceder al admin o a las APIs para ver los datos cargados.")
print("URLs de la API:")
print("- http://127.0.0.1:8000/galeria/api/")
print("- http://127.0.0.1:8000/multimedia/api/")
print("- http://127.0.0.1:8000/proyectos/api/")