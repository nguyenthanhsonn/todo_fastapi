# Todo List API (FastAPI Production-Ready)

Một API quản lý Todo List được phát triển với FastAPI, tuân thủ đầy đủ các chuẩn mực sản xuất (Production-Ready Architecture).

## Tính Năng Nổi Bật

- **FastAPI Modern Architecture**: Phân tách rõ ràng giữa Core, Config, Database, Models, Services, Dependencies và Routers.
- **Annotated Style**: Áp dụng `typing.Annotated` cho Parameter, Path, Query và Dependency Injections.
- **SQLModel ORM**: Làm việc linh hoạt với SQLite (Development) và MySQL/PostgreSQL (Production).
- **Pydantic Settings**: Quản lý cấu hình tập trung và an toàn từ tệp `.env`.
- **Global Exception Handling**: Trả về thông báo lỗi chuẩn định dạng JSON.
- **Testing Suite**: Tích hợp sẵn `pytest` và `httpx`.

## Cấu Trúc Thư Mục

```text
app/
  api/v1/       # API routers/controllers
  core/         # Exception handlers, logging, security/core concerns
  models/       # SQLModel ORM entities/database tables
  schemas/      # DTO/request-response schemas
  services/     # Business logic
  config.py     # Application settings
  database.py   # Engine, session, database initialization
  dependencies.py
  main.py
```

## Hướng Dẫn Chạy Cục Bộ

1. **Khởi tạo môi trường ảo và cài đặt**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

2. **Chạy ứng dụng trong chế độ Development**:
   ```bash
   fastapi dev
   ```

3. **Truy cập tài liệu API**:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

4. **Chạy Kiểm Thử (Tests)**:
   ```bash
   pytest -v
   ```
