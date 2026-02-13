from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base, SessionLocal
from app.routers import epochs, events, geography, gallery, quiz, facts
from app.models import Epoch

# Получаем настройки
settings = get_settings()

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Всегда пересоздаём базу данных при старте (на бесплатном Render она сбрасывается)
def init_db():
    print("🌊 Инициализация базы данных...")
    from seed_data import main as seed_main
    seed_main()
    print("✅ База данных готова!")

init_db()

# Инициализируем FastAPI приложение
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API для приложения 'История реки Енисей'"
)

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(epochs.router)
app.include_router(events.router)
app.include_router(geography.router)
app.include_router(gallery.router)
app.include_router(quiz.router)
app.include_router(facts.router)

# Корневой эндпоинт
@app.get("/")
def root():
    return {
        "message": "Добро пожаловать в API 'История реки Енисей'",
        "version": settings.app_version,
        "docs": "/docs"
    }

# Эндпоинт для проверки здоровья API
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API работает"}

# Эндпоинт для пересоздания базы данных
@app.get("/api/reseed")
def reseed_database():
    """Пересоздать базу данных с новыми данными"""
    try:
        from seed_data import main as seed_main
        seed_main()
        return {"status": "ok", "message": "База данных пересоздана!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Точка входа для запуска
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)