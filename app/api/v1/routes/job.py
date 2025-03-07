from fastapi import APIRouter, Depends, HTTPException, Form, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.db.models.job import Job
from app.db.models.user import User
from app.api.v1.schemas.job import JobCreate, JobUpdate, JobResponse, CategoriesResponseModel
from app.core.database import get_db
from app.utils.auth import get_current_user
from app.utils.response_utils import ResponseHandler, ResponseModel
from app.db.repositories.job import update_job_db, delete_job_by_id, get_jobs_db, create_job_db, get_job_by_id,change_job_status_db

router = APIRouter()

# Get all jobs
@router.get("/", response_model=ResponseModel[List[JobResponse]])
def get_jobs(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="User not found", status_code=404)
    if current_user.role not in ["admin","editor","viewer"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    jobs = get_jobs_db(db)
    if jobs:
        return ResponseHandler.success(data=[JobResponse.model_validate(job) for job in jobs], message="Jobs fetched successfully")
    return ResponseHandler.error(message="No jobs found", status_code=404)
    

# Create a new job
@router.post("/", response_model=ResponseModel[JobResponse])
def create_job(job: JobCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="User not found", status_code=404)
    if current_user.role not in ["admin","editor"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    job_response = create_job_db(db, job)
    if job_response:
        return ResponseHandler.success(data=JobResponse.model_validate(job_response), message="Job created successfully")
    return ResponseHandler.error(message="Job not created", status_code=500)


# Get the categories of jobs
@router.get("/categories/", response_model=CategoriesResponseModel)
def get_job_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="User not found", status_code=404)
    
    if current_user.role not in ["admin", "editor", "viewer"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    
    # Query distinct categories from the Job model
    categories = db.query(Job.category).distinct().all()
    
    # Convert list of tuples to a list of strings
    category_list = [category[0] for category in categories]

    if category_list:
        return ResponseHandler.success(data=category_list, message="Categories fetched successfully")
    return ResponseHandler.error(message="No categories found", status_code=404)   



# Get a single job by ID
@router.get("/{job_id}/", response_model=ResponseModel[JobResponse])
def get_job(job_id: UUID, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="User not found", status_code=404)
    if current_user.role not in ["admin","editor","viewer"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    job = get_job_by_id(db, job_id)
    if job:
        return ResponseHandler.success(data=JobResponse.model_validate(job), message="Job fetched successfully")
    return ResponseHandler.error(message="Job not found", status_code=404)
    

# Update an existing job by ID
@router.put("/{job_id}/edit/", response_model=ResponseModel[JobResponse])
def update_job(job_id: UUID, job: JobUpdate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="User not found", status_code=404)
    if current_user.role not in ["admin","editor"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    updated_job = update_job_db(db, job_id, job)
    if updated_job:
        return ResponseHandler.success(data=JobResponse.model_validate(updated_job), message="Job updated successfully")
    return ResponseHandler.error(message="Job not found", status_code=404)


# change the status of a job
@router.put("/{job_id}/status/{status}/", response_model=ResponseModel[JobResponse])
def change_job_status(job_id: UUID, status: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="User not found", status_code=404)
    if current_user.role not in ["admin","editor"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    job = change_job_status_db(db, job_id, status)
    if job:
        return ResponseHandler.success(data=JobResponse.model_validate(job), message="Job status updated successfully")
    return ResponseHandler.error(message="Job not found", status_code=404)

    

# Delete a job by ID
@router.delete("/{job_id}/delete/", response_model=ResponseModel[JobResponse])
def delete_job(job_id: UUID, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        return ResponseHandler.error(message="User not found", status_code=404)
    if current_user.role not in ["admin","editor"]:
        return ResponseHandler.error(message="User not authorized", status_code=401)
    job_to_delete = delete_job_by_id(db, job_id)
    if job_to_delete:
        return ResponseHandler.success(data=JobResponse.model_validate(job_to_delete), message="Job deleted successfully")
    return ResponseHandler.error(message="Job not found", status_code=404)

