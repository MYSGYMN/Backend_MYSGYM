# API Endpoints - Backend MYSGYM

## Base URL

```
http://localhost:5000/api
```

## Health Check

### GET /health

Verifica que el servidor está operativo.

**Respuesta:**
```json
{
  "status": "ok",
  "message": "Backend MYSGYM está operativo"
}
```

---

## Usuarios

### GET /api/usuarios

Listar todos los usuarios.

**Respuesta (200):**
```json
[
  {
    "id_usuario": 1,
    "nombre": "Ana Lopez",
    "email": "ana.lopez@example.com",
    "telefono": "600111222",
    "fecha_registro": "2026-01-10",
    "estado": "activo"
  }
]
```

### GET /api/usuarios/{id}

Obtener un usuario específico.

**Parámetros:**
- `id` (path): ID del usuario

**Respuesta (200):**
```json
{
  "id_usuario": 1,
  "nombre": "Ana Lopez",
  "email": "ana.lopez@example.com",
  "telefono": "600111222",
  "fecha_registro": "2026-01-10",
  "estado": "activo"
}
```

### POST /api/usuarios

Crear un nuevo usuario.

**Body (JSON):**
```json
{
  "nombre": "Juan Perez",
  "email": "juan.perez@example.com",
  "password_hash": "hash_juan_001",
  "telefono": "600999888",
  "fecha_registro": "2026-04-20",
  "estado": "activo"
}
```

**Respuesta (201):**
```json
{
  "id_usuario": 6,
  "nombre": "Juan Perez",
  "email": "juan.perez@example.com",
  "telefono": "600999888",
  "fecha_registro": "2026-04-20",
  "estado": "activo"
}
```

### PUT /api/usuarios/{id}

Actualizar un usuario.

**Body (JSON):**
```json
{
  "nombre": "Juan Perez Updated",
  "estado": "inactivo"
}
```

**Respuesta (200):** Usuario actualizado

### DELETE /api/usuarios/{id}

Eliminar un usuario.

**Respuesta (200):**
```json
{
  "message": "Usuario eliminado"
}
```

---

## Empleados

### GET /api/empleados

Listar todos los empleados.

### GET /api/empleados/{id}

Obtener un empleado específico.

### POST /api/empleados

Crear un nuevo empleado.

**Body (JSON):**
```json
{
  "nombre": "Fernando Monitor",
  "email": "fernando.monitor@example.com",
  "rol": "monitor",
  "fecha_contratacion": "2026-03-01"
}
```

### PUT /api/empleados/{id}

Actualizar un empleado.

### DELETE /api/empleados/{id}

Eliminar un empleado.

---

## Actividades

### GET /api/actividades

Listar todas las actividades con detalles de monitor, sala y horario.

### GET /api/actividades/{id}

Obtener una actividad específica.

### POST /api/actividades

Crear una nueva actividad.

**Body (JSON):**
```json
{
  "nombre": "Pilates Avanzado",
  "descripcion": "Clase de pilates para nivel avanzado",
  "monitor_id": 1,
  "sala_id": 3,
  "horario_id": 2,
  "aforo_maximo": 15
}
```

### PUT /api/actividades/{id}

Actualizar una actividad.

### DELETE /api/actividades/{id}

Eliminar una actividad.

---

## Códigos de Respuesta HTTP

- **200 OK**: Solicitud exitosa.
- **201 Created**: Recurso creado exitosamente.
- **400 Bad Request**: Parámetros inválidos o incompletos.
- **404 Not Found**: Recurso no encontrado.
- **409 Conflict**: Violación de restricción única (ej. email duplicado).
- **500 Internal Server Error**: Error del servidor.

---

## Testing Local

Usa herramientas como `curl`, Postman o similar:

### Ejemplo con curl

```bash
# Listar usuarios
curl -X GET http://localhost:5000/api/usuarios

# Crear usuario
curl -X POST http://localhost:5000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test User",
    "email": "test@example.com",
    "telefono": "123456789",
    "estado": "activo"
  }'

# Obtener usuario
curl -X GET http://localhost:5000/api/usuarios/1

# Actualizar usuario
curl -X PUT http://localhost:5000/api/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Updated Name"
  }'

# Eliminar usuario
curl -X DELETE http://localhost:5000/api/usuarios/1
```

---

## Próximas Adiciones

- Endpoints para Salas, Horarios, Reservas, Pagos, Material, Incidencias.
- Autenticación y autorización.
- Validación avanzada con Pydantic.
- Rate limiting.
- Documentación interactiva con Swagger/OpenAPI.
