from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Course, Topic, Assignment, Hint

# Создаем все таблицы
Base.metadata.create_all(bind=engine)

def init_data():
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже данные
        if db.query(Course).first():
            print("Данные уже существуют в базе")
            return
        
        # Создаем курс по Vibe Coding
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
            difficulty_level="intermediate"
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        
        # Создаем темы курса
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
                "duration_minutes": 60
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
                "duration_minutes": 120
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
                "duration_minutes": 150
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
                "duration_minutes": 180
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
                "duration_minutes": 120
            }
        ]
        
        for topic_data in topics_data:
            topic = Topic(
                course_id=course.id,
                **topic_data
            )
            db.add(topic)
        
        db.commit()
        
        # Получаем созданные темы для создания заданий
        topics = db.query(Topic).filter(Topic.course_id == course.id).all()
        
        # Создаем задания для каждой темы
        assignments_data = [
            # Задания для темы 1
            {
                "topic_id": topics[0].id,
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
                "is_required": True
            },
            {
                "topic_id": topics[0].id,
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
                "is_required": False
            },
            # Задания для темы 2
            {
                "topic_id": topics[1].id,
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
                "is_required": True
            },
            {
                "topic_id": topics[1].id,
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
                "is_required": True
            },
            # Задания для темы 3
            {
                "topic_id": topics[2].id,
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
                "is_required": True
            },
            {
                "topic_id": topics[2].id,
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
                "is_required": False
            },
            # Задания для темы 4
            {
                "topic_id": topics[3].id,
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
                "is_required": True
            },
            # Задания для темы 5
            {
                "topic_id": topics[4].id,
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
                "is_required": True
            }
        ]
        
        for assignment_data in assignments_data:
            assignment = Assignment(**assignment_data)
            db.add(assignment)
        
        db.commit()

        # Создаем подсказки для всех заданий
        all_assignments = db.query(Assignment).all()
        
        # Словарь с подсказками для каждого задания
        hints_by_title = {
            "Настройка рабочего окружения": [
                {"order_index": 0, "text": "Начните с установки Python и Node.js подходящих версий.", "penalty": 10},
                {"order_index": 1, "text": "Создайте venv и установите FastAPI/uvicorn в изолированное окружение.", "penalty": 10},
                {"order_index": 2, "text": "Проверьте запуск простого FastAPI и React приложения.", "penalty": 10},
            ],
            "Исследование Vibe Coding": [
                {"order_index": 0, "text": "Сформулируйте 3-5 принципов Vibe Coding своими словами.", "penalty": 10},
                {"order_index": 1, "text": "Подберите примеры с сильным UX: подумайте о навигации и скорости.", "penalty": 10},
                {"order_index": 2, "text": "Оформите выводы в краткой структуре: проблема → решение → эффект.", "penalty": 10},
            ],
            "Создание первого API": [
                {"order_index": 0, "text": "Начните с простого FastAPI приложения с одним GET endpoint.", "penalty": 10},
                {"order_index": 1, "text": "Используйте Pydantic BaseModel для валидации входных данных.", "penalty": 10},
                {"order_index": 2, "text": "Добавьте HTTPException для обработки ошибок с правильными кодами.", "penalty": 10},
                {"order_index": 3, "text": "Проверьте автоматическую документацию на /docs.", "penalty": 10},
            ],
            "Интеграция с базой данных": [
                {"order_index": 0, "text": "Создайте модели SQLAlchemy с правильными типами полей.", "penalty": 10},
                {"order_index": 1, "text": "Используйте Depends(get_db) для получения сессии БД.", "penalty": 10},
                {"order_index": 2, "text": "Не забудьте вызывать db.commit() после изменений и db.refresh() для обновления объекта.", "penalty": 10},
                {"order_index": 3, "text": "Используйте alembic для создания и применения миграций.", "penalty": 10},
            ],
            "Создание React приложения": [
                {"order_index": 0, "text": "Используйте функциональные компоненты с хуками вместо классовых.", "penalty": 10},
                {"order_index": 1, "text": "Разделите UI на переиспользуемые компоненты (Button, Card, Input).", "penalty": 10},
                {"order_index": 2, "text": "Для роутинга используйте react-router-dom с BrowserRouter.", "penalty": 10},
                {"order_index": 3, "text": "Валидируйте формы с помощью состояния и отображайте ошибки пользователю.", "penalty": 10},
            ],
            "Управление состоянием": [
                {"order_index": 0, "text": "Создайте Context для глобального состояния, которое используется в нескольких компонентах.", "penalty": 10},
                {"order_index": 1, "text": "Используйте useCallback и useMemo для оптимизации перерисовок.", "penalty": 10},
                {"order_index": 2, "text": "Вынесите логику работы с состоянием в кастомные хуки (useAuth, useForm).", "penalty": 10},
                {"order_index": 3, "text": "Очищайте эффекты с помощью return в useEffect, особенно для таймеров и подписок.", "penalty": 10},
            ],
            "Полная интеграция": [
                {"order_index": 0, "text": "Используйте axios для работы с API и создайте базовый instance с настройками.", "penalty": 10},
                {"order_index": 1, "text": "Реализуйте состояния loading, error и success для каждого запроса.", "penalty": 10},
                {"order_index": 2, "text": "Для аутентификации храните токен в localStorage и добавляйте в headers.", "penalty": 10},
                {"order_index": 3, "text": "Настройте CORS в FastAPI, разрешив origin фронтенда.", "penalty": 10},
                {"order_index": 4, "text": "Добавьте axios interceptors для автоматической обработки ошибок 401.", "penalty": 10},
            ],
            "Деплой и мониторинг": [
                {"order_index": 0, "text": "Создайте Dockerfile для фронтенда и бэкенда отдельно.", "penalty": 10},
                {"order_index": 1, "text": "Используйте docker-compose для локального запуска всех сервисов.", "penalty": 10},
                {"order_index": 2, "text": "Настройте GitHub Actions для автоматического деплоя при push в main.", "penalty": 10},
                {"order_index": 3, "text": "Добавьте healthcheck endpoints и используйте их для мониторинга.", "penalty": 10},
                {"order_index": 4, "text": "Создайте README с инструкциями по локальному запуску и деплою.", "penalty": 10},
            ],
        }
        
        for assignment in all_assignments:
            if assignment.title in hints_by_title:
                hints_data = hints_by_title[assignment.title]
                for hint_data in hints_data:
                    hint = Hint(
                        assignment_id=assignment.id,
                        order_index=hint_data["order_index"],
                        text=hint_data["text"],
                        penalty=hint_data["penalty"]
                    )
                    db.add(hint)
        
        db.commit()
        print("Тестовые данные успешно созданы!")
        
    except Exception as e:
        print(f"Ошибка при создании данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_data()
