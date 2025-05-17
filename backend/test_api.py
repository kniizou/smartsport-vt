# backend/test_api.py
import requests

BASE_URL = "http://localhost:8000/api"


def test_endpoints():
    # Test inscription
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Jean",
        "last_name": "Dupont",
        "role": "joueur"
    }
    response = requests.post(f"{BASE_URL}/register/", json=register_data)
    print("Inscription:", response.status_code, response.json())

    # Test connexion
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/login/", json=login_data)
    print("Connexion:", response.status_code, response.json())


if __name__ == "__main__":
    test_endpoints()
