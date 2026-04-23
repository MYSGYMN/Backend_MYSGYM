def test_index_route(client):
    """
    Test básico para verificar que la raíz de la API responde correctamente.
    Este es el 'Health Check' inicial.
    """
    response = client.get('/')
    
    # Verificamos que el código de estado sea 200 (OK)
    assert response.status_code == 200
    
    # Verificamos que la respuesta sea JSON y tenga el mensaje de bienvenida
    data = response.get_json()
    assert data["status"] == "success"
    assert "Bienvenido a la API de MYSGYM" in data["message"]

def test_404_not_found(client):
    """Verifica que una ruta que no existe devuelve 404."""
    response = client.get('/ruta-inexistente')
    assert response.status_code == 404
