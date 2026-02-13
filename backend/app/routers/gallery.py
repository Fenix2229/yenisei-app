from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import GalleryImage
from pydantic import BaseModel

router = APIRouter(prefix="/api/gallery", tags=["gallery"])

# Pydantic схемы
class GalleryImageResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: str
    category: str
    photographer: Optional[str]
    year_taken: Optional[int]
    location: str
    is_featured: bool
    
    class Config:
        orm_mode = True


# Получить все изображения галереи
@router.get("/", response_model=List[GalleryImageResponse])
def get_gallery_images(
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Получить изображения галереи
    - category: фильтр по категории
    - featured: только избранные
    """
    query = db.query(GalleryImage)
    
    if category:
        query = query.filter(GalleryImage.category == category)
    
    if featured is not None:
        query = query.filter(GalleryImage.is_featured == featured)
    
    images = query.order_by(GalleryImage.order_index).all()
    return images


# Получить изображение по ID
@router.get("/{image_id}", response_model=GalleryImageResponse)
def get_gallery_image(image_id: int, db: Session = Depends(get_db)):
    """Получить конкретное изображение"""
    image = db.query(GalleryImage).filter(GalleryImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return image