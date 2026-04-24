import pytest
from app.models import Usuario, db

@pytest.fixture
def admin_header(client):
    """Fixture: registra y loguea un empleado con rol admin para rutas protegidas."""
    client.post('/auth/register-empleado', json={
        "nombre": "Admin Test", "email": "admin@test.com",
        "password": "admin123", "rol": "admin"
    })
    response = client.post('/auth/login-empleado', json={
        "email": "admin@test.com", "password": "admin123"
    })
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_header(client):
    """Fixture: registra y loguea un usuario cliente."""
    client.post('/auth/register', json={
        "nombre": "User Normal", "email": "user@test.com", "password": "123"
    })
    response = client.post('/auth/login', json={"email": "user@test.com", "password": "123"})
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_id(client, user_header):
    """Fixture: devuelve el ID del usuario logueado."""
    response = client.get('/usuarios/perfil', headers=user_header)
    return response.get_json()["id_usuario"]

def test_get_perfil(client, user_header):
    """Prueba obtener el perfil del usuario actual."""
    response = client.get('/usuarios/perfil', headers=user_header)
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "user@test.com"
    assert "nombre" in data

def test_get_perfil_sin_token(client):
    """Prueba que sin token no se puede acceder al perfil."""
    response = client.get('/usuarios/perfil')
    assert response.status_code == 401

def test_get_usuarios_como_admin(client, admin_header):
    """Prueba listar todos los usuarios como admin."""
    response = client.get('/usuarios/', headers=admin_header)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_usuarios_sin_permiso(client, user_header):
    """Prueba que un cliente no puede ver la lista de usuarios."""
    response = client.get('/usuarios/', headers=user_header)
    assert response.status_code == 403

def test_update_usuario_propio(client, user_header, user_id):
    """Prueba que un usuario puede actualizar su propio perfil."""
    payload = {"nombre": "Nombre Actualizado", "telefono": "999888777"}
    response = client.put(f'/usuarios/{user_id}', json=payload, headers=user_header)
    assert response.status_code == 200
    assert "actualizado" in response.get_json()["message"]

def test_delete_usuario_como_admin(client, admin_header, user_header, user_id):
    """Prueba que un admin puede eliminar un usuario."""
    response = client.delete(f'/usuarios/{user_id}', headers=admin_header)
    assert response.status_code == 200
    assert "eliminado" in response.get_json()["message"]

def test_delete_usuario_no_existe(client, admin_header):
    """Prueba que eliminar un usuario inexistente devuelve 404."""
    response = client.delete('/usuarios/99999', headers=admin_header)
    assert response.status_code == 404
