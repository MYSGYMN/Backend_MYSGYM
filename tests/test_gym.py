import pytest
from werkzeug.security import generate_password_hash
from app.models import Sala, Horario, Empleado, Actividad, db
from datetime import time

@pytest.fixture
def admin_header(client):
    """Fixture: registra y loguea un empleado con rol admin."""
    client.post('/auth/register-empleado', json={
        "nombre": "Admin Gym", "email": "admin_gym@test.com",
        "password": "admin123", "rol": "admin"
    })
    response = client.post('/auth/login-empleado', json={
        "email": "admin_gym@test.com", "password": "admin123"
    })
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def setup_gym(app):
    """Fixture: crea sala, monitor, horario y actividad base para los tests."""
    sala = Sala(nombre="Sala Prueba", capacidad=20)
    monitor = Empleado(
        nombre="Monitor Gym", email="mon_gym@test.com",
        rol="monitor", password_hash=generate_password_hash("123")
    )
    horario = Horario(dia_semana="Martes", hora_inicio=time(9, 0), hora_fin=time(10, 0))
    db.session.add_all([sala, monitor, horario])
    db.session.commit()

    actividad = Actividad(
        nombre="Pilates", descripcion="Clase de pilates",
        monitor_id=monitor.id_empleado, sala_id=sala.id_sala,
        horario_id=horario.id_horario, aforo_maximo=15
    )
    db.session.add(actividad)
    db.session.commit()
    return {
        "sala_id": sala.id_sala,
        "monitor_id": monitor.id_empleado,
        "horario_id": horario.id_horario,
        "actividad_id": actividad.id_actividad
    }

# --- TESTS DE ACTIVIDADES ---

def test_get_actividades(client, setup_gym):
    """Prueba listar actividades (ruta pública)."""
    response = client.get('/gym/actividades')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) >= 1

def test_create_actividad(client, admin_header, setup_gym):
    """Prueba crear una actividad como admin."""
    payload = {
        "nombre": "Zumba", "descripcion": "Baile fitness",
        "monitor_id": setup_gym["monitor_id"],
        "sala_id": setup_gym["sala_id"],
        "horario_id": setup_gym["horario_id"],
        "aforo_maximo": 10
    }
    response = client.post('/gym/actividades', json=payload, headers=admin_header)
    assert response.status_code == 201

def test_update_actividad(client, admin_header, setup_gym):
    """Prueba actualizar una actividad."""
    payload = {"nombre": "Pilates Avanzado", "aforo_maximo": 5}
    response = client.put(
        f'/gym/actividades/{setup_gym["actividad_id"]}',
        json=payload, headers=admin_header
    )
    assert response.status_code == 200

def test_delete_actividad(client, admin_header, setup_gym):
    """Prueba eliminar una actividad."""
    response = client.delete(
        f'/gym/actividades/{setup_gym["actividad_id"]}',
        headers=admin_header
    )
    assert response.status_code == 200

# --- TESTS DE SALAS ---

def test_get_salas(client):
    """Prueba listar salas (ruta pública)."""
    response = client.get('/gym/salas')
    assert response.status_code == 200

def test_create_sala(client, admin_header):
    """Prueba crear una sala como admin."""
    payload = {"nombre": "Sala Cardio", "capacidad": 30}
    response = client.post('/gym/salas', json=payload, headers=admin_header)
    assert response.status_code == 201

def test_update_sala(client, admin_header, setup_gym):
    """Prueba actualizar una sala."""
    response = client.put(
        f'/gym/salas/{setup_gym["sala_id"]}',
        json={"nombre": "Sala Renovada", "capacidad": 25},
        headers=admin_header
    )
    assert response.status_code == 200

def test_update_sala_no_existe(client, admin_header):
    """Prueba actualizar una sala que no existe."""
    response = client.put('/gym/salas/99999', json={"nombre": "X"}, headers=admin_header)
    assert response.status_code == 404

def test_delete_sala_no_existe(client, admin_header):
    """Prueba eliminar una sala que no existe."""
    response = client.delete('/gym/salas/99999', headers=admin_header)
    assert response.status_code == 404

# --- TESTS DE HORARIOS ---

def test_get_horarios(client):
    """Prueba listar horarios (ruta pública)."""
    response = client.get('/gym/horarios')
    assert response.status_code == 200

def test_create_horario(client, admin_header):
    """Prueba crear un horario como admin."""
    payload = {"dia_semana": "Viernes", "hora_inicio": "18:00", "hora_fin": "19:00"}
    response = client.post('/gym/horarios', json=payload, headers=admin_header)
    assert response.status_code == 201

def test_update_and_delete_horario(client, admin_header, setup_gym):
    """Prueba actualizar y eliminar un horario existente."""
    payload = {"dia_semana": "Miercoles", "hora_inicio": "10:30", "hora_fin": "11:30"}
    response = client.put(
        f'/gym/horarios/{setup_gym["horario_id"]}',
        json=payload,
        headers=admin_header
    )
    assert response.status_code == 200

    response = client.delete(
        f'/gym/horarios/{setup_gym["horario_id"]}',
        headers=admin_header
    )
    assert response.status_code == 200
