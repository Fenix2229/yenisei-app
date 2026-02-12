from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models import QuizQuestion
from pydantic import BaseModel

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

# Pydantic схемы
class QuizQuestionResponse(BaseModel):
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: str
    category: str
    points: int
    
    class Config:
        from_attributes = True

class QuizAnswerRequest(BaseModel):
    question_id: int
    answer: str  # "A", "B", "C", "D"

class QuizAnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str
    points_earned: int


# Получить случайные вопросы для викторины
@router.get("/questions/random", response_model=List[QuizQuestionResponse])
def get_random_questions(
    count: int = 10,
    difficulty: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Получить случайные вопросы для викторины
    - count: количество вопросов
    - difficulty: easy, medium, hard
    - category: география, история, экология, культура
    """
    query = db.query(QuizQuestion)
    
    if difficulty:
        query = query.filter(QuizQuestion.difficulty == difficulty)
    
    if category:
        query = query.filter(QuizQuestion.category == category)
    
    questions = query.order_by(func.random()).limit(count).all()
    return questions


# Проверить ответ
@router.post("/check-answer", response_model=QuizAnswerResponse)
def check_answer(answer: QuizAnswerRequest, db: Session = Depends(get_db)):
    """Проверить ответ пользователя"""
    question = db.query(QuizQuestion).filter(
        QuizQuestion.id == answer.question_id
    ).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    
    is_correct = question.correct_answer.upper() == answer.answer.upper()
    
    return QuizAnswerResponse(
        is_correct=is_correct,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
        points_earned=question.points if is_correct else 0
    )


# Получить все категории вопросов
@router.get("/categories")
def get_quiz_categories(db: Session = Depends(get_db)):
    """Получить список категорий викторины"""
    categories = db.query(QuizQuestion.category).distinct().all()
    return {"categories": [cat[0] for cat in categories if cat[0]]}