from sqlalchemy import Column, Integer, String

from app.database.base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, index=True, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
