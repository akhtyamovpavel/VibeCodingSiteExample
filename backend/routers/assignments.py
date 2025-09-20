from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
try:  # Prefer package-relative imports when available
    from ..database import get_db
    from ..models import Assignment, Topic, Hint as HintModel
    from ..schemas import (
        Assignment as AssignmentSchema,
        AssignmentCreate,
        AssignmentUpdate,
        Hint as HintSchema,
    )
except ImportError:  # pragma: no cover - fallback for direct execution
    from database import get_db
    from models import Assignment, Topic, Hint as HintModel
    from schemas import Assignment as AssignmentSchema, AssignmentCreate, AssignmentUpdate, Hint as HintSchema
from typing import List

router = APIRouter()

@router.get("/", response_model=List[AssignmentSchema])
def get_assignments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех заданий"""
    assignments = db.query(Assignment).offset(skip).limit(limit).all()
    return assignments

@router.get("/topic/{topic_id}", response_model=List[AssignmentSchema])
def get_assignments_by_topic(topic_id: int, db: Session = Depends(get_db)):
    """Получить задания по теме"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    
    assignments = db.query(Assignment).filter(Assignment.topic_id == topic_id).all()
    return assignments

@router.get("/{assignment_id}", response_model=AssignmentSchema)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Получить задание по ID"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Задание не найдено")
    return assignment

@router.post("/", response_model=AssignmentSchema)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    """Создать новое задание"""
    # Проверяем, что тема существует
    topic = db.query(Topic).filter(Topic.id == assignment.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    
    db_assignment = Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.put("/{assignment_id}", response_model=AssignmentSchema)
def update_assignment(assignment_id: int, assignment: AssignmentUpdate, db: Session = Depends(get_db)):
    """Обновить задание"""
    db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Задание не найдено")
    
    update_data = assignment.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assignment, field, value)
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Удалить задание"""
    db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Задание не найдено")
    
    db.delete(db_assignment)
    db.commit()
    return {"message": "Задание успешно удалено"}

# ===== Hints endpoints =====

@router.get("/{assignment_id}/hints", response_model=List[HintSchema])
def get_hints_for_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Получить список подсказок для задания"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Задание не найдено")
    hints = (
        db.query(HintModel)
        .filter(HintModel.assignment_id == assignment_id)
        .order_by(HintModel.order_index.asc(), HintModel.id.asc())
        .all()
    )
    return hints

@router.get("/{assignment_id}/hints/{order_index}", response_model=HintSchema)
def get_hint_by_order(assignment_id: int, order_index: int, db: Session = Depends(get_db)):
    """Получить конкретную подсказку по порядковому номеру"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Задание не найдено")
    hint = (
        db.query(HintModel)
        .filter(HintModel.assignment_id == assignment_id, HintModel.order_index == order_index)
        .first()
    )
    if not hint:
        raise HTTPException(status_code=404, detail="Подсказка не найдена")
    return hint
