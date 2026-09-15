from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.core.exceptions import NotFoundError, register_exception_handlers
from app.schemas.response import SuccessResponse, success_response


class DummyCreate(BaseModel):
    title: str = Field(min_length=1)


dummy_router = APIRouter()


@dummy_router.get("/test-success", response_model=SuccessResponse[dict[str, str]])
def dummy_success():
    return success_response(data={"title": "My Task"}, meta={"page": 1, "total": 1})


@dummy_router.get("/test-not-found")
def dummy_not_found():
    raise NotFoundError(resource_name="Task", resource_id="123")


@dummy_router.post("/test-validation")
def dummy_validation(payload: DummyCreate):
    return success_response(data=payload)


def test_standard_success_response():
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(dummy_router)

    with TestClient(app) as test_client:
        res = test_client.get("/test-success")
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["data"] == {"title": "My Task"}
        assert data["meta"] == {"page": 1, "total": 1}


def test_standard_not_found_error_response():
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(dummy_router)

    with TestClient(app) as test_client:
        res = test_client.get("/test-not-found")
        assert res.status_code == 404
        data = res.json()
        assert data["success"] is False
        assert data["error"]["code"] == "NOT_FOUND"
        assert "Task with id '123' was not found" in data["error"]["message"]


def test_standard_validation_error_response():
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(dummy_router)

    with TestClient(app) as test_client:
        res = test_client.post("/test-validation", json={})
        assert res.status_code == 422
        data = res.json()
        assert data["success"] is False
        assert data["error"]["code"] == "VALIDATION_ERROR"
        assert "title" in data["error"]["fields"]
        assert data["error"]["fields"]["title"] == "Required"
