import pytest
from app import create_app, db
from sqlalchemy import text
from datetime import datetime, timezone

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

def test_database_setup(app):
    """Prueba que la base de datos se crea correctamente con las 9 tablas."""
    with app.app_context():
        print("\nLimpiando base de datos (desactivando FK checks temporalmente)...")
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        db.drop_all()
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        
        print("Creando estrictamente las 9 tablas...")
        db.create_all()
        db.session.commit()
        
        tablas_actuales = list(db.metadata.tables.keys())
        print(f"Tablas actuales en la DB: {tablas_actuales}")
        
        # Lista de las 9 tablas esperadas (en plural como se define en los modelos)
        tablas_esperadas = [
            'usuarios', 'empleados', 'salas', 'horarios', 
            'actividades', 'reservas', 'pagos', 'materiales', 'incidencias'
        ]
        
        for tabla in tablas_esperadas:
            assert tabla in tablas_actuales, f"Falta la tabla {tabla}"
        
        assert len(tablas_actuales) == 9, f"Se esperaban 9 tablas, se encontraron {len(tablas_actuales)}"
        print("¡Base de datos lista con las 9 tablas solicitadas!")
