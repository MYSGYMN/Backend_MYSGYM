"""
Tests de integracion para validar la estructura de la base de datos de test.

Este modulo verifica que:
1. La aplicacion Flask de test usa una base de datos aislada
2. Los modelos de SQLAlchemy se traducen en las tablas esperadas
3. Las tablas principales tienen columnas y claves foraneas criticas
"""

import pytest
from sqlalchemy import inspect

from app import db


EXPECTED_TABLES = {
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


def column_names(inspector, table_name):
    """Devuelve los nombres de columnas para una tabla."""
    return {column["name"] for column in inspector.get_columns(table_name)}


@pytest.mark.integration
def test_uses_isolated_test_database(app):
    """Evita ejecutar tests destructivos contra MySQL u otra BD real."""
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///")


@pytest.mark.integration
def test_creates_expected_tables(app):
    """Verifica que la base de datos de test contiene las tablas del sistema."""
    inspector = inspect(db.engine)
    current_tables = set(inspector.get_table_names())

    assert EXPECTED_TABLES.issubset(current_tables), (
        f"Faltan tablas en la BD. Esperadas: {EXPECTED_TABLES}, "
        f"Encontradas: {current_tables}"
    )


@pytest.mark.integration
def test_core_columns_match_models(app):
    """Comprueba columnas que suelen romper rutas si se renombran mal."""
    inspector = inspect(db.engine)

    assert {
        "id_usuario",
        "nombre",
        "email",
        "password_hash",
        "telefono",
        "fecha_registro",
        "estado",
    }.issubset(column_names(inspector, "usuarios"))

    assert {
        "id_empleado",
        "nombre",
        "email",
        "rol",
        "password_hash",
        "fecha_contratacion",
    }.issubset(column_names(inspector, "empleados"))

    assert {
        "id_pago",
        "usuario_id",
        "fecha_pago",
        "monto",
        "metodo_pago",
        "estado",
    }.issubset(column_names(inspector, "pagos"))


@pytest.mark.integration
def test_foreign_keys_match_relationships(app):
    """Verifica claves foraneas importantes entre reservas, pagos y actividades."""
    inspector = inspect(db.engine)

    reservas_fks = {
        fk["constrained_columns"][0]: fk["referred_table"]
        for fk in inspector.get_foreign_keys("reservas")
    }
    pagos_fks = {
        fk["constrained_columns"][0]: fk["referred_table"]
        for fk in inspector.get_foreign_keys("pagos")
    }
    actividades_fks = {
        fk["constrained_columns"][0]: fk["referred_table"]
        for fk in inspector.get_foreign_keys("actividades")
    }

    assert reservas_fks == {
        "usuario_id": "usuarios",
        "actividad_id": "actividades",
    }
    assert pagos_fks == {"usuario_id": "usuarios"}
    assert actividades_fks == {
        "monitor_id": "empleados",
        "sala_id": "salas",
        "horario_id": "horarios",
    }
