from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
try:  # Use relative imports when the package is available
    from ..database import get_db
    from ..models import Course
    from ..schemas import Course as CourseSchema, CourseCreate, CourseUpdate, CourseWithTopics
except ImportError:  # pragma: no cover - fallback for script execution
    from database import get_db
    from models import Course
    from schemas import Course as CourseSchema, CourseCreate, CourseUpdate, CourseWithTopics
from typing import List

router = APIRouter()

@router.get("/", response_model=List[CourseSchema])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех курсов"""
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.get("/{course_id}", response_model=CourseWithTopics)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Получить курс по ID с темами и заданиями"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    return course

@router.post("/", response_model=CourseSchema)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Создать новый курс"""
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.put("/{course_id}", response_model=CourseSchema)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    """Обновить курс"""
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    
    update_data = course.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Удалить курс"""
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    
    db.delete(db_course)
    db.commit()
    return {"message": "Курс успешно удален"}
