import pytest

@pytest.fixture
def admin_header(client):
    """Fixture: registra y loguea un empleado con rol admin."""
    client.post('/auth/register-empleado', json={
        "nombre": "Admin Pago", "email": "admin_pago@test.com",
        "password": "123", "rol": "admin"
    })
    response = client.post('/auth/login-empleado', json={
        "email": "admin_pago@test.com", "password": "123"
    })
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_header(client):
    """Fixture: registra y loguea un usuario cliente."""
    client.post('/auth/register', json={
        "nombre": "Pagador", "email": "pagador@test.com", "password": "123"
    })
    response = client.post('/auth/login', json={"email": "pagador@test.com", "password": "123"})
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def pago_id(client, user_header):
    """Fixture: registra un pago y devuelve su ID."""
    client.post('/pagos/', json={"monto": 50.0, "metodo_pago": "Tarjeta"}, headers=user_header)
    historial = client.get('/pagos/historial', headers=user_header).get_json()
    return historial[0]["id_pago"]

def test_registrar_pago(client, user_header):
    """Prueba registrar un pago con éxito."""
    payload = {"monto": 30.0, "metodo_pago": "Efectivo"}
    response = client.post('/pagos/', json=payload, headers=user_header)
    assert response.status_code == 201
    assert "Pago registrado" in response.get_json()["message"]

def test_historial_pagos(client, user_header, pago_id):
    """Prueba ver el historial de pagos del usuario."""
    response = client.get('/pagos/historial', headers=user_header)
    assert response.status_code == 200
    assert len(response.get_json()) >= 1

def test_listar_pagos_admin(client, user_header, admin_header):
    """Prueba listar pagos desde el panel de administración."""
    client.post('/pagos/', json={"monto": 50.0, "metodo_pago": "Tarjeta"}, headers=user_header)
    response = client.get('/pagos/', headers=admin_header)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data and "usuario" in data[0]

def test_actualizar_pago(client, user_header, pago_id):
    """Prueba actualizar un pago existente."""
    payload = {"estado": "Cancelado", "monto": 25.0}
    response = client.put(f'/pagos/{pago_id}', json=payload, headers=user_header)
    assert response.status_code == 200
    assert "actualizado" in response.get_json()["message"]

def test_actualizar_pago_no_existe(client, user_header):
    """Prueba actualizar un pago que no existe."""
    response = client.put('/pagos/99999', json={"estado": "Cancelado"}, headers=user_header)
    assert response.status_code == 404

def test_eliminar_pago(client, user_header, pago_id):
    """Prueba eliminar un pago."""
    response = client.delete(f'/pagos/{pago_id}', headers=user_header)
    assert response.status_code == 200
    assert "eliminado" in response.get_json()["message"]

def test_eliminar_pago_no_existe(client, user_header):
    """Prueba eliminar un pago que no existe."""
    response = client.delete('/pagos/99999', headers=user_header)
    assert response.status_code == 404

def test_registrar_pago_sin_token(client):
    """Prueba que sin token no se puede registrar un pago."""
    response = client.post('/pagos/', json={"monto": 10.0})
    assert response.status_code == 401
