from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:  # Support both package and direct script execution
    from .database import engine, Base
    from .routers import courses, topics, assignments
    from .init_db import init_data
except ImportError:  # pragma: no cover - fallback when run as script
    from database import engine, Base
    from routers import courses, topics, assignments
    from init_db import init_data

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vibe Coding Course", version="1.0.0")

# Настройка CORS для работы с React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],  # React dev server (localhost and 127.0.0.1)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(courses.router, prefix="/api/courses", tags=["courses"])
app.include_router(topics.router, prefix="/api/topics", tags=["topics"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["assignments"])


@app.on_event("startup")
def ensure_seed_data() -> None:
    """Populate the SQLite database with demo content when it's empty."""
    try:
        init_data()
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f"❌ Не удалось инициализировать тестовые данные: {exc}")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Vibe Coding API", "docs": "/docs"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Vibe Coding API is running"}
