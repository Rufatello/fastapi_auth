from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.core.security import create_jwt_token, get_password_hash, verify_password
from app.database.db import get_db, get_user
from app.database.models import User
from app.schemas.user import UserCreate, UserLogin

bearer_scheme = HTTPBearer(auto_error=False)


def login_controller(user_in: UserLogin, db: Session = Depends(get_db)):
    user = get_user(db, user_in.email)

    # отработка наличия пользователя
    if not user:
        raise HTTPException(status_code=401, detail="Нет такого пользователя")
    # отработка совпадения пароля
    if not verify_password(user_in.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    # создание токена
    token = create_jwt_token({"sub": user_in.email})
    return {"access_token": token, "token_type": "bearer"}


def get_user_from_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
):
    # проверка на наличие токена
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="нет токена",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # извлечение токена
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload.get("sub")
    # обработка ошибки истечения срока действия токена
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="срок действия токена истек",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # обработка ошибки недействительного токена
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_user(user_data: UserCreate, db: Session):
    # проверка наличия в бд почты
    user = get_user(db, user_data.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="пользователь такой уже существует",
        )
    # создания пользователя
    new_user = User(
        email=user_data.email,
        password=get_password_hash(user_data.password),
        name=user_data.name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
