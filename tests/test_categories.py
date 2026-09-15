import uuid
from fastapi.testclient import TestClient


def get_auth_token(client: TestClient) -> str:
    """Helper tao user moi va lay JWT Token cho category tests."""
    email = f"cat_tester_{uuid.uuid4().hex[:6]}@gmail.com"
    reg_payload = {
        "name": "Category Tester",
        "email": email,
        "password": "password123",
    }
    client.post("/api/v1/auth/register", json=reg_payload)
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": "password123"})
    return login_res.json()["data"]["accessToken"]


def test_create_category(client: TestClient) -> None:
    """Kiem thu tao Category cho nguoi dung."""
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_res = client.post(
        "/api/v1/categories",
        json={"name": "Cong viec quan trong", "color": "#FF0000", "icon": "star"},
        headers=headers,
    )
    assert create_res.status_code == 201
    cat_data = create_res.json()["data"]
    assert cat_data["name"] == "Cong viec quan trong"
