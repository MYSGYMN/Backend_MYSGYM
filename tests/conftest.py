import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Configuración principal de la aplicación para pruebas."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        # Usamos SQLite en memoria para no borrar tu base de datos MySQL real
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret-key"
    })

    # Crear las tablas antes de cada test
    with app.app_context():
        db.create_all()
        yield app  # Aquí es donde se ejecutan los tests
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Un cliente de pruebas para hacer peticiones HTTP (GET, POST, etc.)"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Un corredor de comandos para la CLI de Flask"""
    return app.test_cli_runner()
