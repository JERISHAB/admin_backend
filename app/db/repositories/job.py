from sqlalchemy.orm import Session
from app.api.v1.schemas.job import JobCreate
from app.db.models.job import Job
from app.db.models.user import User
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

# Get all jobs with pagination
def get_jobs_db(db: Session):
    return db.query(Job).all()

# Get a specific job by ID
def get_job_by_id(db: Session, job_id: UUID):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None
    return job

# Create a new job posting
def create_job_db(db: Session, job_data: JobCreate):
    try:
        new_job = Job(title = job_data.title,
                      category=job_data.category,
                      experience_required = job_data.experience_required,
                      status = job_data.status,
                      location = job_data.location,
                      timing = job_data.timing,
                      about = job_data.about,
                      responsibilities = job_data.responsibilities,
                      last_date = job_data.last_date
                      ) # THis line means that we are creating a new Job object with the data passed in the job_data dictionary
        db.add(new_job) 
        db.commit()
        db.refresh(new_job)
        return new_job
    except SQLAlchemyError:
        db.rollback()
        return None

# Update a job posting
def update_job_db(db: Session, job_id: UUID, job_data: JobCreate):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None
    for key, value in job_data.model_dump().items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job

# Change the status of a job posting
def change_job_status_db(db: Session, job_id: UUID, status: str):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None
    job.status = status
    db.commit()
    db.refresh(job)
    return job

# Delete a job posting
def delete_job_by_id(db: Session, job_id: UUID):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None
    db.delete(job)
    db.commit()
    return job
