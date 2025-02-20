from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role : str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str

    class Config:
        from_attributes = True
