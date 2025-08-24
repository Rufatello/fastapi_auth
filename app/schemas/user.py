from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import ValidationInfo


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    password_confirm: str

    @field_validator("password_confirm")
    def validate_password_confirm(cls, v: str, info: ValidationInfo) -> str:
        password = info.data.get("password")

        if password and v != password:
            raise ValueError("Пароли не совпадают")
        return v

    @field_validator("password")
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        return v


class UserResponse(BaseModel):
    email: str
    name: str
    id: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str
