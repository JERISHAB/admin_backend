from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base
from sqlalchemy import Enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum("editor","viewer","admin", name="user_role"), default="viewer")
