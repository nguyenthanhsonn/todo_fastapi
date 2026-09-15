from fastapi.testclient import TestClient


def test_register_user_success(client: TestClient) -> None:
    """Test Case 1: Đăng ký tài khoản thành công."""
    payload = {
        "name": "Nguyen Van A",
        "email": "nguyenvana@gmail.com",
        "password": "secretpassword123",
    }
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 201
    res_json = response.json()

    # Kiểm tra chuẩn cấu trúc Success Response
    assert res_json["success"] is True
    assert "data" in res_json
    assert res_json["data"]["name"] == "Nguyen Van A"
    assert res_json["data"]["email"] == "nguyenvana@gmail.com"
    assert "id" in res_json["data"]
    # Đảm bảo KHÔNG lộ mật khẩu trong response
    assert "password" not in res_json["data"]
    assert "password_hash" not in res_json["data"]


def test_register_user_duplicate_email(client: TestClient) -> None:
    """Test Case 2: Đăng ký tài khoản với email đã tồn tại (Lỗi 409 DUPLICATE_ERROR)."""
    payload = {
        "name": "Nguyen Van A",
        "email": "duplicate@gmail.com",
        "password": "secretpassword123",
    }
    # Lần 1: Tạo mới thành công
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    # Lần 2: Trùng email -> Bắt lỗi 409
    res2 = client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 409
    res_json = res2.json()

    # Kiểm tra chuẩn cấu trúc Error Response
    assert res_json["success"] is False
    assert res_json["error"]["code"] == "DUPLICATE_ERROR"
    assert "already exists" in res_json["error"]["message"].lower()


def test_register_user_validation_error(client: TestClient) -> None:
    """Test Case 3: Đăng ký sai định dạng dữ liệu (Lỗi 422 VALIDATION_ERROR)."""
    invalid_payload = {
        "name": "Nguyen Van B",
        "email": "not-an-email",
    }
    response = client.post("/api/v1/auth/register", json=invalid_payload)

    assert response.status_code == 422
    res_json = response.json()

    assert res_json["success"] is False
    assert res_json["error"]["code"] == "VALIDATION_ERROR"
    assert "fields" in res_json["error"]
    assert "email" in res_json["error"]["fields"]
    assert "password" in res_json["error"]["fields"]


def test_register_user_non_gmail_validation_error(client: TestClient) -> None:
    """Test Case 4: Đăng ký email không phải đuôi @gmail.com (Lỗi 422 VALIDATION_ERROR)."""
    invalid_payload = {
        "name": "Nguyen Van C",
        "email": "user@otherdomain.com",
        "password": "secretpassword123",
    }
    response = client.post("/api/v1/auth/register", json=invalid_payload)

    assert response.status_code == 422
    res_json = response.json()

    assert res_json["success"] is False
    assert res_json["error"]["code"] == "VALIDATION_ERROR"
    assert "fields" in res_json["error"]
    assert "email" in res_json["error"]["fields"]


def test_login_user_success(client: TestClient) -> None:
    """Test Case 5: Đăng nhập thành công trả về UserRead và JWT accessToken."""
    reg_payload = {
        "name": "Nguyen Van D",
        "email": "nguyenvand@gmail.com",
        "password": "secretpassword123",
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "email": "nguyenvand@gmail.com",
        "password": "secretpassword123",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    res_json = response.json()

    assert res_json["success"] is True
    assert "user" in res_json["data"]
    assert res_json["data"]["user"]["email"] == "nguyenvand@gmail.com"
    assert "accessToken" in res_json["data"]
    assert len(res_json["data"]["accessToken"]) > 10


def test_login_user_invalid_credentials(client: TestClient) -> None:
    """Test Case 6: Đăng nhập sai thông tin trả về 401 UNAUTHORIZED."""
    login_payload = {
        "email": "nonexistent@gmail.com",
        "password": "wrongpassword",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    res_json = response.json()

    assert res_json["success"] is False
    assert res_json["error"]["code"] == "UNAUTHORIZED"


def test_logout_user_success(client: TestClient) -> None:
    """Test Case 7: Đăng xuất tài khoản thành công."""
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    res_json = response.json()

    assert res_json["success"] is True
    assert "message" in res_json["data"]
    assert "logged out" in res_json["data"]["message"].lower()


def test_get_profile_me_success(client: TestClient) -> None:
    """Test Case 8: Lấy thông tin profile người dùng hiện tại bằng Bearer token."""
    reg_payload = {
        "name": "Nguyen Van E",
        "email": "nguyenvane@gmail.com",
        "password": "secretpassword123",
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_res = client.post("/api/v1/auth/login", json={"email": "nguyenvane@gmail.com", "password": "secretpassword123"})
    token = login_res.json()["data"]["accessToken"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    res_json = response.json()

    assert res_json["success"] is True
    assert res_json["data"]["email"] == "nguyenvane@gmail.com"
    assert res_json["data"]["name"] == "Nguyen Van E"


def test_get_profile_me_unauthorized(client: TestClient) -> None:
    """Test Case 9: Gọi API /me với token sai hoặc không hợp lệ trả về 401."""
    response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid_token_xyz"})
    assert response.status_code == 401
    res_json = response.json()

    assert res_json["success"] is False
    assert res_json["error"]["code"] == "UNAUTHORIZED"
