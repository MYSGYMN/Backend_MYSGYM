import pytest
from werkzeug.security import generate_password_hash
from app.models import Empleado, db

@pytest.fixture
def admin_header(client):
    """Fixture: registra y loguea un empleado con rol admin."""
    client.post('/auth/register-empleado', json={
        "nombre": "Admin", "email": "admin_emp@test.com",
        "password": "admin123", "rol": "admin"
    })
    response = client.post('/auth/login-empleado', json={
        "email": "admin_emp@test.com", "password": "admin123"
    })
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def empleado_existente(app, admin_header):
    """Fixture: crea un empleado en la BD y retorna su ID."""
    empleado = Empleado(
        nombre="Empleado Test",
        email="emp_test@gym.com",
        rol="monitor",
        password_hash=generate_password_hash("123")
    )
    db.session.add(empleado)
    db.session.commit()
    return empleado.id_empleado

def test_get_empleados(client, admin_header):
    """Prueba listar todos los empleados como admin."""
    response = client.get('/empleados/', headers=admin_header)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_crear_empleado(client, admin_header):
    """Prueba crear un nuevo empleado como admin."""
    payload = {"nombre": "Nuevo Monitor", "email": "nuevo@gym.com", "rol": "monitor"}
    response = client.post('/empleados/', json=payload, headers=admin_header)
    assert response.status_code == 201
    assert "registrado" in response.get_json()["message"]

def test_actualizar_empleado(client, admin_header, empleado_existente):
    """Prueba actualizar datos de un empleado."""
    payload = {"nombre": "Monitor Actualizado", "rol": "admin"}
    response = client.put(f'/empleados/{empleado_existente}', json=payload, headers=admin_header)
    assert response.status_code == 200
    assert "actualizado" in response.get_json()["message"]

def test_actualizar_empleado_no_existe(client, admin_header):
    """Prueba actualizar un empleado que no existe."""
    response = client.put('/empleados/99999', json={"nombre": "X"}, headers=admin_header)
    assert response.status_code == 404

def test_eliminar_empleado(client, admin_header, empleado_existente):
    """Prueba eliminar un empleado como admin."""
    response = client.delete(f'/empleados/{empleado_existente}', headers=admin_header)
    assert response.status_code == 200
    assert "eliminado" in response.get_json()["message"]

def test_eliminar_empleado_no_existe(client, admin_header):
    """Prueba eliminar un empleado que no existe."""
    response = client.delete('/empleados/99999', headers=admin_header)
    assert response.status_code == 404
