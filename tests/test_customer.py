import uuid

unique = uuid.uuid4().hex[:6]

def test_get_customers(client, auth_headers):

    response = client.get(
        "/customers",
        headers=auth_headers,
    )

    assert response.status_code == 200

def test_create_customer(client, auth_headers, customer_payload):

    response = client.post(
        "/customers",
        headers=auth_headers,
        json=customer_payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == customer_payload["name"]
    assert data["email"] == customer_payload["email"]
    assert data["phone"] == customer_payload["phone"]

def test_get_customer_by_id(
    client,
    auth_headers,
    created_customer,
):

    customer_id = created_customer["id"]

    response = client.get(
        f"/customers/{customer_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == customer_id
    assert data["email"] == created_customer["email"]
    assert data["phone"] == created_customer["phone"]

def test_update_customer(
    client,
    auth_headers,
    created_customer,
    updated_customer_payload,
):
    customer_id = created_customer["id"]

    response = client.put(
        f"/customers/{customer_id}",
        headers=auth_headers,
        json=updated_customer_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == customer_id
    assert data["name"] == updated_customer_payload["name"]
    assert data["email"] == updated_customer_payload["email"]
    assert data["phone"] == updated_customer_payload["phone"]

def test_delete_customer(
    client,
    auth_headers,
    created_customer,
):
    customer_id = created_customer["id"]

    response = client.delete(
        f"/customers/{customer_id}",
        headers=auth_headers,
    )

    # Adjust if your API returns 204 instead
    assert response.status_code == 204

    response = client.get(
        f"/customers/{customer_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_all_customers(
    client,
    auth_headers,
    created_customer,
):
    response = client.get(
        "/customers?limit=100",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    # Verify pagination response
    assert isinstance(data, dict)

    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data

    # Get the list of customers
    customers = data["items"]

    assert isinstance(customers, list)
    assert len(customers) >= 1

    # Find the customer created by the fixture
    customer = next(
        (
            c
            for c in customers
            if c["id"] == created_customer["id"]
        ),
        None,
    )

    assert customer is not None

    assert customer["name"] == created_customer["name"]
    assert customer["email"] == created_customer["email"]
    assert customer["phone"] == created_customer["phone"]

def test_get_customers_with_limit(
    client,
    auth_headers,
):
    response = client.get(
        "/customers?limit=5",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) <= 5
    assert data["limit"] == 5

def test_get_customers_with_skip(
    client,
    auth_headers,
):
    response = client.get(
        "/customers?skip=5&limit=5",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["skip"] == 5
    assert data["limit"] == 5

    assert len(data["items"]) <= 5

def test_pagination_metadata(
    client,
    auth_headers,
):
    response = client.get(
        "/customers",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data

    assert isinstance(data["total"], int)
    assert isinstance(data["skip"], int)
    assert isinstance(data["limit"], int)


def test_search_customer(
    client,
    auth_headers,
    created_customer,
):
    response = client.get(
        f"/customers?search={created_customer['email']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()
    customers = data["items"]

    assert len(customers) == 1
    assert customers[0]["id"] == created_customer["id"]

def test_search_non_existing_customer(
    client,
    auth_headers,
):
    response = client.get(
        "/customers?search=xyz123456789",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []

def test_filter_customer_by_email(
    client,
    auth_headers,
    created_customer,
):
    response = client.get(
        f"/customers?email={created_customer['email']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    customers = data["items"]

    assert len(customers) == 1

    assert customers[0]["email"] == created_customer["email"]

def test_filter_customer_by_phone(
    client,
    auth_headers,
    created_customer,
):
    response = client.get(
        f"/customers?phone={created_customer['phone']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    customers = data["items"]

    assert len(customers) == 1

    assert customers[0]["phone"] == created_customer["phone"]

def test_sort_customers_by_name(
    client,
    auth_headers,
):
    response = client.get(
        "/customers?sort=name&limit=100",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    customers = data["items"]

    names = [customer["name"] for customer in customers]

    assert names == sorted(names)

def test_sort_customers_by_name_desc(
    client,
    auth_headers,
):
    response = client.get(
        "/customers?sort=-name&limit=100",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    customers = data["items"]

    names = [customer["name"] for customer in customers]

    assert names == sorted(names, reverse=True)

def test_get_customers_without_token(client):
    response = client.get("/customers")

    # print(response.status_code)
    # print(response.json())

def test_get_customers_with_invalid_token(client):
    response = client.get(
        "/customers",
        headers={
            "Authorization": "Bearer invalid_token"
        },
    )

    assert response.status_code == 401

def test_get_customer_not_found(
    client,
    auth_headers,
):
    response = client.get(
        "/customers/999999",
        headers=auth_headers,
    )

    # print(response.status_code)
    # print(response.json())

def test_update_customer_not_found(
    client,
    auth_headers,
    updated_customer_payload,
):
    response = client.put(
        "/customers/999999",
        json=updated_customer_payload,
        headers=auth_headers,
    )

    assert response.status_code == 404

def test_delete_customer_not_found(
    client,
    auth_headers,
):
    response = client.delete(
        "/customers/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404

def test_create_duplicate_email(
    client,
    auth_headers,
    created_customer,
):
    response = client.post(
        "/customers",
        json={
            "name": "Another User",
            "email": created_customer["email"],
            "phone": "9999999999",
        },
        headers=auth_headers,
    )

    assert response.status_code == 409

def test_create_customer_invalid_email(
    client,
    auth_headers,
):
    response = client.post(
        "/customers",
        json={
            "name": "John",
            "email": "not-an-email",
            "phone": "9876543210",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422

def test_create_customer_missing_name(
    client,
    auth_headers,
):
    response = client.post(
        "/customers",
        json={
            "email": "john@example.com",
            "phone": "9876543210",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422