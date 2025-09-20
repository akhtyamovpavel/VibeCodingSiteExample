from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import courses, topics, assignments

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vibe Coding Course", version="1.0.0")

# Настройка CORS для работы с React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(courses.router, prefix="/api/courses", tags=["courses"])
app.include_router(topics.router, prefix="/api/topics", tags=["topics"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["assignments"])

@app.get("/")
async def root():
    return {"status": "ok", "message": "Vibe Coding API", "docs": "/docs"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Vibe Coding API is running"}
