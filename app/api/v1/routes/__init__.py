from fastapi import APIRouter
from app.api.v1.routes import auth
from app.api.v1.routes import job


router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(job.router, prefix="/jobs", tags=["jobs"])