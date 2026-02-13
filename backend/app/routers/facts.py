from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models import InterestingFact
from pydantic import BaseModel

router = APIRouter(prefix="/api/facts", tags=["facts"])

# Pydantic схемы
class FactResponse(BaseModel):
    id: int
    title: str
    fact: str
    category: str
    icon: str
    
    class Config:
        orm_mode = True


# Получить все факты
@router.get("/", response_model=List[FactResponse])
def get_all_facts(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить интересные факты о Енисее"""
    query = db.query(InterestingFact)
    
    if category:
        query = query.filter(InterestingFact.category == category)
    
    facts = query.order_by(InterestingFact.order_index).all()
    return facts


# Получить случайный факт
@router.get("/random", response_model=FactResponse)
def get_random_fact(db: Session = Depends(get_db)):
    """Получить случайный факт"""
    fact = db.query(InterestingFact).order_by(func.random()).first()
    if not fact:
        raise HTTPException(status_code=404, detail="Факты не найдены")
    return fact