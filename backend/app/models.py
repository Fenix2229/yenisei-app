from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# Модель для исторических эпох
class Epoch(Base):
    __tablename__ = "epochs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)  # Например: "Палеолит", "Эпоха освоения"
    start_year = Column(Integer)  # Год начала (может быть отрицательным для до н.э.)
    end_year = Column(Integer)  # Год окончания
    description = Column(Text)  # Описание эпохи
    color = Column(String(20), default="#3B82F6")  # Цвет для визуализации
    order_index = Column(Integer, default=0)  # Порядок отображения
    
    # Связи
    events = relationship("HistoricalEvent", back_populates="epoch", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Epoch {self.name}>"


# Модель для исторических событий
class HistoricalEvent(Base):
    __tablename__ = "historical_events"
    
    id = Column(Integer, primary_key=True, index=True)
    epoch_id = Column(Integer, ForeignKey("epochs.id"), nullable=False)
    title = Column(String(300), nullable=False)  # Название события
    year = Column(Integer)  # Год события
    date_description = Column(String(100))  # "около 10000 до н.э.", "1619 год"
    description = Column(Text, nullable=False)  # Подробное описание
    short_description = Column(String(500))  # Краткое описание для карточек
    image_url = Column(String(500))  # URL изображения
    image_caption = Column(String(300))  # Подпись к изображению
    importance = Column(Integer, default=5)  # Важность события (1-10)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    epoch = relationship("Epoch", back_populates="events")
    
    def __repr__(self):
        return f"<HistoricalEvent {self.title}>"


# Модель для географических точек на карте
class GeographicPoint(Base):
    __tablename__ = "geographic_points"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)  # Название точки (город, место)
    type = Column(String(50))  # "city", "landmark", "nature", "historical"
    latitude = Column(Float, nullable=False)  # Широта
    longitude = Column(Float, nullable=False)  # Долгота
    description = Column(Text)  # Описание места
    short_description = Column(String(300))  # Краткое описание
    founding_year = Column(Integer)  # Год основания (для городов)
    population = Column(Integer)  # Население (для городов)
    image_url = Column(String(500))  # Изображение места
    icon = Column(String(50), default="marker")  # Иконка для карты
    color = Column(String(20), default="#EF4444")  # Цвет маркера
    
    def __repr__(self):
        return f"<GeographicPoint {self.name}>"


# Модель для галереи изображений
class GalleryImage(Base):
    __tablename__ = "gallery_images"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    image_url = Column(String(500), nullable=False)
    category = Column(String(100))  # "nature", "people", "architecture", "wildlife"
    photographer = Column(String(200))  # Автор фото
    year_taken = Column(Integer)  # Год съемки
    location = Column(String(200))  # Место съемки
    order_index = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)  # Избранное фото
    
    def __repr__(self):
        return f"<GalleryImage {self.title}>"


# Модель для вопросов викторины
class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)  # Текст вопроса
    option_a = Column(String(300), nullable=False)
    option_b = Column(String(300), nullable=False)
    option_c = Column(String(300), nullable=False)
    option_d = Column(String(300), nullable=False)
    correct_answer = Column(String(1), nullable=False)  # "A", "B", "C" или "D"
    explanation = Column(Text)  # Объяснение правильного ответа
    difficulty = Column(String(20), default="medium")  # "easy", "medium", "hard"
    category = Column(String(100))  # "geography", "history", "ecology", "culture"
    points = Column(Integer, default=10)  # Баллы за правильный ответ
    
    def __repr__(self):
        return f"<QuizQuestion {self.question[:50]}...>"


# Модель для интересных фактов
class InterestingFact(Base):
    __tablename__ = "interesting_facts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    fact = Column(Text, nullable=False)
    category = Column(String(100))  # "nature", "statistics", "ecology", "culture"
    icon = Column(String(50), default="lightbulb")  # Иконка для UI
    order_index = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<InterestingFact {self.title}>"