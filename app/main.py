import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import auth,job,member, router as api_router  # Import your API routes

# Load environment variables from a .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routers for different routes
app.include_router(auth.router, prefix="/api/v1/users", tags=["Users"])  # Users-related routes
app.include_router(job.router, prefix="/api/v1/jobs", tags=["Jobs"])  # Jobs-related routes
app.include_router(member.router, prefix="/api/v1/members", tags=["Members"])  # Members-related routes
# Root endpoint for basic health check

@app.get("/")
def read_root():
    return {"message": "Hello World! The backend server is running and live for API Testing."}
