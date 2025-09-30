from sqlalchemy.orm import Session
from database import SessionLocal
from models import Assignment, Hint

def add_hints():
    db = SessionLocal()
    
    try:
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
        
        # Получаем все задания
        all_assignments = db.query(Assignment).all()
        
        added_count = 0
        for assignment in all_assignments:
            if assignment.title in hints_by_title:
                # Проверяем, есть ли уже подсказки для этого задания
                existing_hints_count = db.query(Hint).filter(Hint.assignment_id == assignment.id).count()
                
                if existing_hints_count > 0:
                    print(f"Задание '{assignment.title}' уже имеет {existing_hints_count} подсказок, пропускаем...")
                    continue
                
                hints_data = hints_by_title[assignment.title]
                for hint_data in hints_data:
                    hint = Hint(
                        assignment_id=assignment.id,
                        order_index=hint_data["order_index"],
                        text=hint_data["text"],
                        penalty=hint_data["penalty"]
                    )
                    db.add(hint)
                    added_count += 1
                
                print(f"Добавлено {len(hints_data)} подсказок для задания '{assignment.title}'")
        
        db.commit()
        print(f"\nВсего добавлено {added_count} новых подсказок!")
        
    except Exception as e:
        print(f"Ошибка при добавлении подсказок: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_hints()
