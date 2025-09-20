# Vibe Coding Course Website

Современный веб-сайт курса по Vibe Coding, построенный на FastAPI + React.

## 🚀 Особенности

- **Backend**: FastAPI с SQLite базой данных
- **Frontend**: React с современным UI/UX
- **База данных**: SQLite с миграциями Alembic
- **API**: RESTful API с полной документацией
- **Дизайн**: Адаптивный дизайн с градиентами и анимациями

## 📋 Страницы

1. **Главная** - Обзор курса и призыв к действию
2. **О курсе** - Подробное описание курса и статистика
3. **Темы** - Список всех тем курса с содержанием
4. **Задания** - Практические задания для закрепления

## 🛠️ Установка и запуск

### Предварительные требования

- Python 3.8+
- Node.js 16+
- npm

### Быстрый старт

1. **Клонируйте репозиторий**
   ```bash
   git clone <repository-url>
   cd Vibe
   ```

2. **Запустите Backend (в отдельном терминале)**
   ```bash
   chmod +x run_backend.sh
   ./run_backend.sh
   ```
   Backend будет доступен по адресу: http://localhost:8000

3. **Запустите Frontend (в отдельном терминале)**
   ```bash
   chmod +x run_frontend.sh
   ./run_frontend.sh
   ```
   Frontend будет доступен по адресу: http://localhost:3000

### Ручная установка

#### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r ../requirements.txt
python init_db.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## 📊 Структура проекта

```
Vibe/
├── backend/
│   ├── main.py              # Основной файл FastAPI
│   ├── database.py          # Настройка базы данных
│   ├── models.py            # SQLAlchemy модели
│   ├── schemas.py           # Pydantic схемы
│   ├── routers/             # API роутеры
│   │   ├── courses.py
│   │   ├── topics.py
│   │   └── assignments.py
│   ├── alembic/             # Миграции базы данных
│   └── init_db.py           # Инициализация с тестовыми данными
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React компоненты
│   │   ├── pages/           # Страницы приложения
│   │   └── App.js           # Главный компонент
│   └── package.json
├── requirements.txt         # Python зависимости
├── run_backend.sh          # Скрипт запуска backend
├── run_frontend.sh         # Скрипт запуска frontend
└── README.md
```

## 🗄️ База данных

Проект использует SQLite с тремя основными таблицами:

- **courses** - Курсы
- **topics** - Темы курсов
- **assignments** - Домашние задания

### Миграции

Для создания миграций:
```bash
cd backend
alembic revision --autogenerate -m "Описание изменений"
alembic upgrade head
```

## 🔌 API Endpoints

### Курсы
- `GET /api/courses/` - Список всех курсов
- `GET /api/courses/{id}` - Получить курс по ID
- `POST /api/courses/` - Создать новый курс
- `PUT /api/courses/{id}` - Обновить курс
- `DELETE /api/courses/{id}` - Удалить курс

### Темы
- `GET /api/topics/` - Список всех тем
- `GET /api/topics/course/{course_id}` - Темы по курсу
- `GET /api/topics/{id}` - Получить тему по ID
- `POST /api/topics/` - Создать новую тему
- `PUT /api/topics/{id}` - Обновить тему
- `DELETE /api/topics/{id}` - Удалить тему

### Задания
- `GET /api/assignments/` - Список всех заданий
- `GET /api/assignments/topic/{topic_id}` - Задания по теме
- `GET /api/assignments/{id}` - Получить задание по ID
- `POST /api/assignments/` - Создать новое задание
- `PUT /api/assignments/{id}` - Обновить задание
- `DELETE /api/assignments/{id}` - Удалить задание

## 🎨 Дизайн

Проект использует современный дизайн с:
- Градиентными фонами
- Плавными анимациями
- Адаптивной версткой
- Интуитивным UX

## 📝 Тестовые данные

При первом запуске автоматически создаются тестовые данные:
- 1 курс "Vibe Coding: Современная разработка с душой"
- 5 тем курса
- 8 практических заданий

## 🔧 Разработка

### Добавление новых страниц

1. Создайте компонент в `frontend/src/pages/`
2. Добавьте роут в `frontend/src/App.js`
3. Обновите навигацию в `frontend/src/components/Navbar.js`

### Добавление новых API endpoints

1. Создайте роутер в `backend/routers/`
2. Добавьте модели в `backend/models.py`
3. Создайте схемы в `backend/schemas.py`
4. Подключите роутер в `backend/main.py`

## 📄 Лицензия

MIT License

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature branch
3. Commit изменения
4. Push в branch
5. Создайте Pull Request

---

**Vibe Coding** - Создавайте код с душой! 💜

