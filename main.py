from fastapi import FastAPI
from routers import companies, jobs

app = FastAPI()

app.include_router(companies.router, prefix="/companies")
app.include_router(jobs.router, prefix="/jobs")
