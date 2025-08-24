from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic
from sqlalchemy.orm import Session
from starlette import status

from app.controllers.user_controller import (
    create_user,
    get_user_from_token,
    login_controller,
)
from app.database.db import get_db, get_user
from app.schemas.user import UserCreate, UserLogin, UserResponse

security = HTTPBasic()
app = FastAPI()


@app.get("/")
async def new_():
    return {"message": "1"}


@app.post("/login")
async def login(user_in: UserLogin, db: Session = Depends(get_db)):
    return login_controller(user_in, db)


@app.get("/about_me", response_model=UserResponse)
async def about_me(
    current_user: str = Depends(get_user_from_token), db: Session = Depends(get_db)
):

    user = get_user(db, current_user)
    # отработка наличия пользователя
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="нет такого пользователя"
    )


@app.post("/register", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(user_data, db)
