from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    """
    Test para crear un usuario
    """
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["is_active"] == True
    assert "id" in data
    assert "created_at" in data

def test_get_users():
    """
    Test para obtener lista de usuarios
    """
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_user():
    """
    Test para obtener un usuario específico
    """
    # Primero crear un usuario
    user_data = {
        "email": "test2@example.com",
        "full_name": "Test User 2",
        "password": "testpassword123"
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Luego obtener el usuario
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == user_data["email"]

def test_get_user_not_found():
    """
    Test para obtener un usuario que no existe
    """
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"

def test_update_user():
    """
    Test para actualizar un usuario
    """
    # Primero crear un usuario
    user_data = {
        "email": "test3@example.com",
        "full_name": "Test User 3",
        "password": "testpassword123"
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Luego actualizar el usuario
    update_data = {
        "full_name": "Updated User Name"
    }
    
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]

def test_delete_user():
    """
    Test para eliminar un usuario
    """
    # Primero crear un usuario
    user_data = {
        "email": "test4@example.com",
        "full_name": "Test User 4",
        "password": "testpassword123"
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Luego eliminar el usuario
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204
    
    # Verificar que el usuario ya no existe
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404
