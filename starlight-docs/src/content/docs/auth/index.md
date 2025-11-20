---
title: Autenticación
description: Endpoints para registro, inicio de sesión y validación de tokens.
---

# Microservicio de Autenticación

Este microservicio maneja toda la lógica relacionada con la autenticación y gestión de usuarios en el sistema.

---
### Endpoints
* **POST /register** - _Registrar usuario_
* **POST /login** - _Iniciar sesión_
* **GET /me** - _Obtener información del usuario actual_
* **GET /users** - _Listar todos los usuarios_
* **DELETE /users/{user_id}** - _Eliminar usuario_

---
## Registrar Usuario
`POST`

| Descripción | Registra un nuevo usuario en el sistema. |
|:----------|:----------------------------------------|
| Autorización     | No requerida                            |

### Request
```json
{
  "name": "Fernanada Gomez",
  "email": "fer@gmail.com",
  "role": "admin",
  "password": "admin789"
}
```
### Response
**Códigos de estado posibles:** 201, 400, 409, 500.

`201 Created`
```json
{
  "name": "Fernanada Gomez",
  "email": "fer@gmail.com",
  "role": "admin",
  "id": 5
}
```

`400 Bad Request`
```json
{
  "detail": "Todos los campos son requeridos: name, email, password, role"
}
```

`409 Conflict`
```json
{
  "detail": "El email ya está registrado"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Iniciar Sesión
`POST`

| Descripción | Autentica un usuario y devuelve un token de acceso. |
|:----------|:---------------------------------------------------|
| Autorización     | No requerida                                       |

### Request
```json
{
  "email": "fer@gmail.com",
  "password": "admin789"
}
```
### Response
**Códigos de estado posibles:** 200, 400, 401, 500.

`200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmZXJAZ21haWwuY29tIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzYzNjczNzA5fQ.ojAxcl_ismEvDCDPYjHRZ7-SYOXrt-g9X-_DtJr0sgE",
  "token_type": "bearer",
  "user": {
    "name": "Fernanada Gomez",
    "email": "fer@gmail.com",
    "role": "admin",
    "id": 5
  }
}
```

`400 Bad Request`
```json
{
  "detail": "Debe enviar 'email' y 'password'"
}
```

`401 Unauthorized`
```json
{
  "detail": "Credenciales incorrectas"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Obtener Información del Usuario Actual
`GET`

| Descripción | Obtiene la información del usuario autenticado. |
|:----------|:-----------------------------------------------|
| Autorización     | Requerida (Todos los usuarios autenticados)    |

### Request (Headers)
- `Authorization: Bearer {token}`

### Response
**Códigos de estado posibles:** 200, 401, 404, 500.

`200 OK`
```json
{
  "name": "Fernanada Gomez",
  "email": "fer@gmail.com",
  "role": "admin",
  "id": 5
}
```

`401 Unauthorized`
```json
{
  "detail": "Token inválido o expirado"
}
```

`404 Not Found`
```json
{
  "detail": "Usuario no encontrado"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Internal Server Error"
}
```

---

## Listar Todos los Usuarios
`GET`

| Descripción | Lista todos los usuarios del sistema (solo administradores). |
|:----------|:-----------------------------------------------------------|
| Autorización     | Requerida (Rol: Administrador)                             |

### Request (Headers)
- `Authorization: Bearer {token}`

### Response
**Códigos de estado posibles:** 200, 401, 403, 500.

`200 OK`
```json
[
  {
    "name": "Administrador",
    "email": "admin@eventos.com",
    "role": "admin",
    "id": 1
  },
  {
    "name": "luisa",
    "email": "lu@gmail.com",
    "role": "admin",
    "id": 2
  },
  {
    "name": "",
    "email": "user@example.com",
    "role": "user",
    "id": 3
  },
  {
    "name": "Sara Romero",
    "email": "sara@gmail.com",
    "role": "admin",
    "id": 4
  },
  {
    "name": "Fernanada Gomez",
    "email": "fer@gmail.com",
    "role": "admin",
    "id": 5
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

## Eliminar Usuario
`DELETE`

| Descripción | Elimina un usuario del sistema por su ID. |
|:----------|:-----------------------------------------|
| Autorización     | Requerida (Rol: Administrador)           |

### Request (Parámetros de ruta)
- `user_id` (string): ID único del usuario

### Request (Headers)
- `Authorization: Bearer {token}`

### Response
**Códigos de estado posibles:** 200, 400, 401, 403, 404, 500.

`200 OK`
```json
{
  "message": "Usuario 'cliente@ejemplo.com' eliminado correctamente"
}
```

`400 Bad Request`
```json
{
  "detail": "No puedes eliminar tu propio usuario"
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
  "detail": "Acceso denegado. Se requiere el rol de Administrador."
}
```

`404 Not Found`
```json
{
  "detail": "Usuario no encontrado"
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

### Usuario
| Campo | Tipo | Descripción |
|:------|:-----|:------------|
| id | string | Identificador único del usuario |
| email | string | Email del usuario (único) |
| password | string | Contraseña hasheada |
| nombre | string | Nombre completo del usuario |
| rol | string | Rol del usuario (cliente, gestor, administrador) |

### Token de Acceso
| Campo | Tipo | Descripción |
|:------|:-----|:------------|
| access_token | string | Token JWT para autenticación |
| token_type | string | Tipo de token (siempre "bearer") |
| expires_in | number | Tiempo de expiración en segundos |

### Roles del Sistema
- **cliente**: Usuario final que realiza compras a eventos
- **administrador**: Acceso completo al sistema

### Notas de Seguridad
- Las contraseñas se almacenan hasheadas con bcrypt
- Los tokens JWT expiran después de 30 minutos
- Solo los administradores pueden listar y eliminar usuarios
- Los usuarios solo pueden acceder a su propia información mediante `/me`