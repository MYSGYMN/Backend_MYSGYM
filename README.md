# Backend_MYSGYM

Repositorio base para la construccion del backend de MYSGYM, con base de datos MySQL 8 en Docker y flujo de trabajo orientado a VS Code + SQLTools.

## 1. Objetivo del repositorio

Este repositorio centraliza:

- Definicion funcional en historias y EPICs.
- Modelado de dominio (literario y ER).
- Entorno local reproducible de MySQL con Docker Compose.
- Flujo de desarrollo SQL sin MySQL Workbench.

## 2. Estructura actual

### 2.1 Documentación y configuración

- `EPIC_1.md` - Historias del epic 1.
- `EPIC_2.md` - Historias del epic 2.
- `EPIC_3.md` - Historias del epic 3.
- `EPIC_4.md` - Historias del epic 4.
- `modelo_literario.md` - Modelo de negocio y entidades.
- `Instalar_MySQL.md` - Guía de instalación y operación MySQL.
- `API.md` - Documentación de endpoints REST.
- `README.md` - Este archivo.

### 2.2 Infraestructura

- `docker-compose.yml` - Orquestación de MySQL con Compose.
- `.env` - Variables locales del entorno (no versionar).
- `.env.example` - Plantilla para variables.
- `.gitignore` - Exclusiones de Git.
- `Makefile` - Automatización de comandos diarios.

### 2.3 Backend Flask

- `run.py` - Entry point de la aplicación.
- `config.py` - Configuración por entornos (dev/prod/test).
- `requirements.txt` - Dependencias Python.
- `app/` - Paquete principal de la aplicación.
  - `__init__.py` - Factory pattern y configuración.
  - `models.py` - Modelos SQLAlchemy (10 tablas).
  - `routes/` - Blueprints de rutas.
    - `usuarios.py` - CRUD usuarios.
    - `empleados.py` - CRUD empleados.
    - `actividades.py` - CRUD actividades.

### 2.4 Base de datos

- `Modelo.sql` - Script DDL de esquema.
- `seeds/seed.sql` - Datos de prueba reproducibles.
- `mysql-gym.inspect.json` - Snapshot de la configuración del contenedor.

### 2.5 VS Code

- `.vscode/settings.json` - Configuración de SQLTools del workspace.

## 3. Prerrequisitos

### 3.1 Sistema

- Linux (Mint/Ubuntu recomendado).
- Docker Engine.
- Docker Compose plugin.
- GNU Make.
- Python 3.9+.

### 3.2 VS Code

- VS Code instalado.
- Extensiones recomendadas:
  - SQLTools (`mtxr.sqltools`)
  - SQLTools MySQL Driver (`mtxr.sqltools-driver-mysql`)
  - Python extension (`ms-python.python`)

Instalación base en Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin make python3 python3-venv
sudo systemctl enable --now docker
```

Opcional para usar Docker sin sudo:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 4. Configuracion inicial

### 4.1 Crear archivo de entorno

Si no existe `.env`, crealo desde la plantilla:

```bash
cp .env.example .env
```

Ejemplo usado en este proyecto:

```env
MYSQL_ROOT_PASSWORD=RootPass123!
MYSQL_DATABASE=gimnasio
MYSQL_APP_USER=app_user
MYSQL_APP_PASSWORD=segura123
MYSQL_ADMIN_USER=admin
MYSQL_ADMIN_PASSWORD=adminpass
```

### 4.2 Levantar base de datos

```bash
make up
make ps
```

### 4.3 Validar conectividad

```bash
set -a
source .env
set +a
docker exec mysql-gym mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1 as ok;"
```

Respuesta esperada:

- Columna `ok` con valor `1`.

## 5. SQLTools en VS Code

El workspace ya trae conexiones configuradas en `.vscode/settings.json`:

- `MySQL Docker Local (app_user)`
- `MySQL Docker Local (root)`

Conexion por defecto para desarrollo:

- `sqltools.autoConnectTo = "MySQL Docker Local (app_user)"`

Recomendacion de uso:

- Usar `app_user` para consultas y operaciones CRUD normales.
- Usar `root` solo para tareas administrativas (usuarios, grants, mantenimiento).

## 6. Comandos operativos (Makefile)

Mostrar ayuda:

```bash
make help
```

Comandos disponibles:

- `make up`: levanta MySQL con Compose.
- `make down`: detiene el stack.
- `make restart`: reinicia.
- `make ps`: estado de servicios.
- `make logs`: logs en vivo del servicio mysql.
- `make mysql-root`: consola mysql como root.
- `make mysql-app`: consola mysql como app_user.
- `make backup`: crea dump SQL timestamp en `backups/`.
- `make seed`: carga datos de prueba desde `seeds/seed.sql`.

### 6.1 Carga de datos de prueba (seed)

Para poblar la base con datos de ejemplo:

```bash
make seed
```

El comando ejecuta el archivo `seeds/seed.sql` sobre la base configurada en `.env`.

## 7. Seguridad y versionado

`.gitignore` excluye secretos y artefactos locales:

- `.env`
- otros `.env.*` (excepto `.env.example`)
- `backups/`
- `*.session.sql`
- `mysql-gym.inspect.json`

Buenas practicas:

- No subir credenciales reales al repositorio.
- Rotar passwords antes de despliegues compartidos.
- Usar usuarios con privilegios minimos para desarrollo diario.

## 8. Flujo recomendado de trabajo

1. `make up`
2. Abrir SQLTools y confirmar conexion activa `app_user`.
3. Ejecutar scripts SQL de desarrollo.
4. Cargar datos de prueba con `make seed` cuando necesites un entorno reproducible.
5. Para tareas admin, cambiar temporalmente a `root`.
6. Al finalizar, crear backup con `make backup` si hiciste cambios sensibles.
7. `make down` si necesitas liberar recursos.

## 9. Solucion de problemas

### 9.1 SQLTools no aparece

- Verificar extensiones instaladas.
- Abrir comando `View: Open View...` y buscar SQLTools.
- Ejecutar `Developer: Reload Window`.
- Verificar que estas en el mismo contexto (local/WSL/SSH/Container) donde esta instalada la extension.

### 9.2 Puerto 3306 ocupado

```bash
sudo lsof -i :3306
```

Detener servicio que use el puerto o cambiar mapeo en `docker-compose.yml`.

### 9.3 Contenedor no arranca

```bash
docker compose logs -f mysql
docker compose ps
```

Verificar:

- credenciales en `.env`
- permisos de Docker
- estado del volumen `mysql_data`

## 10. Referencias del proyecto

- Guía de instalación MySQL: [Instalar_MySQL.md](Instalar_MySQL.md)
- Documentación de API REST: [API.md](API.md)
- Configuración de servicios: [docker-compose.yml](docker-compose.yml)
- Automatización de tareas: [Makefile](Makefile)

---

## 11. Backend Flask

### 11.1 ¿Qué es?

Backend REST basado en Flask con SQLAlchemy ORM para acceso a MySQL. Proporciona CRUD completo para usuarios, empleados y actividades, con relaciones entre entidades.

**Stack:**
- Flask 3.0.0
- SQLAlchemy 2.0 ORM
- PyMySQL para conexión
- Flask-CORS para corsé
- Python-Dotenv para configuración

### 11.2 Setup inicial

#### 11.2.1 Crear entorno virtual e instalar dependencias

```bash
make venv
make install
```

O manualmente:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 11.2.2 Validar variables de entorno

El archivo `.env` debe tener:

```env
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=mysql+pymysql://app_user:segura123@127.0.0.1:3306/gimnasio
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO
```

#### 11.2.3 Asegurar que MySQL está en marcha

```bash
make up
docker compose ps
```

### 11.3 Estructura de carpetas

```
Backend_MYSGYM/
├── app/                          # Aplicación Flask
│   ├── __init__.py              # Factory pattern + setup
│   ├── models.py                # Modelos SQLAlchemy (10 entidades)
│   └── routes/
│       ├── __init__.py          # Imports de blueprints
│       ├── usuarios.py          # GET, POST, PUT, DELETE /api/usuarios
│       ├── empleados.py         # GET, POST, PUT, DELETE /api/empleados
│       └── actividades.py       # GET, POST, PUT, DELETE /api/actividades
├── config.py                     # Configuraciones (dev/prod/test)
├── run.py                        # Entry point (main)
├── requirements.txt              # Dependencias pip
├── .env                          # Variables secretas (local, no versionar)
├── .env.example                  # Template de .env
└── Makefile                      # Automatización
```

### 11.4 Iniciar servidor

```bash
make flask-run
```

Ó con Python directo:

```bash
source .venv/bin/activate
python run.py
```

Salida esperada:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 11.5 Verificar que está activo

```bash
curl http://localhost:5000/health
```

Respuesta:

```json
{
  "status": "ok",
  "message": "Backend MYSGYM está operativo"
}
```

### 11.6 Comandos operativos

| Comando | Descripción |
|---------|-------------|
| `make venv` | Crear entorno virtual |
| `make install` | Instalar dependencias |
| `make install-dev` | + herramientas desarrollo (pytest, black) |
| `make flask-run` | Levanta servidor Flask |
| `make flask-shell` | Abre shell interactivo Flask |

### 11.7 Modelos y Relaciones

La app expone 10 modelos SQLAlchemy mapeados a las tablas:

1. **Usuario** - usuarios (id_usuario PK)
2. **Empleado** - empleados (id_empleado PK)
3. **Sala** - salas (id_sala PK)
4. **Horario** - horarios (id_horario PK)
5. **Actividad** - actividades (id_actividad PK, FK a empleados, salas, horarios)
6. **Reserva** - reservas (id_reserva PK, FK a usuarios, actividades)
7. **Pago** - pagos (id_pago PK, FK a usuarios)
8. **Material** - material (id_material PK, FK a salas)
9. **Incidencia** - incidencias (id_incidencia PK, FK a empleados, material)

Cada modelo tiene método `.to_dict()` para serializar a JSON.

### 11.8 Endpoints disponibles

#### 11.8.1 Health Check

```bash
GET /health
```

#### 11.8.2 Usuarios

```bash
GET    /api/usuarios              # Listar todos
GET    /api/usuarios/{id}         # Obtener por ID
POST   /api/usuarios              # Crear nuevo
PUT    /api/usuarios/{id}         # Actualizar
DELETE /api/usuarios/{id}         # Eliminar
```

#### 11.8.3 Empleados

```bash
GET    /api/empleados             # Listar todos
GET    /api/empleados/{id}        # Obtener por ID
POST   /api/empleados             # Crear nuevo
PUT    /api/empleados/{id}        # Actualizar
DELETE /api/empleados/{id}        # Eliminar
```

#### 11.8.4 Actividades

```bash
GET    /api/actividades           # Listar todos
GET    /api/actividades/{id}      # Obtener por ID
POST   /api/actividades           # Crear nuevo
PUT    /api/actividades/{id}      # Actualizar
DELETE /api/actividades/{id}      # Eliminar
```

### 11.9 Ejemplos de uso

#### 11.9.1 Listar usuarios

```bash
curl http://localhost:5000/api/usuarios
```

Respuesta:

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

#### 11.9.2 Crear usuario

```bash
curl -X POST http://localhost:5000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos Nuevo",
    "email": "carlos.nuevo@example.com",
    "password_hash": "hashed_password",
    "telefono": "600123456",
    "fecha_registro": "2026-04-20",
    "estado": "activo"
  }'
```

Respuesta (201 Created):

```json
{
  "id_usuario": 6,
  "nombre": "Carlos Nuevo",
  "email": "carlos.nuevo@example.com",
  "telefono": "600123456",
  "fecha_registro": "2026-04-20",
  "estado": "activo"
}
```

#### 11.9.3 Actualizar usuario

```bash
curl -X PUT http://localhost:5000/api/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "inactivo"
  }'
```

#### 11.9.4 Eliminar usuario

```bash
curl -X DELETE http://localhost:5000/api/usuarios/1
```

Respuesta:

```json
{
  "message": "Usuario eliminado"
}
```

### 11.10 Validación y errores

Códigos HTTP:

- **200 OK**: Exitoso.
- **201 Created**: Recurso creado.
- **400 Bad Request**: Falta campo requerido o formato inválido.
- **404 Not Found**: Recurso no existe.
- **409 Conflict**: Violación de restricción única (ej. email duplicado).
- **500 Internal Server Error**: Error del servidor.

Ejemplo de error 400:

```json
{
  "error": "Faltan campos requeridos"
}
```

### 11.11 Testing

Usar Postman, curl o cliente HTTP favorito.

Conjunto mínimo de pruebas:

```bash
# Health
curl http://localhost:5000/health

# Usuarios
curl http://localhost:5000/api/usuarios
curl http://localhost:5000/api/usuarios/1

# Empleados
curl http://localhost:5000/api/empleados

# Actividades
curl http://localhost:5000/api/actividades
```

### 11.12 Entorno de desarrollo

Para desarrollo avanzado:

```bash
make install-dev
```

Agrega:
- pytest: testing
- pytest-cov: cobertura
- black: formateador
- flake8: linter

### 11.13 Shell interactivo Flask

```bash
make flask-shell
```

Dentro de la shell:

```python
from app.models import Usuario
usuarios = Usuario.query.all()
print([u.to_dict() for u in usuarios])
```

---

## 12. Flujo de trabajo integrado (MySQL + Flask)

Flujo típico de desarrollo:

### Paso 1: Base de datos

```bash
make up                # Levanta MySQL
make seed              # Carga datos de prueba
```

### Paso 2: Desarrollo backend

```bash
make install           # Instala dependencias Flask
make flask-run         # Inicia servidor
```

### Paso 3: Testing API

```bash
# En otra terminal
curl http://localhost:5000/api/usuarios
curl http://localhost:5000/api/empleados
```

### Paso 4: Desarrollo SQL

Abre VS Code → SQLTools → MySQL Docker Local (app_user) → Escribe queries

### Paso 5: Limpieza

```bash
make down              # Detiene MySQL
```

---

## 13. Próximas adiciones

- Endpoints para Salas, Reservas, Pagos, Material, Incidencias.
- Autenticación JWT.
- Validación avanzada (Pydantic).
- Rate limiting.
- Swagger/OpenAPI automática.
- Tests unitarios (pytest).
- Dockerización de la app Flask.

---

## 14. Contacto y referencias

Para detalles de endpoints, ver [API.md](API.md).

Para instalación MySQL, ver [Instalar_MySQL.md](Instalar_MySQL.md).
