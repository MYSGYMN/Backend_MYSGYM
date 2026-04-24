import pytest
from app.models import Usuario, Empleado, Actividad, Sala, Horario, Reserva, Material, Incidencia, db
from werkzeug.security import generate_password_hash
from datetime import time

@pytest.fixture
def admin_header(client):
    client.post('/auth/register-empleado', json={
        "nombre": "Admin Cob", "email": "admin_cob@test.com",
        "password": "123", "rol": "admin"
    })
    response = client.post('/auth/login-empleado', json={
        "email": "admin_cob@test.com", "password": "123"
    })
    return {"Authorization": f"Bearer {response.get_json()['access_token']}"}

@pytest.fixture
def user_header(client):
    client.post('/auth/register', json={
        "nombre": "User Cob", "email": "user_cob@test.com", "password": "123"
    })
    response = client.post('/auth/login', json={"email": "user_cob@test.com", "password": "123"})
    return {"Authorization": f"Bearer {response.get_json()['access_token']}"}

@pytest.fixture
def other_user_header(client):
    client.post('/auth/register', json={
        "nombre": "Other", "email": "other_cov@test.com", "password": "123"
    })
    response = client.post('/auth/login', json={"email": "other_cov@test.com", "password": "123"})
    return {"Authorization": f"Bearer {response.get_json()['access_token']}"}

# --- AUTH EXTRA ---
def test_register_empleado_duplicado(client):
    payload = {"nombre": "Emp", "email": "emp_dup@test.com", "password": "123"}
    client.post('/auth/register-empleado', json=payload)
    response = client.post('/auth/register-empleado', json=payload)
    assert response.status_code == 400
    assert "existe" in response.get_json()["message"]

def test_register_empleado_faltan_datos(client):
    response = client.post('/auth/register-empleado', json={"nombre": "X"})
    assert response.status_code == 400

def test_login_empleado_invalido(client):
    response = client.post('/auth/login-empleado', json={"email": "no@existe.com", "password": "X"})
    assert response.status_code == 401

# --- GYM EXTRA ---
def test_gym_404_cases(client, admin_header):
    assert client.put('/gym/actividades/999', json={}, headers=admin_header).status_code == 404
    assert client.delete('/gym/actividades/999', headers=admin_header).status_code == 404
    
    # Test delete sala exitoso
    client.post('/gym/salas', json={"nombre": "Borrar", "capacidad": 1}, headers=admin_header)
    salas = client.get('/gym/salas').get_json()
    sala_id = [s["id_sala"] for s in salas if s["nombre"] == "Borrar"][0]
    assert client.delete(f'/gym/salas/{sala_id}', headers=admin_header).status_code == 200

# --- MANTENIMIENTO EXTRA ---
def test_incidencia_cases(client, admin_header, user_header):
    # 404
    assert client.put('/mantenimiento/incidencias/999', json={}, headers=admin_header).status_code == 404
    
    # Success update (para cubrir líneas 101-106)
    client.post('/mantenimiento/incidencias', json={"descripcion": "Prueba"}, headers=user_header)
    incidencias = client.get('/mantenimiento/incidencias', headers=admin_header).get_json()
    inc_id = incidencias[-1]["id_incidencia"]
    payload = {"descripcion": "Actualizada", "estado": "resuelto"}
    assert client.put(f'/mantenimiento/incidencias/{inc_id}', json=payload, headers=admin_header).status_code == 200

# --- RESERVAS EXTRA ---
def test_reservas_edge_cases(client, user_header, other_user_header, app):
    # Sin ID
    assert client.post('/reservas', json={}, headers=user_header).status_code == 400
    # Actividad no existe
    assert client.post('/reservas', json={"actividad_id": 999}, headers=user_header).status_code == 404
    # Cancelar no existe
    assert client.delete('/reservas/999', headers=user_header).status_code == 404
    
    s = Sala(nombre="S21", capacidad=10)
    h = Horario(dia_semana="L", hora_inicio=time(10), hora_fin=time(11))
    db.session.add_all([s, h])
    db.session.commit()
    a = Actividad(nombre="A21", sala_id=s.id_sala, horario_id=h.id_horario, aforo_maximo=10)
    db.session.add(a)
    db.session.commit()
    act_id = a.id_actividad
    
    client.post('/reservas', json={"actividad_id": act_id}, headers=user_header)
    reservas = client.get('/reservas/mis-reservas', headers=user_header).get_json()
    res_id = reservas[-1]["id_reserva"]
    
    # Cancelar con otro usuario (403)
    assert client.delete(f'/reservas/{res_id}', headers=other_user_header).status_code == 403
    
    # Actualizar estado success (para cubrir líneas 73-81)
    assert client.put(f'/reservas/{res_id}', json={"estado": "Confirmada"}, headers=user_header).status_code == 200
    assert client.put('/reservas/999', json={"estado": "X"}, headers=user_header).status_code == 404

# --- USUARIOS EXTRA ---
def test_usuarios_edge_cases(client, user_header, other_user_header, admin_header):
    # Perfil no existe
    uid = client.get('/usuarios/perfil', headers=user_header).get_json()["id_usuario"]
    client.delete(f'/usuarios/{uid}', headers=admin_header)
    assert client.get('/usuarios/perfil', headers=user_header).status_code == 404
    
    # Update sin permiso
    client.post('/auth/register', json={"nombre": "U2", "email": "u2_edge@t.com", "password": "1"})
    u2_token = client.post('/auth/login', json={"email": "u2_edge@t.com", "password": "1"}).get_json()["access_token"]
    u2_headers = {"Authorization": f"Bearer {u2_token}"}
    u2_id = client.get('/usuarios/perfil', headers=u2_headers).get_json()["id_usuario"]
    
    # Intentar editar un ID que no es el suyo (y no es admin)
    assert client.put(f'/usuarios/{u2_id + 1}', json={"nombre": "X"}, headers=u2_headers).status_code == 403
    assert client.put('/usuarios/999', json={"nombre": "X"}, headers=admin_header).status_code == 404
