from sqlalchemy import UUID, Column, String, Integer, Enum, DateTime, ARRAY
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime,timedelta,timezone
from app.core.database import Base
 # Assuming Base is your SQLAlchemy declarative base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    experience_required = Column(Integer, nullable=False)
    status = Column(Enum("active", "private", "closed", name="job_status"), default="private")
    location = Column(Enum("remote", "hybrid", "onsite", name="job_location"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc)) # sets the time as now in UTC and converts it to IST timezone before storing it in the database
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_date = Column(DateTime, nullable=True)
    timing = Column(Enum('full-time', 'part-time', 'contract', name='job_timing'), nullable=False)
    about = Column(String, nullable=False)
    responsibilities = Column(ARRAY(String), nullable=True)