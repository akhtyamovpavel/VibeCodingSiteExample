from collections import defaultdict
from typing import List

from sqlalchemy.orm import Session

try:  # Support running as a module or standalone script
    from .database import SessionLocal, engine
    from .models import Base, Course, Topic, Assignment, Hint
except ImportError:  # pragma: no cover - fallback when executed directly
    from database import SessionLocal, engine
    from models import Base, Course, Topic, Assignment, Hint

# Создаем все таблицы
Base.metadata.create_all(bind=engine)

EXPECTED_TOPICS = 5
EXPECTED_ASSIGNMENTS = 8


def seed_course_data(db: Session) -> None:
    """Создает базовый курс вместе с темами, заданиями и подсказками."""
    course = Course(
        title="Vibe Coding: Современная разработка с душой",
        description="""
        Добро пожаловать в мир Vibe Coding! Этот курс научит вас не просто писать код,
        а создавать приложения с душой и характером. Мы изучим современные технологии,
        лучшие практики разработки и научимся создавать проекты, которые вдохновляют.

        В этом курсе вы:
        - Изучите основы современной веб-разработки
        - Научитесь работать с React и FastAPI
        - Поймете принципы чистой архитектуры
        - Создадите полноценное приложение
        - Получите навыки работы в команде
        """,
        duration_hours=40,
        difficulty_level="intermediate",
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    topics_data = [
        {
            "title": "Введение в Vibe Coding",
            "description": "Понимание философии Vibe Coding и современной разработки",
            "content": """
            Vibe Coding - это не просто написание кода, это создание цифрового опыта,
            который трогает сердца пользователей. В этой теме мы разберем:

            1. Что такое Vibe Coding и почему это важно
            2. Принципы современной разработки
            3. Инструменты и технологии, которые мы будем использовать
            4. Настройка рабочего окружения

            К концу этой темы вы поймете, что делает код не просто функциональным,
            а по-настоящему вдохновляющим.
            """,
            "order_index": 1,
            "duration_minutes": 60,
        },
        {
            "title": "Основы FastAPI и Python",
            "description": "Создание мощного backend с помощью FastAPI",
            "content": """
            FastAPI - это современный фреймворк для создания API на Python.
            В этой теме мы изучим:

            1. Основы FastAPI и его преимущества
            2. Создание API endpoints
            3. Работа с базами данных (SQLAlchemy)
            4. Валидация данных с Pydantic
            5. Документация API (Swagger/OpenAPI)
            6. Обработка ошибок и middleware

            Вы создадите свой первый API и поймете, как строить масштабируемые backend-системы.
            """,
            "order_index": 2,
            "duration_minutes": 120,
        },
        {
            "title": "React и современный Frontend",
            "description": "Создание интерактивных пользовательских интерфейсов",
            "content": """
            React изменил мир frontend-разработки. В этой теме мы изучим:

            1. Основы React и JSX
            2. Компоненты и их жизненный цикл
            3. Hooks (useState, useEffect, useContext)
            4. Управление состоянием
            5. Роутинг с React Router
            6. Стилизация (CSS Modules, Styled Components)
            7. Работа с API

            Вы создадите современный, отзывчивый интерфейс для вашего приложения.
            """,
            "order_index": 3,
            "duration_minutes": 150,
        },
        {
            "title": "Интеграция Frontend и Backend",
            "description": "Соединение всех частей в единое приложение",
            "content": """
            Теперь пришло время соединить все части воедино:

            1. Настройка CORS и взаимодействие с API
            2. Обработка состояний загрузки и ошибок
            3. Аутентификация и авторизация
            4. Оптимизация производительности
            5. Тестирование интеграции
            6. Деплой приложения

            Вы создадите полноценное приложение, готовое к продакшену.
            """,
            "order_index": 4,
            "duration_minutes": 180,
        },
        {
            "title": "Продвинутые техники и лучшие практики",
            "description": "Углубленное изучение современных подходов к разработке",
            "content": """
            В финальной теме мы изучим продвинутые техники:

            1. Микросервисная архитектура
            2. Контейнеризация с Docker
            3. CI/CD пайплайны
            4. Мониторинг и логирование
            5. Безопасность приложений
            6. Оптимизация и масштабирование
            7. Работа в команде и code review

            Вы станете настоящим Vibe Coder, готовым к любым вызовам!
            """,
            "order_index": 5,
            "duration_minutes": 120,
        },
    ]

    for topic_data in topics_data:
        db.add(Topic(course_id=course.id, **topic_data))

    db.commit()

    topics = (
        db.query(Topic)
        .filter(Topic.course_id == course.id)
        .order_by(Topic.order_index.asc(), Topic.id.asc())
        .all()
    )
    topics_by_order = {topic.order_index: topic for topic in topics}

    assignments_data = [
        {
            "topic_order": 1,
            "title": "Настройка рабочего окружения",
            "description": "Настройте ваше рабочее окружение для Vibe Coding",
            "instructions": """
            1. Установите Python 3.8+ и Node.js 16+
            2. Создайте виртуальное окружение Python
            3. Установите необходимые пакеты (FastAPI, React)
            4. Настройте IDE (VS Code с расширениями)
            5. Создайте первый проект и запустите его

            Результат: Рабочее окружение готово к разработке
            """,
            "difficulty_level": "easy",
            "estimated_hours": 2,
            "is_required": True,
        },
        {
            "topic_order": 1,
            "title": "Исследование Vibe Coding",
            "description": "Изучите концепцию Vibe Coding и найдите примеры",
            "instructions": """
            1. Изучите принципы Vibe Coding
            2. Найдите 3 приложения с отличным UX/UI
            3. Проанализируйте, что делает их особенными
            4. Создайте презентацию с вашими находками

            Результат: Презентация с анализом примеров
            """,
            "difficulty_level": "medium",
            "estimated_hours": 3,
            "is_required": False,
        },
        {
            "topic_order": 2,
            "title": "Создание первого API",
            "description": "Создайте простое API с FastAPI",
            "instructions": """
            1. Создайте FastAPI приложение
            2. Добавьте несколько endpoints (GET, POST, PUT, DELETE)
            3. Используйте Pydantic для валидации
            4. Добавьте обработку ошибок
            5. Создайте документацию API

            Результат: Рабочее API с документацией
            """,
            "difficulty_level": "medium",
            "estimated_hours": 4,
            "is_required": True,
        },
        {
            "topic_order": 2,
            "title": "Интеграция с базой данных",
            "description": "Подключите SQLAlchemy к вашему API",
            "instructions": """
            1. Настройте SQLAlchemy с SQLite
            2. Создайте модели данных
            3. Добавьте CRUD операции
            4. Создайте миграции
            5. Протестируйте все операции

            Результат: API с полной работой с БД
            """,
            "difficulty_level": "hard",
            "estimated_hours": 6,
            "is_required": True,
        },
        {
            "topic_order": 3,
            "title": "Создание React приложения",
            "description": "Создайте базовое React приложение",
            "instructions": """
            1. Создайте React приложение с Create React App
            2. Создайте несколько компонентов
            3. Настройте роутинг
            4. Добавьте стили
            5. Создайте форму с валидацией

            Результат: Базовое React приложение
            """,
            "difficulty_level": "medium",
            "estimated_hours": 5,
            "is_required": True,
        },
        {
            "topic_order": 3,
            "title": "Управление состоянием",
            "description": "Реализуйте сложное управление состоянием",
            "instructions": """
            1. Используйте Context API для глобального состояния
            2. Реализуйте локальное состояние с useState
            3. Добавьте side effects с useEffect
            4. Создайте кастомные хуки
            5. Оптимизируйте производительность

            Результат: Приложение с продуманным управлением состоянием
            """,
            "difficulty_level": "hard",
            "estimated_hours": 8,
            "is_required": False,
        },
        {
            "topic_order": 4,
            "title": "Полная интеграция",
            "description": "Соедините Frontend и Backend",
            "instructions": """
            1. Настройте взаимодействие с API
            2. Реализуйте аутентификацию
            3. Добавьте обработку ошибок
            4. Создайте loading состояния
            5. Оптимизируйте UX

            Результат: Полноценное приложение
            """,
            "difficulty_level": "hard",
            "estimated_hours": 10,
            "is_required": True,
        },
        {
            "topic_order": 5,
            "title": "Деплой и мониторинг",
            "description": "Разверните приложение в продакшене",
            "instructions": """
            1. Контейнеризуйте приложение с Docker
            2. Настройте CI/CD пайплайн
            3. Разверните на облачной платформе
            4. Настройте мониторинг
            5. Создайте документацию

            Результат: Приложение в продакшене
            """,
            "difficulty_level": "hard",
            "estimated_hours": 12,
            "is_required": True,
        },
    ]

    for assignment_data in assignments_data:
        topic_order = assignment_data["topic_order"]
        topic = topics_by_order.get(topic_order)
        if topic is None:
            raise ValueError(f"Не найдена тема с order_index={topic_order} для задания '{assignment_data['title']}'")
        payload = {k: v for k, v in assignment_data.items() if k != "topic_order"}
        db.add(Assignment(topic_id=topic.id, **payload))

    db.commit()

    assignments = {
        assignment.title: assignment
        for assignment in db.query(Assignment)
        .filter(Assignment.topic_id.in_([topic.id for topic in topics]))
        .all()
    }

    first_assignment = assignments.get("Настройка рабочего окружения")
    second_assignment = assignments.get("Исследование Vibe Coding")

    if first_assignment:
        hints_data = [
            {
                "assignment_id": first_assignment.id,
                "order_index": 0,
                "text": "Начните с установки Python и Node.js подходящих версий.",
                "penalty": 10,
            },
            {
                "assignment_id": first_assignment.id,
                "order_index": 1,
                "text": "Создайте venv и установите FastAPI/uvicorn в изолированное окружение.",
                "penalty": 10,
            },
            {
                "assignment_id": first_assignment.id,
                "order_index": 2,
                "text": "Проверьте запуск простого FastAPI и React приложения.",
                "penalty": 10,
            },
        ]
        for hint_data in hints_data:
            db.add(Hint(**hint_data))

    if second_assignment:
        hints_data2 = [
            {
                "assignment_id": second_assignment.id,
                "order_index": 0,
                "text": "Сформулируйте 3-5 принципов Vibe Coding своими словами.",
                "penalty": 10,
            },
            {
                "assignment_id": second_assignment.id,
                "order_index": 1,
                "text": "Подберите примеры с сильным UX: подумайте о навигации и скорости.",
                "penalty": 10,
            },
            {
                "assignment_id": second_assignment.id,
                "order_index": 2,
                "text": "Оформите выводы в краткой структуре: проблема → решение → эффект.",
                "penalty": 10,
            },
        ]
        for hint_data in hints_data2:
            db.add(Hint(**hint_data))

    db.commit()


def validate_data(db: Session) -> None:
    """Проверяет, что тестовые данные заполнены корректно."""
    errors: List[str] = []

    courses = db.query(Course).all()
    topics = db.query(Topic).order_by(Topic.order_index.asc()).all()
    assignments = db.query(Assignment).all()
    hints = db.query(Hint).all()

    if not courses:
        errors.append("В базе отсутствуют курсы")
    if len(courses) != 1:
        errors.append(f"Ожидался 1 курс, найдено {len(courses)}")

    course_ids = {course.id for course in courses}

    if len(topics) != EXPECTED_TOPICS:
        errors.append(f"Ожидалось {EXPECTED_TOPICS} тем, найдено {len(topics)}")

    topic_ids = {topic.id for topic in topics}
    topics_by_course = defaultdict(list)
    for topic in topics:
        if topic.course_id not in course_ids:
            errors.append(f"Тема '{topic.title}' ссылается на несуществующий курс ({topic.course_id})")
        topics_by_course[topic.course_id].append(topic.order_index)

    for course_id, orders in topics_by_course.items():
        if len(orders) != len(set(orders)):
            errors.append(f"Курс {course_id} содержит темы с повторяющимися order_index")
        expected_orders = list(range(1, len(orders) + 1))
        if sorted(orders) != expected_orders:
            errors.append(f"Для курса {course_id} порядок тем должен быть последовательным от 1 до {len(orders)}")

    if len(assignments) != EXPECTED_ASSIGNMENTS:
        errors.append(f"Ожидалось {EXPECTED_ASSIGNMENTS} заданий, найдено {len(assignments)}")

    assignment_ids = {assignment.id for assignment in assignments}
    assignments_by_topic = defaultdict(list)
    for assignment in assignments:
        if assignment.topic_id not in topic_ids:
            errors.append(f"Задание '{assignment.title}' ссылается на отсутствующую тему ({assignment.topic_id})")
        if assignment.estimated_hours <= 0:
            errors.append(f"У задания '{assignment.title}' должно быть положительное количество часов")
        assignments_by_topic[assignment.topic_id].append(assignment)

    for topic in topics:
        if not assignments_by_topic.get(topic.id):
            errors.append(f"У темы '{topic.title}' отсутствуют задания")

    hints_by_assignment = defaultdict(list)
    for hint in hints:
        if hint.assignment_id not in assignment_ids:
            errors.append(f"Подсказка {hint.id} ссылается на несуществующее задание ({hint.assignment_id})")
        hints_by_assignment[hint.assignment_id].append(hint.order_index)

    for assignment_id, orders in hints_by_assignment.items():
        sorted_orders = sorted(orders)
        if sorted_orders != list(range(len(sorted_orders))):
            errors.append(
                "Порядковые номера подсказок для задания "
                f"{assignment_id} должны быть последовательными от 0 без пропусков"
            )

    if errors:
        error_text = "\n - ".join(errors)
        raise ValueError(f"Обнаружены проблемы с тестовыми данными:\n - {error_text}")

    print(
        "✔️ Консистентность данных подтверждена."
        f" Курсы: {len(courses)}, темы: {len(topics)}, задания: {len(assignments)}, подсказки: {len(hints)}."
    )


def init_data() -> None:
    db = SessionLocal()
    try:
        created = False
        if not db.query(Course).first():
            print("🌱 Данные не найдены — создаю тестовый набор...")
            seed_course_data(db)
            created = True
        else:
            print("ℹ️ Данные уже присутствуют, выполняю проверку...")

        validate_data(db)
        if created:
            print("✅ Тестовые данные успешно созданы и проверены!")
        else:
            print("✅ Существующие данные прошли проверку консистентности.")

    except Exception as exc:
        db.rollback()
        print(f"❌ Ошибка при инициализации базы: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_data()
