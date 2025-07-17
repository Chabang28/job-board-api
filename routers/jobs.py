from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Job, Company
from pydantic import BaseModel
from typing import List
from auth import get_current_company

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas for request and response
class JobCreate(BaseModel):
    title: str
    description: str
    location: str

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    company_id: int

    class Config:
        orm_mode = True

# Route to create job - requires authentication
@router.post("/", response_model=JobResponse)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_company: Company = Security(get_current_company),
):
    new_job = Job(
        title=job.title,
        description=job.description,
        location=job.location,
        company_id=current_company.id,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

# Route to list jobs - public
@router.get("/", response_model=List[JobResponse])
def list_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs
