# Documentación de la API del Sistema de Gestión de Tareas

Esta documentación detalla todos los endpoints disponibles en la API del Sistema de Gestión de Tareas, sus parámetros, formatos de respuesta y códigos de estado.

## Tabla de Contenidos

1. [Autenticación](#autenticación)
2. [Listas](#listas)
3. [Tareas](#tareas)
4. [Etiquetas](#etiquetas)
5. [Endpoints Especiales](#endpoints-especiales)
6. [Códigos de Estado HTTP](#códigos-de-estado-http)

## Autenticación

La API actualmente permite el acceso público. Para operaciones de escritura como POST, PUT y DELETE, se recomienda iniciar sesión a través de la interfaz del navegador.

**URL**: `/api-auth/login/`  
**Método**: GET, POST  
**Descripción**: Inicia sesión en la API para acceder a todas las operaciones CRUD.

## Listas

### Listar Todas las Listas

**URL**: `/tareas/api/listas/`  
**Método**: GET  
**Parámetros de consulta**:
- `search` (opcional): Buscar por nombre o descripción

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
[
    {
        "id": 1,
        "nombre": "Trabajo",
        "descripcion": "Tareas relacionadas con el trabajo",
        "fecha_creacion": "2025-05-07T10:00:00Z"
    },
    {
        "id": 2,
        "nombre": "Personal",
        "descripcion": "Tareas personales",
        "fecha_creacion": "2025-05-07T11:00:00Z"
    }
]
```

### Crear una Lista

**URL**: `/tareas/api/listas/`  
**Método**: POST  
**Parámetros**:
- `nombre` (requerido): Nombre de la lista
- `descripcion` (opcional): Descripción de la lista

**Ejemplo de solicitud**:
```json
{
    "nombre": "Proyectos",
    "descripcion": "Lista de proyectos pendientes"
}
```

**Respuesta Exitosa**:
- **Código**: 201 Created
- **Contenido**:
```json
{
    "id": 3,
    "nombre": "Proyectos",
    "descripcion": "Lista de proyectos pendientes",
    "fecha_creacion": "2025-05-07T12:30:45Z"
}
```

**Respuesta de Error**:
- **Código**: 400 Bad Request
- **Contenido**:
```json
{
    "nombre": ["Este campo es requerido."]
}
```

### Obtener Detalles de una Lista

**URL**: `/tareas/api/listas/{id}/`  
**Método**: GET  
**Parámetros de URL**:
- `id` (requerido): ID de la lista

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
{
    "id": 1,
    "nombre": "Trabajo",
    "descripcion": "Tareas relacionadas con el trabajo",
    "fecha_creacion": "2025-05-07T10:00:00Z",
    "tareas": [
        {
            "id": 1,
            "titulo": "Completar informe",
            "fecha_vencimiento": "2025-05-15",
            "prioridad": 3,
            "prioridad_nombre": "Alta",
            "estado": "pendiente",
            "estado_nombre": "Pendiente",
            "completada": false
        },
        {
            "id": 2,
            "titulo": "Reunión de equipo",
            "fecha_vencimiento": "2025-05-10",
            "prioridad": 2,
            "prioridad_nombre": "Media",
            "estado": "pendiente",
            "estado_nombre": "Pendiente",
            "completada": false
        }
    ],
    "total_tareas": 2,
    "tareas_completadas": 0
}
```

**Respuesta de Error**:
- **Código**: 404 Not Found
- **Contenido**:
```json
{
    "detail": "No encontrado."
}
```

### Actualizar una Lista

**URL**: `/tareas/api/listas/{id}/`  
**Método**: PUT  
**Parámetros de URL**:
- `id` (requerido): ID de la lista

**Parámetros de Cuerpo**:
- `nombre` (requerido): Nombre de la lista
- `descripcion` (opcional): Descripción de la lista

**Ejemplo de solicitud**:
```json
{
    "nombre": "Trabajo Actualizado",
    "descripcion": "Descripción actualizada"
}
```

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
{
    "id": 1,
    "nombre": "Trabajo Actualizado",
    "descripcion": "Descripción actualizada",
    "fecha_creacion": "2025-05-07T10:00:00Z"
}
```

### Eliminar una Lista

**URL**: `/tareas/api/listas/{id}/`  
**Método**: DELETE  
**Parámetros de URL**:
- `id` (requerido): ID de la lista

**Respuesta Exitosa**:
- **Código**: 204 No Content

### Obtener Tareas de una Lista

**URL**: `/tareas/api/listas/{id}/tareas/`  
**Método**: GET  
**Parámetros de URL**:
- `id` (requerido): ID de la lista

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
[
    {
        "id": 1,
        "titulo": "Completar informe",
        "fecha_vencimiento": "2025-05-15",
        "prioridad": 3,
        "prioridad_nombre": "Alta",
        "estado": "pendiente",
        "estado_nombre": "Pendiente",
        "completada": false
    },
    {
        "id": 2,
        "titulo": "Reunión de equipo",
        "fecha_vencimiento": "2025-05-10",
        "prioridad": 2,
        "prioridad_nombre": "Media",
        "estado": "pendiente",
        "estado_nombre": "Pendiente",
        "completada": false
    }
]
```

## Tareas

### Listar Todas las Tareas

**URL**: `/tareas/api/tareas/`  
**Método**: GET  
**Parámetros de consulta**:
- `search` (opcional): Buscar por título o descripción
- `estado` (opcional): Filtrar por estado (`pendiente`, `en_proceso`, `completada`, `cancelada`)
- `prioridad` (opcional): Filtrar por prioridad (1-4)
- `completada` (opcional): Filtrar por completada (`true`, `false`)
- `fecha_vencimiento` (opcional): Filtrar por fecha exacta (YYYY-MM-DD)
- `fecha_vencimiento__gte` (opcional): Filtrar por fecha mayor o igual
- `fecha_vencimiento__lte` (opcional): Filtrar por fecha menor o igual
- `lista` (opcional): Filtrar por ID de lista
- `ordering` (opcional): Ordenar resultados (`fecha_vencimiento`, `prioridad`, `fecha_creacion`)

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
[
    {
        "id": 1,
        "titulo": "Completar informe",
        "fecha_vencimiento": "2025-05-15",
        "prioridad": 3,
        "prioridad_nombre": "Alta",
        "estado": "pendiente",
        "estado_nombre": "Pendiente",
        "completada": false
    },
    {
        "id": 2,
        "titulo": "Reunión de equipo",
        "fecha_vencimiento": "2025-05-10",
        "prioridad": 2,
        "prioridad_nombre": "Media",
        "estado": "pendiente",
        "estado_nombre": "Pendiente",
        "completada": false
    }
]
```

### Crear una Tarea

**URL**: `/tareas/api/tareas/`  
**Método**: POST  
**Parámetros**:
- `titulo` (requerido): Título de la tarea
- `lista` (requerido): ID de la lista a la que pertenece
- `descripcion` (opcional): Descripción de la tarea
- `fecha_vencimiento` (opcional): Fecha de vencimiento (formato YYYY-MM-DD)
- `prioridad` (opcional): Prioridad (1-4, por defecto 2)
- `estado` (opcional): Estado (`pendiente`, `en_proceso`, `completada`, `cancelada`)
- `etiquetas` (opcional): Lista de IDs de etiquetas

**Ejemplo de solicitud**:
```json
{
    "titulo": "Preparar presentación",
    "descripcion": "Preparar presentación para la reunión",
    "lista": 1,
    "fecha_vencimiento": "2025-05-20",
    "prioridad": 3,
    "estado": "pendiente"
}
```

**Respuesta Exitosa**:
- **Código**: 201 Created
- **Contenido**:
```json
{
    "id": 3,
    "titulo": "Preparar presentación",
    "descripcion": "Preparar presentación para la reunión",
    "lista": 1,
    "fecha_creacion": "2025-05-07T14:22:30Z",
    "fecha_vencimiento": "2025-05-20",
    "prioridad": 3,
    "estado": "pendiente",
    "completada": false,
    "fecha_completada": null,
    "etiquetas": []
}
```

### Obtener Detalles de una Tarea

**URL**: `/tareas/api/tareas/{id}/`  
**Método**: GET  
**Parámetros de URL**:
- `id` (requerido): ID de la tarea

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
{
    "id": 1,
    "titulo": "Completar informe",
    "descripcion": "Informe mensual de ventas",
    "lista": 1,
    "fecha_creacion": "2025-05-07T10:15:00Z",
    "fecha_vencimiento": "2025-05-15",
    "prioridad": 3,
    "prioridad_nombre": "Alta",
    "estado": "pendiente",
    "estado_nombre": "Pendiente",
    "completada": false,
    "fecha_completada": null,
    "etiquetas": [
        {
            "id": 1,
            "nombre": "urgente",
            "color": "#FF0000"
        },
        {
            "id": 5,
            "nombre": "informe",
            "color": "#008000"
        }
    ]
}
```

### Actualizar una Tarea

**URL**: `/tareas/api/tareas/{id}/`  
**Método**: PUT  
**Parámetros de URL**:
- `id` (requerido): ID de la tarea

**Parámetros de Cuerpo**:
- `titulo` (requerido): Título de la tarea
- `lista` (requerido): ID de la lista a la que pertenece
- `descripcion` (opcional): Descripción de la tarea
- `fecha_vencimiento` (opcional): Fecha de vencimiento (formato YYYY-MM-DD)
- `prioridad` (opcional): Prioridad (1-4)
- `estado` (opcional): Estado (`pendiente`, `en_proceso`, `completada`, `cancelada`)

**Ejemplo de solicitud**:
```json
{
    "titulo": "Completar informe actualizado",
    "descripcion": "Descripción actualizada",
    "lista": 1,
    "prioridad": 4,
    "estado": "en_proceso",
    "fecha_vencimiento": "2025-05-18"
}
```

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
{
    "id": 1,
    "titulo": "Completar informe actualizado",
    "descripcion": "Descripción actualizada",
    "lista": 1,
    "fecha_creacion": "2025-05-07T10:15:00Z",
    "fecha_vencimiento": "2025-05-18",
    "prioridad": 4,
    "estado": "en_proceso",
    "completada": false,
    "fecha_completada": null,
    "etiquetas": [
        {
            "id": 1,
            "nombre": "urgente",
            "color": "#FF0000"
        },
        {
            "id": 5,
            "nombre": "informe",
            "color": "#008000"
        }
    ]
}
```

### Eliminar una Tarea

**URL**: `/tareas/api/tareas/{id}/`  
**Método**: DELETE  
**Parámetros de URL**:
- `id` (requerido): ID de la tarea

**Respuesta Exitosa**:
- **Código**: 204 No Content

## Etiquetas

### Listar Todas las Etiquetas

**URL**: `/tareas/api/etiquetas/`  
**Método**: GET  
**Parámetros de consulta**:
- `search` (opcional): Buscar por nombre

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
[
    {
        "id": 1,
        "nombre": "urgente",
        "color": "#FF0000"
    },
    {
        "id": 2,
        "nombre": "importante",
        "color": "#FFA500"
    },
    {
        "id": 3,
        "nombre": "pendiente",
        "color": "#FFFF00"
    }
]
```

### Crear una Etiqueta

**URL**: `/tareas/api/etiquetas/`  
**Método**: POST  
**Parámetros**:
- `nombre` (requerido): Nombre de la etiqueta
- `color` (opcional): Color en formato hexadecimal (por defecto "#3498DB")

**Ejemplo de solicitud**:
```json
{
    "nombre": "proyecto_especial",
    "color": "#1ABC9C"
}
```

**Respuesta Exitosa**:
- **Código**: 201 Created
- **Contenido**:
```json
{
    "id": 4,
    "nombre": "proyecto_especial",
    "color": "#1ABC9C"
}
```

### Obtener Detalles de una Etiqueta

**URL**: `/tareas/api/etiquetas/{id}/`  
**Método**: GET  
**Parámetros de URL**:
- `id` (requerido): ID de la etiqueta

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
{
    "id": 1,
    "nombre": "urgente",
    "color": "#FF0000"
}
```

### Actualizar una Etiqueta

**URL**: `/tareas/api/etiquetas/{id}/`  
**Método**: PUT  
**Parámetros de URL**:
- `id` (requerido): ID de la etiqueta

**Parámetros de Cuerpo**:
- `nombre` (requerido): Nombre de la etiqueta
- `color` (opcional): Color en formato hexadecimal

**Ejemplo de solicitud**:
```json
{
    "nombre": "muy_urgente",
    "color": "#990000"
}
```

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
{
    "id": 1,
    "nombre": "muy_urgente",
    "color": "#990000"
}
```

### Eliminar una Etiqueta

**URL**: `/tareas/api/etiquetas/{id}/`  
**Método**: DELETE  
**Parámetros de URL**:
- `id` (requerido): ID de la etiqueta

**Respuesta Exitosa**:
- **Código**: 204 No Content

### Obtener Tareas con una Etiqueta Específica

**URL**: `/tareas/api/etiquetas/{id}/tareas/`  
**Método**: GET  
**Parámetros de URL**:
- `id` (requerido): ID de la etiqueta

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
[
    {
        "id": 1,
        "titulo": "Completar informe",
        "fecha_vencimiento": "2025-05-15",
        "prioridad": 3,
        "prioridad_nombre": "Alta",
        "estado": "pendiente",
        "estado_nombre": "Pendiente",
        "completada": false
    },
    {
        "id": 5,
        "titulo": "Revisar presupuesto",
        "fecha_vencimiento": "2025-05-25",
        "prioridad": 4,
        "prioridad_nombre": "Muy Alta",
        "estado": "pendiente",
        "estado_nombre": "Pendiente",
        "completada": false
    }
]
```

## Endpoints Especiales

### Marcar una Tarea como Completada

**URL**: `/tareas/api/tareas/{id}/completar/`  
**Método**: POST  
**Parámetros de URL**:
- `id` (requerido): ID de la tarea

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
{
    "id": 1,
    "titulo": "Completar informe",
    "descripcion": "Informe mensual de ventas",
    "lista": 1,
    "fecha_creacion": "2025-05-07T10:15:00Z",
    "fecha_vencimiento": "2025-05-15",
    "prioridad": 3,
    "prioridad_nombre": "Alta",
    "estado": "completada",
    "estado_nombre": "Completada",
    "completada": true,
    "fecha_completada": "2025-05-07T15:30:00Z",
    "etiquetas": [
        {
            "id": 1,
            "nombre": "urgente",
            "color": "#FF0000"
        },
        {
            "id": 5,
            "nombre": "informe",
            "color": "#008000"
        }
    ]
}
```

**Respuesta de Error** (si ya está completada):
- **Código**: 400 Bad Request
- **Contenido**:
```json
{
    "mensaje": "Esta tarea ya está completada"
}
```

### Asignar Etiquetas a una Tarea

**URL**: `/tareas/api/tareas/{id}/asignar_etiquetas/`  
**Método**: POST  
**Parámetros de URL**:
- `id` (requerido): ID de la tarea

**Parámetros de Cuerpo**:
- `etiqueta_ids` (requerido): Lista de IDs de etiquetas para asignar

**Ejemplo de solicitud**:
```json
{
    "etiqueta_ids": [1, 2, 5]
}
```

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**: Los detalles completos de la tarea con las etiquetas asignadas
```json
{
    "id": 1,
    "titulo": "Completar informe",
    "descripcion": "Informe mensual de ventas",
    "lista": 1,
    "fecha_creacion": "2025-05-07T10:15:00Z",
    "fecha_vencimiento": "2025-05-15",
    "prioridad": 3,
    "prioridad_nombre": "Alta",
    "estado": "pendiente",
    "estado_nombre": "Pendiente",
    "completada": false,
    "fecha_completada": null,
    "etiquetas": [
        {
            "id": 1,
            "nombre": "urgente",
            "color": "#FF0000"
        },
        {
            "id": 2,
            "nombre": "importante",
            "color": "#FFA500"
        },
        {
            "id": 5,
            "nombre": "informe",
            "color": "#008000"
        }
    ]
}
```

**Respuesta de Error**:
- **Código**: 400 Bad Request
- **Contenido**:
```json
{
    "error": "Alguna de las etiquetas solicitadas no existe"
}
```

### Filtrar Tareas por Múltiples Criterios

**URL**: `/tareas/api/tareas/filtrar/`  
**Método**: GET  
**Parámetros de consulta**:
- `estado` (opcional): Filtrar por estado
- `prioridad` (opcional): Filtrar por prioridad
- `fecha_desde` (opcional): Filtrar tareas con fecha de vencimiento mayor o igual (formato YYYY-MM-DD)
- `fecha_hasta` (opcional): Filtrar tareas con fecha de vencimiento menor o igual (formato YYYY-MM-DD)
- `completada` (opcional): Filtrar por completada (`true`, `false`)
- `etiqueta` (opcional): Filtrar por ID de etiqueta

**Ejemplo de URL**:
```
/tareas/api/tareas/filtrar/?estado=pendiente&prioridad=4&fecha_desde=2025-05-15&fecha_hasta=2025-06-15&etiqueta=1
```

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Contenido**:
```json
[
    {
        "id": 5,
        "titulo": "Revisar presupuesto",
        "fecha_vencimiento": "2025-05-25",
        "prioridad": 4,
        "prioridad_nombre": "Muy Alta",
        "estado": "pendiente",
        "estado_nombre": "Pendiente",
        "completada": false
    },
    {
        "id": 8,
        "titulo": "Preparar propuesta",
        "fecha_vencimiento": "2025-06-10",
        "prioridad": 4,
        "prioridad_nombre": "Muy Alta",
        "estado": "pendiente",
        "estado_nombre": "Pendiente",
        "completada": false
    }
]
```

## Códigos de Estado HTTP

La API puede devolver los siguientes códigos de estado:

- **200 OK**: La solicitud ha tenido éxito.
- **201 Created**: La solicitud ha tenido éxito y se ha creado un nuevo recurso.
- **204 No Content**: La solicitud ha tenido éxito pero no devuelve contenido en la respuesta.
- **400 Bad Request**: La solicitud tiene un formato incorrecto o faltan datos requeridos.
- **401 Unauthorized**: Es necesario autenticar para obtener la respuesta solicitada.
- **403 Forbidden**: El servidor ha entendido la solicitud pero se niega a autorizarla.
- **404 Not Found**: El servidor no pudo encontrar el contenido solicitado.
- **405 Method Not Allowed**: El método solicitado no está permitido para el recurso.
- **500 Internal Server Error**: Error interno del servidor.