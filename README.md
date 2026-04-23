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

## Requisitos Previos

1.  Tener instalado **Docker** y **Docker Compose**.
2.  Python 3.12+ (para ejecución local).

## ⚡ Instalación Rápida

1.  **Levantar Base de Datos**:
    ```bash
    docker-compose up -d
    ```

2.  **Configurar Entorno**:
    Crea un archivo `.env` basado en `.env.example`.

3.  **Ejecutar Servidor**:
    ```bash
    source .venv/bin/activate
    python run.py
    ```

El servidor estará disponible en `http://localhost:8000`.

## Tests
## Scripts de Utilidad

El proyecto incluye scripts auxiliares en el folder `scripts/`:

- **[seed_data.py](scripts/seed_data.py)** — Carga datos de prueba iniciales en la BD (salas, empleados, horarios, actividades). Útil para desarrollo local:
    ```bash
    .venv/bin/python scripts/seed_data.py
    ```

## Tests

El proyecto incluye pruebas automatizadas con `pytest` para validar el estado de la base de datos y el flujo de integración.

### Qué cubren

*   La prueba principal de integración en [tests/test_db.py](tests/test_db.py) crea la base de datos desde los modelos y verifica que existan las 9 tablas esperadas.
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
    pylint app/ --disable=missing-docstring  #para evitar analisis de docstring
```

### Generación de reportes

El progreso de cada prueba se guarda automáticamente en `test_progress.log` con fecha y hora (hook configurado en [tests/conftest.py](tests/conftest.py)). 

Los reportes HTML se generan en:
- `reporte.html` — Detalles de ejecución de pruebas
- `htmlcov/` — Cobertura de código por línea y módulo

Pylint evalúa la calidad del código en `pylint_report.txt` con puntuación y recomendaciones.

---

*Desarrollado para el proyecto final de MYSGYM.*
