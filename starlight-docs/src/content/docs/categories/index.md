---
title: Categorías 
description: Endpoints para categorías.
---

# Microservicio de Categorías

Este microservicio maneja toda la lógica relacionada con la gestión de categorías de productos en el sistema.

---
### Endpoints
* **GET /categories** - _Listar categorías_
* **POST /categories** - _Crear categoría_
* **GET /categories/{category_id}** - _Obtener categoría específica_
* **PUT /categories/{category_id}** - _Actualizar categoría_
* **DELETE /categories/{category_id}** - _Eliminar categoría_

---
## Listar Categorías
`GET`

| Descripción | Lista todas las categorías disponibles en el sistema. |
|:----------|:-----------------------------------------------------|
| Autorización     | Opcional (Accesible por todos los usuarios)          |

### Request (Sin body o parámetros de consulta)

### Response
**Códigos de estado posibles:** 200, 500.

`200 OK`
```json
[
  {
    "id": "cat_1",
    "nombre": "Bebidas",
    "descripcion": "Bebidas y refrescos",
    "estado": "activa",
    "fecha_creacion": "2024-01-10T08:00:00Z",
    "numero_productos": 15
  },
  {
    "id": "cat_2",
    "nombre": "Comida Rápida",
    "descripcion": "Alimentos de preparación rápida",
    "estado": "activa",
    "fecha_creacion": "2024-01-10T08:00:00Z",
    "numero_productos": 23
  },
  {
    "id": "cat_3",
    "nombre": "Postres",
    "descripcion": "Dulces y postres",
    "estado": "inactiva",
    "fecha_creacion": "2024-01-10T08:00:00Z",
    "numero_productos": 8
  }
]
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Crear Categoría
`POST`

| Descripción | Agrega una nueva categoría al sistema. |
|:----------|:--------------------------------------|
| Autorización     | Requerida (Rol: Administrador, Gestor) |

### Request
```json
{
  "name": "Celebracion de Bodas",
  "description": "fiesta de recien casados"
}
```
### Response
**Códigos de estado posibles:** 201, 400, 401, 403, 409, 500.

`201 Created`
```json
{
  "name": "Celebracion de Bodas",
  "description": "fiesta de recien casados",
  "id": 1
}
```

`400 Bad Request`
```json
{
  "detail": "El campo name es requerido"
}
```

`401 Unauthorized`
```json
{
  "detail": "Token inválido o expirado"
}
```

`403 Forbidden`
```json
{
  "detail": "Not authenticated"
}
```

`409 Conflict`
```json
{
  "detail": "Ya existe una categoría con ese nombre"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Obtener Categoría Específica
`GET`

| Descripción | Obtiene la información de una categoría específica por su ID. |
|:----------|:------------------------------------------------------------|
| Autorización     | Opcional (Accesible por todos los usuarios)                 |

### Request (Parámetros de ruta)
- `category_id` (string): ID único de la categoría

### Response
**Códigos de estado posibles:** 200, 404, 500.

`200 OK`
```json
{
  "name": "Celebracion de Bodas",
  "description": "fiesta de recien casados",
  "id": 1
}
```

`404 Not Found`
```json
{
  "detail": "La categoría no existe."
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Actualizar Categoría
`PUT`

| Descripción | Modifica la información de una categoría existente por su ID. |
|:----------|:------------------------------------------------------------|
| Autorización     | Requerida (Rol: Administrador, Gestor)                     |

### Request
```json
{
  "name": "Celebracion de Bodas",
  "description": "fiesta de recien casados, solo invitados lol"
}
```

### Response
**Códigos de estado posibles:** 200, 400, 401, 403, 404, 409, 500.

`200 OK`
```json
{
  "name": "Celebracion de Bodas",
  "description": "fiesta de recien casados, solo invitados lol",
  "id": 1
}
```

`400 Bad Request`
```json
{
  "detail": "Name no puede estar vacío"
}
```

`401 Unauthorized`
```json
{
  "detail": "Token inválido o expirado"
}
```

`403 Forbidden`
```json
{
  "detail": "Not authenticated"
}
```

`404 Not Found`
```json
{
  "detail": "Categoría no encontrada"
}
```

`409 Conflict`
```json
{
  "detail": "Ya existe una categoría con ese nombre"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Eliminar Categoría
`DELETE`

| Descripción | Elimina una categoría del sistema por su ID. |
|:----------|:--------------------------------------------|
| Autorización     | Requerida (Rol: Administrador)              |

### Request (Parámetros de ruta)
- `category_id` (string): ID único de la categoría

### Response
**Códigos de estado posibles:** 204, 400, 401, 403, 404, 500.

`204 No Content`
```
content-type: application/json 
date: Thu,20 Nov 2025 21:43:14 GMT 
server: uvicorn 
```

`400 Bad Request`
```json
{
  "detail": "No se puede eliminar una categoría que tiene productos asociados"
}
```

`401 Unauthorized`
```json
{
  "detail": "Token inválido o expirado"
}
```

`403 Forbidden`
```json
{
  "detail": "Not authenticated"
}
```

`404 Not Found`
```json
{
  "detail": "La categoría no existe."
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Estructura de Datos

### Categoría
| Campo | Tipo | Descripción |
|:------|:-----|:------------|
| id | string | Identificador único de la categoría |
| nombre | string | Nombre de la categoría |
| descripcion | string | Descripción detallada de la categoría |

### Notas de Autorización
- **Administrador**: Acceso completo a todos los endpoints
- **Gestor**: Puede crear, listar, ver y actualizar categorías
- **Todos los usuarios**: Pueden listar y ver categorías (sin necesidad de autenticación para estos endpoints)