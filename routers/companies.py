from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import CompanyCreate, CompanyLogin, Token
from database import SessionLocal
from models import Company
from auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.email == company.email).first()
    if db_company:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = get_password_hash(company.password)
    new_company = Company(name=company.name, email=company.email, password=hashed_pw)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return {"message": "Company registered successfully"}

@router.post("/login", response_model=Token)
def login_company(credentials: CompanyLogin, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.email == credentials.email).first()
    if not db_company or not verify_password(credentials.password, db_company.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": db_company.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
