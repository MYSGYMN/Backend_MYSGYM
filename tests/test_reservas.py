import pytest
from werkzeug.security import generate_password_hash
from app.models import Sala, Empleado, Actividad, Horario, Reserva, db
from datetime import time

@pytest.fixture
def admin_header(client):
    """Fixture para obtener un token de admin."""
    client.post('/auth/register-empleado', json={
        "nombre": "Admin Reserva", "email": "admin_reserva@test.com",
        "password": "123", "rol": "admin"
    })
    response = client.post('/auth/login-empleado', json={
        "email": "admin_reserva@test.com", "password": "123"
    })
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_header(client):
    """Fixture para obtener el token de autenticación."""
    email = "reserva@test.com"
    client.post('/auth/register', json={
        "nombre": "User Test", "email": email, "password": "123"
    })
    response = client.post('/auth/login', json={"email": email, "password": "123"})
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def setup_actividad(app):
    """Crea una actividad necesaria para las reservas.
    
    IMPORTANTE: No usamos 'with app.app_context()' aquí porque el conftest.py
    ya provee un contexto activo (yield app). Usar el mismo contexto garantiza
    que los datos sean visibles para las peticiones del cliente de test.
    """
    sala = Sala(nombre="Sala Zen", capacidad=10)
    monitor = Empleado(
        nombre="Monitor", email="mon@test.com", rol="monitor",
        password_hash=generate_password_hash("123")
    )
    horario = Horario(dia_semana="Lunes", hora_inicio=time(10, 0), hora_fin=time(11, 0))

    db.session.add_all([sala, monitor, horario])
    db.session.commit()

    actividad = Actividad(
        nombre="Yoga", monitor_id=monitor.id_empleado,
        sala_id=sala.id_sala, horario_id=horario.id_horario, aforo_maximo=1
    )
    db.session.add(actividad)
    db.session.commit()
    return actividad.id_actividad

def test_crear_reserva_exitosa(client, auth_header, setup_actividad):
    """Prueba crear una reserva con éxito."""
    payload = {"actividad_id": setup_actividad}
    response = client.post('/reservas', json=payload, headers=auth_header)
    assert response.status_code == 201

def test_crear_reserva_actividad_llena(client, auth_header, setup_actividad):
    """Prueba que no permite reservar si el aforo está completo."""
    payload = {"actividad_id": setup_actividad}
    client.post('/reservas', json=payload, headers=auth_header)
    response = client.post('/reservas', json=payload, headers=auth_header)
    assert response.status_code == 400

def test_listar_mis_reservas(client, auth_header, setup_actividad):
    """Prueba listar las reservas del usuario actual."""
    client.post('/reservas', json={"actividad_id": setup_actividad}, headers=auth_header)
    response = client.get('/reservas/mis-reservas', headers=auth_header)
    assert response.status_code == 200
    assert len(response.get_json()) >= 1

def test_cancelar_reserva(client, auth_header, setup_actividad):
    """Prueba cancelar una reserva existente."""
    client.post('/reservas', json={"actividad_id": setup_actividad}, headers=auth_header)
    res_data = client.get('/reservas/mis-reservas', headers=auth_header).get_json()
    res_id = res_data[0]["id_reserva"]

    response = client.delete(f'/reservas/{res_id}', headers=auth_header)
    assert response.status_code == 200

def test_listar_reservas_admin(client, admin_header, auth_header, setup_actividad):
    """Prueba listar reservas desde el panel de administración."""
    client.post('/reservas', json={"actividad_id": setup_actividad}, headers=auth_header)
    response = client.get('/reservas/', headers=admin_header)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data and "usuario" in data[0]
