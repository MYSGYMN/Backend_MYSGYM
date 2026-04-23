"""
Tests de integración para validar la estructura de la base de datos.

Este módulo verifica que:
1. La aplicación Flask se crea correctamente
2. Los modelos de SQLAlchemy se traducen en las tablas esperadas
3. Las 9 tablas del sistema existen en MySQL
"""

import pytest
from sqlalchemy import inspect, text

from app import create_app, db


# ============================================================================
# FIXTURES - Configuración inicial y cleanup para las pruebas
# ============================================================================

@pytest.fixture(scope="module")
def app_context():
    """
    Crea el contexto de la aplicación Flask una sola vez para todo el módulo.
    
    Scope: module → Se ejecuta una vez antes de todas las pruebas en este archivo.
    
    Yield: Mantiene el contexto vivo durante todas las pruebas, permitiendo
           acceder a la app y la BD a través de 'db' global.
    """
    app = create_app()
    with app.app_context():
        yield


@pytest.fixture(scope="module")
def reset_database(app_context):
    """
    Limpia la base de datos completamente y la recrea desde los modelos.
    
    Scope: module → Se ejecuta una sola vez, antes de la primera prueba.
    
    Pasos:
    1. Desactiva chequeos de clave foránea (permite borrar sin restricciones)
    2. Elimina todas las tablas existentes (drop_all)
    3. Reactiva los chequeos de clave foránea
    4. Crea todas las tablas definidas en los modelos (create_all)
    5. Confirma la transacción (commit)
    6. Yield: Las pruebas se ejecutan con una BD limpia
    
    Parámetro:
        app_context (fixture): Requiere el contexto de Flask para operar
    """
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    db.drop_all()
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    db.create_all()
    db.session.commit()
    yield


# ============================================================================
# TESTS - Pruebas de integración
# ============================================================================

@pytest.mark.integration
def test_creates_expected_tables(reset_database):
    """
    Verifica que la base de datos contiene las 9 tablas esperadas del sistema.
    
    Marcador: @pytest.mark.integration
    - Indica que esta es una prueba de integración (toca BD real)
    - Permite filtrar con: pytest -m integration
    
    Parámetro:
        reset_database (fixture): Asegura que la BD está limpia y con todas
                                  las tablas creadas antes de la prueba
    
    Tabla esperadas del sistema MYSGYM:
        1. usuarios    - Clientes del gimnasio
        2. empleados   - Staff (monitores, admin)
        3. salas       - Espacios del gimnasio
        4. horarios    - Franjas horarias disponibles
        5. actividades - Clases/ejercicios
        6. reservas    - Registro de inscripciones a actividades
        7. pagos       - Transacciones de clientes
        8. materiales  - Equipamiento de las salas
        9. incidencias - Reportes de problemas/mantenimiento
    
    Aserciones:
        1. expected_tables ⊆ current_tables
           → Las 9 tablas definidas existen en la BD
        2. len(expected_tables) == 9
           → Exactamente 9 tablas son requeridas (validación redundante)
    """
    # Define el conjunto de 9 tablas que debe tener el sistema
    expected_tables = {
        "usuarios",
        "empleados",
        "salas",
        "horarios",
        "actividades",
        "reservas",
        "pagos",
        "materiales",
        "incidencias",
    }

    # Inspecciona el motor de BD para obtener los nombres de tablas actuales
    inspector = inspect(db.engine)
    current_tables = set(inspector.get_table_names())

    # Verifica que todas las tablas esperadas existen
    assert expected_tables.issubset(current_tables), (
        f"Faltan tablas en la BD. Esperadas: {expected_tables}, "
        f"Encontradas: {current_tables}"
    )
    
    # Verifica que se definieron exactamente 9 tablas
    assert len(expected_tables) == 9, (
        f"Se espera exactamente 9 tablas, pero se definieron {len(expected_tables)}"
    )
