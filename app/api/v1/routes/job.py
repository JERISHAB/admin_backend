from fastapi import APIRouter, Depends, HTTPException, Form, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.api.v1.schemas.job import JobCreate, JobUpdate, JobResponse
from app.core.database import get_db
from app.utils.response_utils import ResponseHandler, ResponseModel
from app.db.repositories.job import update_job_db, delete_job_by_id, get_jobs_db, create_job_db, get_job_by_id

router = APIRouter()

# Get all jobs
@router.get("/", response_model=ResponseModel[List[JobResponse]])
def get_jobs(db: Session = Depends(get_db)):
    try:
        jobs = get_jobs_db(db)
        return ResponseHandler.success(data=[JobResponse.model_validate(job) for job in jobs], message="Jobs fetched successfully")
    except Exception as e:
        return ResponseHandler.error(message=str(e), status_code=500)
    

# Create a new job
@router.post("/", response_model=ResponseModel[JobResponse])
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        job_response = create_job_db(db, job)
        return ResponseHandler.success(data=JobResponse.model_validate(job_response), message="Job created successfully")
    except Exception as e:
        return ResponseHandler.error(message=str(e), status_code=500)
    

# Get a single job by ID
@router.get("/{job_id}/", response_model=ResponseModel[JobResponse])
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    try:
        job = get_job_by_id(db, job_id)
        if job:
            return ResponseHandler.success(data=JobResponse.model_validate(job), message="Job fetched successfully")
        return ResponseHandler.error(message="Job not found", status_code=404)
    except Exception as e:
        return ResponseHandler.error(message=str(e), status_code=500)
    

# Update an existing job by ID
@router.put("/jobs/{job_id}/", response_model=ResponseModel[JobResponse])
def update_job(job_id: UUID, job: JobUpdate, db: Session = Depends(get_db)):
    try:
        updated_job = update_job_db(db, job_id, job)
        if updated_job:
            return ResponseHandler.success(data=JobResponse.model_validate(updated_job), message="Job updated successfully")
        return ResponseHandler.error(message="Job not found", status_code=404)
    except Exception as e:
        return ResponseHandler.error(message=str(e), status_code=500)
    

# Delete a job by ID
@router.delete("/jobs/{job_id}/", response_model=ResponseModel[JobResponse])
def delete_job(job_id: UUID, db: Session = Depends(get_db)):
    try:
        job_to_delete = delete_job_by_id(db, job_id)
        if job_to_delete:
            return ResponseHandler.success(data=JobResponse.model_validate(job_to_delete), message="Job deleted successfully")
        return ResponseHandler.error(message="Job not found", status_code=404)
    except Exception as e:
        return ResponseHandler.error(message=str(e), status_code=500)
