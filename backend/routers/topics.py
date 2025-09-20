from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
try:  # Prefer package-relative imports when available
    from ..database import get_db
    from ..models import Topic, Course
    from ..schemas import Topic as TopicSchema, TopicCreate, TopicUpdate, TopicWithAssignments
except ImportError:  # pragma: no cover - fallback for direct execution
    from database import get_db
    from models import Topic, Course
    from schemas import Topic as TopicSchema, TopicCreate, TopicUpdate, TopicWithAssignments
from typing import List

router = APIRouter()

@router.get("/", response_model=List[TopicSchema])
def get_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех тем"""
    topics = db.query(Topic).offset(skip).limit(limit).all()
    return topics

@router.get("/course/{course_id}", response_model=List[TopicWithAssignments])
def get_topics_by_course(course_id: int, db: Session = Depends(get_db)):
    """Получить темы по курсу"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    
    topics = db.query(Topic).filter(Topic.course_id == course_id).order_by(Topic.order_index).all()
    return topics

@router.get("/{topic_id}", response_model=TopicWithAssignments)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """Получить тему по ID с заданиями"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    return topic

@router.post("/", response_model=TopicSchema)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    """Создать новую тему"""
    # Проверяем, что курс существует
    course = db.query(Course).filter(Course.id == topic.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    
    db_topic = Topic(**topic.dict())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.put("/{topic_id}", response_model=TopicSchema)
def update_topic(topic_id: int, topic: TopicUpdate, db: Session = Depends(get_db)):
    """Обновить тему"""
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    
    update_data = topic.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_topic, field, value)
    
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.delete("/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    """Удалить тему"""
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    
    db.delete(db_topic)
    db.commit()
    return {"message": "Тема успешно удалена"}
