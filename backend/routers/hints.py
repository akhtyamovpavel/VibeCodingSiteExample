from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Hint as HintModel, Assignment
from schemas import Hint as HintSchema, HintCreate, HintUpdate
from typing import List

router = APIRouter()

@router.get("/assignment/{assignment_id}", response_model=List[HintSchema])
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

@router.get("/{hint_id}", response_model=HintSchema)
def get_hint(hint_id: int, db: Session = Depends(get_db)):
    """Получить подсказку по ID"""
    hint = db.query(HintModel).filter(HintModel.id == hint_id).first()
    if not hint:
        raise HTTPException(status_code=404, detail="Подсказка не найдена")
    return hint

@router.post("/", response_model=HintSchema)
def create_hint(hint: HintCreate, db: Session = Depends(get_db)):
    """Создать новую подсказку"""
    # Проверяем, что задание существует
    assignment = db.query(Assignment).filter(Assignment.id == hint.assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Задание не найдено")
    
    db_hint = HintModel(**hint.dict())
    db.add(db_hint)
    db.commit()
    db.refresh(db_hint)
    return db_hint

@router.put("/{hint_id}", response_model=HintSchema)
def update_hint(hint_id: int, hint: HintUpdate, db: Session = Depends(get_db)):
    """Обновить подсказку"""
    db_hint = db.query(HintModel).filter(HintModel.id == hint_id).first()
    if not db_hint:
        raise HTTPException(status_code=404, detail="Подсказка не найдена")
    
    update_data = hint.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_hint, field, value)
    
    db.commit()
    db.refresh(db_hint)
    return db_hint

@router.delete("/{hint_id}")
def delete_hint(hint_id: int, db: Session = Depends(get_db)):
    """Удалить подсказку"""
    db_hint = db.query(HintModel).filter(HintModel.id == hint_id).first()
    if not db_hint:
        raise HTTPException(status_code=404, detail="Подсказка не найдена")
    
    db.delete(db_hint)
    db.commit()
    return {"message": "Подсказка успешно удалена"}
