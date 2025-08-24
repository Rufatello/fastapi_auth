from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.database.models import User

# движок для подключения к БД
engine = create_engine(settings.database())
# сессия для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# получение пользователя по почте
def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
