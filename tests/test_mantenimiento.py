import pytest
from werkzeug.security import generate_password_hash
from app.models import Sala, Empleado, Material, db

@pytest.fixture
def admin_header(client):
    """Fixture: registra y loguea un empleado con rol admin."""
    client.post('/auth/register-empleado', json={
        "nombre": "Admin Mant", "email": "admin_mant@test.com",
        "password": "admin123", "rol": "admin"
    })
    response = client.post('/auth/login-empleado', json={
        "email": "admin_mant@test.com", "password": "admin123"
    })
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_header(client):
    """Fixture: registra y loguea un usuario cliente."""
    client.post('/auth/register', json={
        "nombre": "User Mant", "email": "user_mant@test.com", "password": "123"
    })
    response = client.post('/auth/login', json={"email": "user_mant@test.com", "password": "123"})
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def material_id(app, admin_header):
    """Fixture: crea un material de prueba y devuelve su ID."""
    sala = Sala(nombre="Sala Mat", capacidad=5)
    db.session.add(sala)
    db.session.commit()

    material = Material(nombre="Mancuerna 5kg", estado="Bueno", sala_id=sala.id_sala)
    db.session.add(material)
    db.session.commit()
    return material.id_material

# --- TESTS DE MATERIALES ---

def test_get_materiales(client):
    """Prueba listar materiales (ruta pública)."""
    response = client.get('/mantenimiento/materiales')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_crear_material(client, admin_header):
    """Prueba crear un material como admin."""
    payload = {"nombre": "Cuerda de saltar", "estado": "Bueno"}
    response = client.post('/mantenimiento/materiales', json=payload, headers=admin_header)
    assert response.status_code == 201
    assert "registrado" in response.get_json()["message"]

def test_actualizar_material(client, admin_header, material_id):
    """Prueba actualizar el estado de un material."""
    payload = {"estado": "En reparación"}
    response = client.put(f'/mantenimiento/materiales/{material_id}', json=payload, headers=admin_header)
    assert response.status_code == 200
    assert "actualizado" in response.get_json()["message"]

def test_actualizar_material_no_existe(client, admin_header):
    """Prueba actualizar un material que no existe."""
    response = client.put('/mantenimiento/materiales/99999', json={"estado": "X"}, headers=admin_header)
    assert response.status_code == 404

def test_eliminar_material(client, admin_header, material_id):
    """Prueba eliminar un material."""
    response = client.delete(f'/mantenimiento/materiales/{material_id}', headers=admin_header)
    assert response.status_code == 200
    assert "eliminado" in response.get_json()["message"]

def test_eliminar_material_no_existe(client, admin_header):
    """Prueba eliminar un material que no existe."""
    response = client.delete('/mantenimiento/materiales/99999', headers=admin_header)
    assert response.status_code == 404

# --- TESTS DE INCIDENCIAS ---

def test_reportar_incidencia(client, user_header, material_id):
    """Prueba reportar una incidencia sobre un material."""
    payload = {"descripcion": "La mancuerna está rota", "material_id": material_id}
    response = client.post('/mantenimiento/incidencias', json=payload, headers=user_header)
    assert response.status_code == 201
    assert "reportada" in response.get_json()["message"]

def test_listar_incidencias_como_admin(client, admin_header, user_header, material_id):
    """Prueba listar incidencias como admin."""
    client.post('/mantenimiento/incidencias',
                json={"descripcion": "Incidencia test", "material_id": material_id},
                headers=user_header)
    response = client.get('/mantenimiento/incidencias', headers=admin_header)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_listar_incidencias_sin_permiso(client, user_header):
    """Prueba que un usuario cliente no puede listar incidencias."""
    response = client.get('/mantenimiento/incidencias', headers=user_header)
    assert response.status_code == 403
