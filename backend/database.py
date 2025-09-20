from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

"""Конфигурация подключения к SQLite.

Всегда используем абсолютный путь к файлу БД в корне проекта, чтобы
исключить рассинхронизацию при различной рабочей директории запуска
(корень проекта против каталога `backend`).
"""

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DB_FILE_PATH = os.path.join(PROJECT_ROOT, "vibe_coding.db")
DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Нужно для SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
