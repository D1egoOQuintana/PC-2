# PC2 - Plataforma de Gestión Multimedia y Tareas

Bienvenido a PC2, una plataforma modular construida con Django y Django REST Framework. Este proyecto integra varias aplicaciones para la gestión de imágenes, archivos multimedia, proyectos creativos y un sistema avanzado de gestión de tareas.

---

## Tabla de Contenidos
- [Características Principales](#características-principales)
- [Requisitos](#requisitos)
- [Instalación y Puesta en Marcha](#instalación-y-puesta-en-marcha)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Acceso y Navegación](#acceso-y-navegación)
- [Sistema de Gestión de Tareas (API Detallada)](#sistema-de-gestión-de-tareas-api-detallada)
- [Carga de Datos de Prueba](#carga-de-datos-de-prueba)
- [Pruebas Automatizadas](#pruebas-automatizadas)
- [Notas Finales](#notas-finales)

---

## Características Principales
- **Gestión de Galería:** Categorías, fotógrafos, etiquetas e imágenes.
- **Gestión Multimedia:** Archivos, colecciones, tipos y comentarios.
- **Proyectos Creativos:** Proyectos, clientes, tareas y comentarios.
- **Sistema de Gestión de Tareas:** Listas, tareas, etiquetas, filtrado avanzado, endpoints especiales y documentación exhaustiva.

---

## Requisitos
- Python 3.10+
- pip
- (Opcional) virtualenv

---

## Instalación y Puesta en Marcha

1. **Clona el repositorio o copia los archivos a tu máquina.**
2. **Instala las dependencias:**
   ```bash
   pip install django djangorestframework django-filter
   ```
3. **Realiza las migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Crea un superusuario para acceder al admin (opcional):**
   ```bash
   python manage.py createsuperuser
   ```
5. **Inicia el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
6. **(Opcional) Carga datos de prueba para el sistema de tareas:**
   ```bash
   python manage.py shell < load_test_tareas.py
   ```

---

## Estructura del Proyecto

- `PC2/` - Configuración principal del proyecto Django
- `Ejemplo/` - App de ejemplo (CRUD básico de productos)
- `galeria/` - Gestión de imágenes, categorías, fotógrafos, etc.
- `gestor_multimedia/` - Gestión de archivos multimedia
- `proyectos_creativos/` - Gestión de proyectos, clientes, tareas creativas
- `Sistema_de_Gestión_de_Tareas/` - **Sistema completo de gestión de tareas (CRUD, filtrado, etiquetas, etc.)**
- `load_test_tareas.py` - Script para cargar datos de prueba en el sistema de tareas

---

## Acceso y Navegación

- **Admin Django:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **API Root:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **API de Ejemplo:** [http://127.0.0.1:8000/Ejemplo/api/productos/](http://127.0.0.1:8000/Ejemplo/api/productos/)
- **API de Galería:** [http://127.0.0.1:8000/galeria/api/](http://127.0.0.1:8000/galeria/api/)
- **API de Multimedia:** [http://127.0.0.1:8000/multimedia/api/](http://127.0.0.1:8000/multimedia/api/)
- **API de Proyectos Creativos:** [http://127.0.0.1:8000/proyectos/api/](http://127.0.0.1:8000/proyectos/api/)
- **API de Sistema de Gestión de Tareas:** [http://127.0.0.1:8000/tareas/api/](http://127.0.0.1:8000/tareas/api/)

> **Nota:** Para las apps que no sean el sistema de tareas, consulta los endpoints navegando por la API root o revisando los archivos `urls.py` y `serializers.py` de cada app.

---

# Sistema de Gestión de Tareas (API Detallada)

La app **Sistema_de_Gestión_de_Tareas** permite gestionar listas, tareas y etiquetas, con endpoints avanzados para marcar tareas como completadas, filtrado por criterios y asignación de etiquetas.

## Tabla Resumida de Endpoints

| Recurso   | Método | Endpoint                                         | Descripción                                 |
|-----------|--------|--------------------------------------------------|---------------------------------------------|
| Listas    | GET    | `/tareas/api/listas/`                            | Listar todas las listas                     |
|           | POST   | `/tareas/api/listas/`                            | Crear una nueva lista                       |
|           | GET    | `/tareas/api/listas/{id}/`                       | Obtener detalles de una lista               |
|           | PUT    | `/tareas/api/listas/{id}/`                       | Actualizar una lista                        |
|           | DELETE | `/tareas/api/listas/{id}/`                       | Eliminar una lista                          |
|           | GET    | `/tareas/api/listas/{id}/tareas/`                | Listar tareas de una lista                  |
| Tareas    | GET    | `/tareas/api/tareas/`                            | Listar todas las tareas (con filtros)       |
|           | POST   | `/tareas/api/tareas/`                            | Crear una nueva tarea                       |
|           | GET    | `/tareas/api/tareas/{id}/`                       | Obtener detalles de una tarea               |
|           | PUT    | `/tareas/api/tareas/{id}/`                       | Actualizar una tarea                        |
|           | DELETE | `/tareas/api/tareas/{id}/`                       | Eliminar una tarea                          |
|           | POST   | `/tareas/api/tareas/{id}/completar/`             | Marcar tarea como completada                |
|           | POST   | `/tareas/api/tareas/{id}/asignar_etiquetas/`     | Asignar etiquetas a una tarea               |
|           | GET    | `/tareas/api/tareas/filtrar/`                    | Filtrar tareas por criterios                |
| Etiquetas | GET    | `/tareas/api/etiquetas/`                         | Listar todas las etiquetas                  |
|           | POST   | `/tareas/api/etiquetas/`                         | Crear una nueva etiqueta                    |
|           | GET    | `/tareas/api/etiquetas/{id}/`                    | Obtener detalles de una etiqueta            |
|           | PUT    | `/tareas/api/etiquetas/{id}/`                    | Actualizar una etiqueta                     |
|           | DELETE | `/tareas/api/etiquetas/{id}/`                    | Eliminar una etiqueta                       |
|           | GET    | `/tareas/api/etiquetas/{id}/tareas/`             | Listar tareas con una etiqueta              |

## Ejemplo de Uso de la API de Tareas

### Crear una Tarea
```http
POST /tareas/api/tareas/
Content-Type: application/json
{
  "titulo": "Preparar informe",
  "descripcion": "Informe mensual",
  "lista": 1,
  "fecha_vencimiento": "2025-05-15",
  "prioridad": 3,
  "estado": "pendiente"
}
```
**Respuesta:**
```json
{
  "id": 1,
  "titulo": "Preparar informe",
  "descripcion": "Informe mensual",
  "lista": 1,
  "fecha_creacion": "2025-05-07T10:00:00Z",
  "fecha_vencimiento": "2025-05-15",
  "prioridad": 3,
  "estado": "pendiente",
  "completada": false,
  "fecha_completada": null,
  "etiquetas": []
}
```

### Marcar tarea como completada
```http
POST /tareas/api/tareas/{id}/completar/
```
**Respuesta:**
```json
{
  "id": 1,
  "titulo": "Preparar informe",
  "estado": "completada",
  "completada": true,
  ...
}
```

### Filtrar tareas
```http
GET /tareas/api/tareas/filtrar/?estado=pendiente&prioridad=3
```
**Respuesta:**
```json
[
  {
    "id": 1,
    "titulo": "Preparar informe",
    "prioridad": 3,
    "estado": "pendiente",
    ...
  }
]
```

### Asignar etiquetas a una tarea
```http
POST /tareas/api/tareas/{id}/asignar_etiquetas/
Content-Type: application/json
{
  "etiqueta_ids": [1, 2]
}
```
**Respuesta:** Detalles completos de la tarea con las etiquetas asignadas

### Más ejemplos y detalles
Para la documentación completa de todos los endpoints, parámetros, ejemplos de respuesta y códigos de estado, revisa el archivo [`Sistema_de_Gestión_de_Tareas/api_docs.md`](Sistema_de_Gestión_de_Tareas/api_docs.md).

---

## Carga de Datos de Prueba

Puedes cargar datos de ejemplo para el sistema de tareas ejecutando:
```bash
python manage.py shell < load_test_tareas.py
```
Esto creará 10 listas, 10 etiquetas y 30 tareas de ejemplo.

---

## Pruebas Automatizadas

Para ejecutar las pruebas automatizadas del sistema de tareas:
```bash
python manage.py test Sistema_de_Gestión_de_Tareas
```

---

## Notas Finales
- Para las demás apps (galería, multimedia, proyectos, ejemplo), consulta la API root o los archivos de cada app para ver los endpoints disponibles.
- El sistema de gestión de tareas es completamente funcional y documentado para pruebas y desarrollo.
- Si tienes dudas sobre los endpoints, revisa la documentación detallada en [`Sistema_de_Gestión_de_Tareas/api_docs.md`](Sistema_de_Gestión_de_Tareas/api_docs.md).