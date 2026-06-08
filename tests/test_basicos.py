def test_home_page_route(client):
    """La raíz debe servir la portada unificada del frontend."""
    response = client.get('/')

    assert response.status_code == 200
    assert b"MYSGYM" in response.data


def test_api_health_route(client):
    """La información de salud de la API vive en /api."""
    response = client.get('/api')

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "Bienvenido a la API de MYSGYM" in data["message"]

def test_404_not_found(client):
    """Verifica que una ruta que no existe devuelve 404."""
    response = client.get('/ruta-inexistente')
    assert response.status_code == 404
