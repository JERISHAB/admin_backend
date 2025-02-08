from sqlalchemy.orm import Session
from app.db.models.user import User
from app.api.v1.schemas.user import UserCreate
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get a user by their username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Get a user by their email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Create a new user and store their information in the database
def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
