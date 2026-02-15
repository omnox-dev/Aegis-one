from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.database import engine, Base
from app.api import (
    auth, grievances, courses, internships, users, dashboard,
    attendance, resources, calendar, tasks, lost_found, announcements,
    commons, clubs, emergency, map,
)

# Import all models so SQLAlchemy knows about them for create_all
from app.models import user, grievance, course, internship  # noqa: F401
from app.models import attendance as attendance_model  # noqa: F401
from app.models import resource, academic_event, task  # noqa: F401
from app.models import lost_found as lost_found_model  # noqa: F401
from app.models import announcement, audit_log  # noqa: F401
from app.models import caravan_mercenary, clubs as clubs_model, incident, location # noqa: F401

# Create all tables
Base.metadata.create_all(bind=engine)

# Create uploads directory
os.makedirs("uploads", exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    description="Unified Campus Governance Platform — One Identity. One Platform. One Campus.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

from fastapi import Request
import time

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for deployment flexibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"DEBUG: {request.method} {request.url.path} - Status: {response.status_code} - In: {duration:.4f}s")
    return response

# Static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers — Core Pillars
app.include_router(auth.router)
app.include_router(grievances.router)
app.include_router(courses.router)
app.include_router(internships.router)
app.include_router(users.router)
app.include_router(dashboard.router)

# Pillar III: Academic Mastery
app.include_router(attendance.router)
app.include_router(resources.router)
app.include_router(calendar.router)

# Pillar IV: Tasks (Scholar's Ledger)
app.include_router(tasks.router)

# Additional functionality
app.include_router(lost_found.router)
app.include_router(announcements.router)
# app.include_router(forum.router)
app.include_router(commons.router)
app.include_router(clubs.router)
app.include_router(emergency.router)
app.include_router(map.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "name": settings.APP_NAME,
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
