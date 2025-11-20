---
title: Punto de venta
description: Endpoints para manehjar todos los puntos de ventas.
---

# Microservicio de Puntos de Venta

Este microservicio maneja toda la lógica relacionada con la gestión de puntos de venta en el sistema.

---
### Endpoints
* **GET /points-of-sale** - _Listar puntos de venta_
* **POST /points-of-sale** - _Crear punto de venta_
* **GET /points-of-sale/{pos_id}** - _Obtener punto de venta específico_
* **PUT /points-of-sale/{pos_id}** - _Actualizar punto de venta_
* **DELETE /points-of-sale/{pos_id}** - _Eliminar punto de venta_

---
## Listar Puntos de Venta
`GET`

| Descripción | Lista todos los puntos de venta disponibles por cuidad. |
|:----------|:--------------------------------------------------------|
| Autorización     | Requerida (Roles: Administrador)                        |

### Request (Sin body o parámetros de consulta)

### Response
**Códigos de estado posibles:** 200, 401, 403, 500.

`200 OK`
```json
[
  {
    "name": "Catedral",
    "address": "cr543 #67-78",
    "city_id": 4,
    "phone": "5212659522",
    "email": "jajsdj@.com",
    "is_active": 1,
    "id": 2
  }
]
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

## Crear Punto de Venta
`POST`

| Descripción | Agrega un nuevo punto de venta al sistema. |
|:----------|:------------------------------------------|
| Autorización     | Requerida (Rol: Administrador, Gestor)    |

### Request
```json
{
  "name": "Catedral",
  "address": "cr543 #67-78",
  "city_id": 4,
  "phone": "5212659522",
  "email": "jajsdj@.com",
  "is_active": 1
}
```
### Response
**Códigos de estado posibles:** 201, 400, 401, 403, 500.

`201 Created`
```json
{
  "name": "Catedral",
  "address": "cr543 #67-78",
  "city_id": 4,
  "phone": "5212659522",
  "email": "jajsdj@.com",
  "is_active": 1,
  "id": 2
}
```

`400 Bad Request`
```json
{
  "detail": "Los campos name, address y city_id son requeridos"
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

## Obtener Punto de Venta Específico
`GET`

| Descripción | Obtiene la información de un punto de venta específico por su ID. |
|:----------|:----------------------------------------------------------------|
| Autorización     | Requerida (Roles: Administrador, Gestor, Vendedor)             |

### Request (Parámetros de ruta)
- `pos_id` (string): ID único del punto de venta

### Response
**Códigos de estado posibles:** 200, 401, 403, 404, 500.

`200 OK`
```json
{
  "name": "CC Andino",
  "address": "cr 32 #85-45",
  "city_id": 3,
  "phone": "565685",
  "email": "ccandino@gmail.com",
  "is_active": 1,
  "id": 1
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
  "detail": "Punto de venta no encontrado"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Actualizar Punto de Venta
`PUT`

| Descripción | Modifica la información de un punto de venta existente por su ID. |
|:----------|:----------------------------------------------------------------|
| Autorización     | Requerida (Rol: Administrador, Gestor)                         |

### Request
```json
{
  "name": "CC Fabricato",
  "address": "cr 32 #85-45",
  "city_id": 3,
  "phone": "565685",
  "email": "ccandino@gmail.com",
  "is_active": 1
}
```

### Response
**Códigos de estado posibles:** 200, 400, 401, 403, 404, 500.

`200 OK`
```json
{
  "name": "CC Fabricato",
  "address": "cr 32 #85-45",
  "city_id": 3,
  "phone": "565685",
  "email": "ccandino@gmail.com",
  "is_active": 1,
  "id": 1
}
```

`400 Bad Request`
```json
{
  "detail": "Los campos name, address y city_id son requeridos"
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
  "detail": "Punto de venta no encontrado"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Eliminar Punto de Venta
`DELETE`

| Descripción | Elimina un punto de venta del sistema por su ID. |
|:----------|:------------------------------------------------|
| Autorización     | Requerida (Rol: Administrador)                 |

### Request (Parámetros de ruta)
- `pos_id` (string): ID único del punto de venta

### Response
**Códigos de estado posibles:** 204, 401, 403, 404, 500.

`204 No Content`
```
content-type: application/json 
date: Thu,20 Nov 2025 22:11:30 GMT 
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
  "detail": "Punto de venta no encontrado"
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

### Punto de Venta
| Campo     | Tipo | Descripción                            |
|:----------|:-----|:---------------------------------------|
| id        | string | Identificador único del punto de venta |
| nombre    | string | Nombre del punto de venta              |
| direccion | string | Dirección física completa              |
| ciudad_id | string | ID de la ciudad donde se encuentra     |
| telefono  | string | Número de teléfono de contacto         |
| email     | string | Email de contacto                      |


### Notas de Autorización
- **Administrador**: Acceso completo a todos los endpoints
- **Gestor**: Puede crear, listar, ver y actualizar puntos de venta
- **Vendedor**: Solo puede listar y ver puntos de venta activos