import datetime
from typing import Dict

import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=settings.HASHING_SCHEME, deprecated="auto")


# функция для хэширования пароля
def get_password_hash(password: str):
    return pwd_context.hash(password)


# функция для валидации пароля
def verify_password(hash_password: str, password: str):
    return pwd_context.verify(hash_password, password)


# создание токена
def create_jwt_token(data: Dict):
    # копия данных
    to_encode = data.copy()
    # время жизни токена
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # данные для кодирования
    to_encode.update({"exp": expire})
    # кодируем данные
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
