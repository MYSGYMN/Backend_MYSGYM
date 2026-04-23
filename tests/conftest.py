import pytest
from app import create_app, db
from datetime import datetime
from pathlib import Path

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

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda el progreso de cada prueba en un archivo."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        log_file = Path(__file__).parent.parent / "test_progress.log"
        
        status = "PASS" if report.passed else "FAIL" if report.failed else "SKIP"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"[{timestamp}] {item.name}: {status}\n"
        
        with open(log_file, "a") as f:
            f.write(log_entry)
