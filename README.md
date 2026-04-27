# MYSGYM — Backend API

Sistema de gestión integral para gimnasios desarrollado con **Python Flask**, **SQLAlchemy** y **MySQL**.

## Estructura del Proyecto

El proyecto sigue un patrón modular utilizando Blueprints para facilitar la escalabilidad:

```text
Backend_MYSGYM/
├── app/                    # Lógica principal de la aplicación
│   ├── routes/             # Blueprints (Auth, Gym, Usuarios, etc.)
│   ├── models.py           # Modelos de SQLAlchemy
│   ├── utils.py            # Decoradores y utilidades de seguridad
│   └── __init__.py         # Factory de la aplicación
├── database/               # Volumen de persistencia de MySQL (Docker)
├── docs/                   # Documentación detallada (Épicas, Diagramas, E/R)
├── migrations/             # Migraciones de la base de datos
├── scripts/                # Scripts de utilidad (Carga de datos/Seed)
├── tests/                  # Pruebas unitarias y de integración
├── database_schema.sql     # Script SQL completo de la DB
├── docker-compose.yml      # Orquestación de contenedores
├── run.py                  # Punto de entrada de la aplicación
└── requirements.txt        # Dependencias del proyecto
```

## Tecnologías utilizadas

*   **Framework:** Flask
*   **Base de Datos:** MySQL 8.0 (Dockerizado)
*   **ORM:** SQLAlchemy + Flask-Migrate
*   **Seguridad:** Flask-JWT-Extended (Roles: Cliente, Monitor, Admin)

## Requisitos previos

Antes de instalar el proyecto, asegúrate de tener:

- **Python 3.12+**
- **Docker**
- **Docker Compose**
- **Git**

## Instalación desde cero

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPO
cd Backend_MYSGYM
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear el archivo `.env`

El archivo `.env` no se sube al repositorio porque contiene configuración local. Crea un archivo llamado `.env` en la raíz del proyecto con este contenido:

```env
DB_HOST=localhost
DB_PORT=3307
DB_USER=root
DB_PASSWORD=root_password
DB_NAME=gimnasio
JWT_SECRET_KEY=super-secret-key
```

Si usas otros datos de MySQL, modifica esos valores para que coincidan con tu entorno.

### 5. Levantar MySQL con Docker

```bash
docker-compose up -d
```

El contenedor de MySQL se expone en el puerto `3307` del ordenador. En una instalación limpia, Docker ejecuta automáticamente [database_schema.sql](database_schema.sql) para crear la base de datos `gimnasio` y sus tablas.

Si ya existía una carpeta `database/` de una ejecución anterior, Docker puede reutilizar datos antiguos y no volver a ejecutar el script SQL. Para reiniciar la base de datos desde cero:

```bash
docker-compose down
rm -rf database
docker-compose up -d
```

### 6. Ejecutar el backend

```bash
python run.py
```

El servidor estará disponible en `http://localhost:8000`.

Puedes comprobar que responde con:

```bash
curl http://localhost:8000
```

## Scripts de Utilidad

El proyecto incluye scripts auxiliares en el folder `scripts/`:

- **[seed_data.py](scripts/seed_data.py)** — Carga datos de prueba iniciales en la BD (salas, empleados, horarios, actividades). Útil para desarrollo local:
    ```bash
    .venv/bin/python scripts/seed_data.py
    ```

## Tests

El proyecto incluye pruebas automatizadas con `pytest` para validar el estado de la base de datos y el flujo de integración.

### Qué cubren

*   La prueba principal de integración en [tests/test_db.py](tests/test_db.py) usa una base SQLite temporal, crea las tablas desde los modelos y verifica tablas, columnas y claves foráneas importantes.
*   La configuración de [pytest.ini](pytest.ini) ignora `database/` durante la recolección, evitando errores por archivos internos de MySQL.

### Cómo ejecutarlos

```bash
.venv/bin/python -m pytest -q
```

Para generar un reporte HTML detallado:

```bash
.venv/bin/python -m pytest -q --html=reporte.html
```

Para medir cobertura de código:

```bash
.venv/bin/python -m pytest -q --cov=app --cov-report=html --cov-report=term
```

Para análisis estático de código:

```bash
.venv/bin/python -m pylint app/ --output-format=parseable
.venv/bin/python -m pylint app/ --disable=missing-docstring
```

### Generación de reportes

El progreso de cada prueba se guarda automáticamente en `test_progress.log` con fecha y hora (hook configurado en [tests/conftest.py](tests/conftest.py)). 

Los reportes HTML se generan en:
- `reporte.html` — Detalles de ejecución de pruebas
- `htmlcov/` — Cobertura de código por línea y módulo

Pylint evalúa la calidad del código en `pylint_report.txt` con puntuación y recomendaciones.

---

*Desarrollado para el proyecto final de MYSGYM.*
