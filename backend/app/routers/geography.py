from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.models import GeographicPoint
from pydantic import BaseModel

router = APIRouter(prefix="/api/geography", tags=["geography"])

# Pydantic схемы
class GeographicPointResponse(BaseModel):
    id: int
    name: str
    type: str
    latitude: float
    longitude: float
    description: str
    short_description: str
    founding_year: Optional[int]
    population: Optional[int]
    image_url: str
    icon: str
    color: str
    
    class Config:
        orm_mode = True


# Получить все географические точки
@router.get("/", response_model=List[GeographicPointResponse])
def get_geographic_points(
    type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получить географические точки
    - type: фильтр по типу (city, landmark, nature, historical)
    """
    query = db.query(GeographicPoint)
    
    if type:
        query = query.filter(GeographicPoint.type == type)
    
    points = query.offset(skip).limit(limit).all()
    return points


# Получить точку по ID
@router.get("/{point_id}", response_model=GeographicPointResponse)
def get_geographic_point(point_id: int, db: Session = Depends(get_db)):
    """Получить конкретную географическую точку"""
    point = db.query(GeographicPoint).filter(GeographicPoint.id == point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="Точка не найдена")
    return point


# Получить крупные города
@router.get("/cities/major", response_model=List[GeographicPointResponse])
def get_major_cities(db: Session = Depends(get_db)):
    """Получить крупные города на Енисее"""
    cities = db.query(GeographicPoint).filter(
        GeographicPoint.type == "city",
        GeographicPoint.population != None
    ).order_by(GeographicPoint.population.desc()).limit(10).all()
    return cities


# Получить достопримечательности
@router.get("/landmarks/", response_model=List[GeographicPointResponse])
def get_landmarks(db: Session = Depends(get_db)):
    """Получить достопримечательности"""
    landmarks = db.query(GeographicPoint).filter(
        GeographicPoint.type == "landmark"
    ).all()
    return landmarks


# Поиск по названию
@router.get("/search/{query}", response_model=List[GeographicPointResponse])
def search_points(query: str, db: Session = Depends(get_db)):
    """Поиск географических точек по названию"""
    points = db.query(GeographicPoint).filter(
        or_(
            GeographicPoint.name.contains(query),
            GeographicPoint.description.contains(query)
        )
    ).all()
    return points
