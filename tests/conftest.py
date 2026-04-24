import pytest
from app import create_app, db
from datetime import datetime
from pathlib import Path

@pytest.fixture
def app(tmp_path):
    """Configuración principal de la aplicación para pruebas."""
    db_file = tmp_path / "test_testing.db"

    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_file}"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        JWT_SECRET_KEY = "clave-super-secreta-para-tests-de-gimnasio-32bytes"

    app = create_app(TestConfig)
    database_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    if not database_uri.startswith("sqlite:///"):
        raise RuntimeError(f"Los tests no pueden ejecutarse contra esta BD: {database_uri}")

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
