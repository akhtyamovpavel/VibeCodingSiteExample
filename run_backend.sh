#!/bin/bash

# Скрипт для запуска FastAPI backend

echo "🚀 Запуск Vibe Coding Backend..."

# Переходим в директорию backend
cd backend

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Гарантируем наличие pip внутри venv (fallback на get-pip.py если ensurepip недоступен)
echo "🧰 Проверка pip в venv..."
if ! command -v pip >/dev/null 2>&1; then
    echo "📥 Установка pip в venv..."
    python -m ensurepip --upgrade 2>/dev/null || {
        echo "⚠️ ensurepip недоступен, использую get-pip.py";
        curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && python /tmp/get-pip.py;
    }
fi

echo "⬆️ Обновление pip/setuptools/wheel..."
python -m pip install -U pip setuptools wheel

# Устанавливаем зависимости проекта
echo "📥 Установка зависимостей проекта..."
python -m pip install -r ../requirements.txt

# Запускаем миграции Alembic
echo "🧬 Применение миграций Alembic..."
alembic upgrade head || {
  echo "⚙️  Инициализация alembic...";
  alembic init alembic 2>/dev/null || true;
  alembic upgrade head || true;
}

# Инициализируем/досеваем данные
echo "🗄️ Инициализация и наполнение базы..."
python init_db.py

# Запускаем сервер
echo "🌟 Запуск FastAPI сервера..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

