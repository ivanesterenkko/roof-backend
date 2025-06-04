from pydantic import BaseModel
from schemas.company import CompanyCreate
from schemas.user import UserCreate


class RegisterAdminData(BaseModel):
    user: UserCreate
    company: CompanyCreate


class TokenResponse(BaseModel):
    access_token: str


class UserAuth(BaseModel):
    login_or_email: str
    password: str
