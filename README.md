# MYSGYM — Backend API

Sistema de gestión integral para gimnasios desarrollado con **Python Flask**, **SQLAlchemy** y **MySQL**.

## 🚀 Estructura del Proyecto

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

## 🛠️ Tecnologías utilizadas

*   **Framework:** Flask
*   **Base de Datos:** MySQL 8.0 (Dockerizado)
*   **ORM:** SQLAlchemy + Flask-Migrate
*   **Seguridad:** Flask-JWT-Extended (Roles: Cliente, Monitor, Admin)

## 📋 Requisitos Previos

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

---

*Desarrollado para el proyecto final de MYSGYM.*
