from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    email: str
    password: str

class CompanyLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
