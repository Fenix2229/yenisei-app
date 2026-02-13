from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.models import HistoricalEvent
from pydantic import BaseModel

router = APIRouter(prefix="/api/events", tags=["events"])

# Pydantic схемы
class EventResponse(BaseModel):
    id: int
    epoch_id: int
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


# Получить все события
@router.get("/", response_model=List[EventResponse])
def get_all_events(
    skip: int = 0,
    limit: int = 100,
    epoch_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Получить список событий с фильтрацией
    - epoch_id: фильтр по эпохе
    - search: поиск по названию и описанию
    """
    query = db.query(HistoricalEvent)
    
    if epoch_id:
        query = query.filter(HistoricalEvent.epoch_id == epoch_id)
    
    if search:
        query = query.filter(
            or_(
                HistoricalEvent.title.contains(search),
                HistoricalEvent.description.contains(search)
            )
        )
    
    events = query.order_by(HistoricalEvent.year).offset(skip).limit(limit).all()
    return events


# Получить событие по ID
@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Получить конкретное событие"""
    event = db.query(HistoricalEvent).filter(HistoricalEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    return event


# Получить важные события (топ по важности)
@router.get("/important/top", response_model=List[EventResponse])
def get_important_events(limit: int = 10, db: Session = Depends(get_db)):
    """Получить самые важные события"""
    events = db.query(HistoricalEvent).order_by(
        HistoricalEvent.importance.desc()
    ).limit(limit).all()
    return events