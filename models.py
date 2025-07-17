from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    jobs = relationship("Job", back_populates="company")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    cv_link = Column(String)
    job_id = Column(Integer, ForeignKey("jobs.id"))

    job = relationship("Job", back_populates="applications")
