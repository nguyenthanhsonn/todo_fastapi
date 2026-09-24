import uuid
from fastapi.testclient import TestClient


def get_auth_token(client: TestClient) -> str:
    """Helper tao user moi va lay JWT token."""
    reg_payload = {
        "name": "Task Tester",
        "email": f"tasktester_{uuid.uuid4().hex[:6]}@gmail.com",
        "password": "secretpassword123",
    }
    client.post("/api/v1/auth/register", json=reg_payload)
    login_res = client.post("/api/v1/auth/login", json={"email": reg_payload["email"], "password": "secretpassword123"})
    return login_res.json()["data"]["accessToken"]


def test_crud_task_flow(client: TestClient) -> None:
    """Kiem thu full quy trinh CRUD Task."""
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Tao task
    create_payload = {
        "title": "Hoc FastAPI Production",
        "notes": "Viet CRUD Task",
        "priority": "high",
        "status": "todo",
    }
    res = client.post("/api/v1/tasks", json=create_payload, headers=headers)
    assert res.status_code == 201
    task_data = res.json()["data"]
    task_id = task_data["id"]
    assert task_data["status"] == "todo"

    # 2. List task
    list_res = client.get("/api/v1/tasks", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()["data"]) == 1
    assert list_res.json()["meta"]["total"] == 1

    # 3. Get task by ID
    get_res = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["data"]["id"] == task_id

    # 4. Update status to in_progress & in_review
    update_status_res = client.patch(f"/api/v1/tasks/{task_id}", json={"status": "in_progress"}, headers=headers)
    assert update_status_res.status_code == 200
    assert update_status_res.json()["data"]["status"] == "in_progress"

    update_status_res2 = client.patch(f"/api/v1/tasks/{task_id}", json={"status": "in_review"}, headers=headers)
    assert update_status_res2.status_code == 200
    assert update_status_res2.json()["data"]["status"] == "in_review"

    # 5. Update task to completed / done
    update_res = client.patch(f"/api/v1/tasks/{task_id}", json={"is_completed": True}, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["data"]["is_completed"] is True
    assert update_res.json()["data"]["status"] == "done"

    # 6. Delete task
    del_res = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert del_res.status_code == 204

    # 7. Check 404 after delete
    get_404 = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert get_404.status_code == 404
