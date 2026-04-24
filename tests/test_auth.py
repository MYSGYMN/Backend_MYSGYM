import pytest

def test_register_usuario_exitoso(client):
    """Prueba que un usuario se puede registrar correctamente."""
    payload = {
        "nombre": "Test User",
        "email": "test@gym.com",
        "password": "password123",
        "telefono": "123456789"
    }
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Usuario registrado con éxito"

def test_register_usuario_faltan_datos(client):
    """Prueba error al registrar usuario sin email o password."""
    payload = {"nombre": "Incompleto"}
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 400
    assert "Email y contraseña son obligatorios" in response.get_json()["message"]

def test_register_usuario_duplicado(client):
    """Prueba que no se puede registrar un email que ya existe."""
    payload = {
        "nombre": "User 1",
        "email": "repetido@gym.com",
        "password": "password123"
    }
    # Primer registro
    client.post('/auth/register', json=payload)
    # Segundo registro con mismo email
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 400
    assert "El usuario ya existe" in response.get_json()["message"]

def test_login_usuario_exitoso(client):
    """Prueba login correcto y obtención de JWT."""
    # Primero registramos al usuario
    payload = {"nombre": "User Login", "email": "login@gym.com", "password": "123"}
    client.post('/auth/register', json=payload)
    
    # Intentamos login
    login_payload = {"email": "login@gym.com", "password": "123"}
    response = client.post('/auth/login', json=login_payload)
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_login_usuario_credenciales_invalidas(client):
    """Prueba error en login con contraseña incorrecta."""
    payload = {"email": "error@gym.com", "password": "wrong"}
    response = client.post('/auth/login', json=payload)
    assert response.status_code == 401
    assert "Credenciales inválidas" in response.get_json()["message"]

def test_register_empleado_exitoso(client):
    """Prueba registro de empleado."""
    payload = {
        "nombre": "Empleado Test",
        "email": "empleado@gym.com",
        "password": "123",
        "rol": "monitor"
    }
    response = client.post('/auth/register-empleado', json=payload)
    assert response.status_code == 201
    assert "Empleado registrado con éxito" in response.get_json()["message"]

def test_login_empleado_exitoso(client):
    """Prueba login de empleado."""
    # Registro previo
    payload = {"nombre": "Emp", "email": "emp@gym.com", "password": "123", "rol": "admin"}
    client.post('/auth/register-empleado', json=payload)
    
    # Login
    response = client.post('/auth/login-empleado', json={"email": "emp@gym.com", "password": "123"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()
