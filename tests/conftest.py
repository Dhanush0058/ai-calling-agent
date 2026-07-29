from fastapi.testclient import TestClient
import pytest
from app.main import app
import random
import uuid
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "dhanushr672@example.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }



@pytest.fixture
def customer_payload():
    unique = random.randint(10000000, 99999999)

    return {
        "name": "Pytest User",
        "email": f"pytest{unique}@example.com",
        "phone": f"98{unique}",
    }

@pytest.fixture
def created_customer(client, auth_headers, customer_payload):

    response = client.post(
        "/customers",
        headers=auth_headers,
        json=customer_payload,
    )

    assert response.status_code == 201

    return response.json()

@pytest.fixture
def updated_customer_payload():
    unique = random.randint(10000000, 99999999)

    return {
        "name": "Updated User",
        "email": f"updated{unique}@example.com",
        "phone": f"99{unique}",
    }