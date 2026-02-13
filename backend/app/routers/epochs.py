from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Epoch, HistoricalEvent
from pydantic import BaseModel

router = APIRouter(prefix="/api/epochs", tags=["epochs"])

# Pydantic схемы для валидации
class EpochBase(BaseModel):
    name: str
    start_year: int
    end_year: int
    description: str
    color: str = "#3B82F6"
    
class EpochResponse(EpochBase):
    id: int
    order_index: int
    
    class Config:
        orm_mode = True

class EventInEpoch(BaseModel):
    id: int
    title: str
    year: int
    date_description: str
    description: str
    short_description: str
    image_url: str
    image_caption: str
    importance: int
    
    class Config:
        orm_mode = True

class EpochWithEvents(EpochResponse):
    events: List[EventInEpoch]


# Получить все эпохи
@router.get("/", response_model=List[EpochResponse])
def get_all_epochs(db: Session = Depends(get_db)):
    """Получить список всех эпох"""
    epochs = db.query(Epoch).order_by(Epoch.order_index).all()
    return epochs


# Получить эпоху с событиями
@router.get("/{epoch_id}", response_model=EpochWithEvents)
def get_epoch_with_events(epoch_id: int, db: Session = Depends(get_db)):
    """Получить эпоху со всеми событиями"""
    epoch = db.query(Epoch).filter(Epoch.id == epoch_id).first()
    if not epoch:
        raise HTTPException(status_code=404, detail="Эпоха не найдена")
    return epoch