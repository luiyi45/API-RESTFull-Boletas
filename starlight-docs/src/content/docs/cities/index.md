---
title: Ciudades
description: Endpoints para gestionar ciudades.
---

# Microservicio de Ciudades

Este microservicio maneja toda la lógica relacionada con la gestión de ciudades en el sistema.

---
### Endpoints
* **GET /cities** - _Listar ciudades_
* **POST /cities** - _Crear ciudad_
* **GET /cities/{city_id}** - _Obtener ciudad específica_
* **PUT /cities/{city_id}** - _Actualizar ciudad_
* **DELETE /cities/{city_id}** - _Eliminar ciudad_

---
## Listar Ciudades
```
Nota: para usar este endpoint no se necesita autenticación JWT 
```
`GET`

| Descripción | Lista todas las ciudades disponibles en el sistema. |
|:----------|:---------------------------------------------------|
| Autorización     | Opcional (Accesible por todos los usuarios)        |

### Request (Sin body o parámetros de consulta)

### Response
**Códigos de estado posibles:** 200, 500.

`200 OK`
```json
[
  {
    "name": "Bogotá",
    "country": "Colombia",
    "is_active": 1,
    "id": 2
  },
  {
    "name": "Bello",
    "country": "Colombia",
    "is_active": 1,
    "id": 4
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

## Crear Ciudad
`POST`

| Descripción | Agrega una nueva ciudad al sistema. |
|:----------|:-----------------------------------|
| Autorización     | Requerida (Rol: Administrador)     |

### Request
```json
{
  "name": "Bello",
  "country": "Colombia",
  "is_active": 1
}
```
### Response
**Códigos de estado posibles:** 201, 400, 401, 403, 500.

`201 Created`
```json
{
  "name": "Bello",
  "country": "Colombia",
  "is_active": 1,
  "id": 4
}
```

`400 Bad Request`
```json
{
  "detail": "Los campos name y country son requeridos"
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

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Obtener Ciudad Específica
`GET`

| Descripción | Obtiene la información de una ciudad específica por su ID. |
|:----------|:----------------------------------------------------------|
| Autorización     | Opcional (Accesible por todos los usuarios)               |

### Request (Parámetros de ruta)
- `city_id`: ID único de la ciudad

### Response
**Códigos de estado posibles:** 200, 404, 500.

`200 OK`
```json
{
  "name": "Bogotá",
  "country": "Colombia",
  "is_active": 1,
  "id": 2
}
```

`404 Not Found`
```json
{
  "detail": "Ciudad no encontrada"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Actualizar Ciudad
`PUT`

| Descripción | Modifica la información de una ciudad existente por su ID. |
|:----------|:----------------------------------------------------------|
| Autorización     | Requerida (Rol: Administrador)                            |

### Request
```json
{
  "nombre": "Bogotá D.C.",
  "departamento": "Cundinamarca",
  "pais": "Colombia",
  "codigo_postal": "110011",
  "poblacion": 8200000
}
```

### Response
**Códigos de estado posibles:** 200, 400, 401, 403, 404, 500.

`200 OK`
```json
{
  "name": "Cartagena",
  "country": "Colombia",
  "is_active": 1,
  "id": 3
}
```

`400 Bad Request`
```json
{
  "detail": "Los campos name y country son requeridos"
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
  "detail": "Ciudad no encontrada"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Eliminar Ciudad
`DELETE`

| Descripción | Elimina una ciudad del sistema por su ID. |
|:----------|:------------------------------------------|
| Autorización     | Requerida (Rol: Administrador)            |

### Request (Parámetros de ruta)
- `city_id` (string): ID único de la ciudad

### Response
**Códigos de estado posibles:** 204, 401, 403, 404, 500.

`204 No Content`
```
content-type: application/json 
date: Thu,20 Nov 2025 22:00:15 GMT 
server: uvicorn 
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
  "detail": "Ciudad no encontrada"
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

### Ciudad
| Campo | Tipo | Descripción |
|:------|:-----|:------------|
| id | string | Identificador único de la ciudad |
| nombre | string | Nombre de la ciudad |
| pais | string | País de la ciudad |