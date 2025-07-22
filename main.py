from fastapi import FastAPI
from routers import companies, jobs, users

app = FastAPI()

app.include_router(companies.router, prefix="/companies")
app.include_router(jobs.router, prefix="/jobs")
app.include_router(users.router, prefix="/users")
