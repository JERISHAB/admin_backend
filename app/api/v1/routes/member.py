from fastapi import APIRouter, Depends
from typing import List
from pydantic import validate_email
from sqlalchemy.orm import Session
from app.api.v1.schemas.user import UserCreate, UserResponse
from app.db.models.user import User
from app.core.database import get_db
from app.db.repositories.user import create_user, get_user_by_email, get_user_by_id, get_user_by_username
from app.utils.auth import get_current_user
from app.utils.response_utils import ResponseHandler, ResponseModel

router = APIRouter()


# Create a member viewer or editor
@router.post("/create/", response_model=ResponseModel[UserResponse])
def create_member(user:UserCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="User not found", status_code=404)
    if current_user.role not in ["admin"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    

    # Validate email format
    if not validate_email(user.email):
        return ResponseHandler.error("Invalid email address", status_code=400)
    
    #check if username is already in use
    db_user_by_username = get_user_by_username(db, username=user.username)
    if db_user_by_username:
        return ResponseHandler.error("Username already registered", status_code=400)    
    
    # Check if email is already in use
    db_user_by_email = get_user_by_email(db, email=user.email)
    if db_user_by_email:
        return ResponseHandler.error("Email already registered", status_code=400)

    # Create the new user and return response
    user_response = create_user(db, user)
    if user_response:
        return ResponseHandler.success(data=UserResponse.model_validate(user_response), message="User created successfully")
    return ResponseHandler.error(message="User not created", status_code=500)



# Get all members
@router.get("/", response_model=ResponseModel[List[UserResponse]])
def get_members(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # try:
        print(current_user)
        members = db.query(User).all()
        if members:
            return ResponseHandler.success(data=[UserResponse.model_validate(member) for member in members], message="Members fetched successfully")
        print("Error: No members found")
        return ResponseHandler.error(message="No members found", status_code=404)
    # except Exception as e:
    #     print("Error fetching members:", e)
    #     raise HTTPException(status_code=500, detail=str(e))



# Change the role of a member
@router.put("/{user_id}/change-role/{role}", response_model=ResponseModel[UserResponse])
def change_role(user_id: int, role: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="Admin not found", status_code=404)
    if current_user.role not in ["admin"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    user = get_user_by_id(db, user_id)
    if not user:
        return ResponseHandler.error(message="User not found", status_code=404)
    user.role = role
    db.commit()
    db.refresh(user)
    return ResponseHandler.success(data=UserResponse.model_validate(user), message="User role changed successfully") 


# Delete a member
@router.delete("/{user_id}/delete/", response_model=ResponseModel[UserResponse])
def delete_member(user_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="User not found", status_code=404)
    if current_user.role not in ["admin"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    user = get_user_by_id(db, user_id)
    if not user:
        return ResponseHandler.error(message="User not found", status_code=404)
    db.delete(user)
    db.commit()
    return ResponseHandler.success(data=UserResponse.model_validate(user), message="User deleted successfully")