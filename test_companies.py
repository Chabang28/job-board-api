from database import SessionLocal
from models import Company

db = SessionLocal()
companies = db.query(Company).all()
for company in companies:
    print(company.email, company.hashed_password)
