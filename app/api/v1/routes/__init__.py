from fastapi import APIRouter
from app.api.v1.routes import auth
from app.api.v1.routes import job
from app.api.v1.routes import member


router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(job.router, prefix="/jobs", tags=["jobs"])
router.include_router(member.router, prefix="/members", tags=["members"])