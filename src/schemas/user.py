from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from constants.user import UserRole


class UserCreate(BaseModel):
    fio: str = Field(pattern=r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$")
    email: Optional[EmailStr] = None
    login: str
    password: str


class UserBase(BaseModel):
    fio: str
    email: Optional[EmailStr] = None
    login: str


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool


class UserCreateDB(UserBase):
    hashed_password: str
    is_email_verified: Optional[bool] = None
    company_id: Optional[int] = None
    role: Optional[UserRole] = UserRole.admin


class UserUpdateDB(BaseModel):
    company_id: Optional[int] = None
    is_email_verified: Optional[bool] = None
    hashed_password: Optional[str] = None
    fio: Optional[str] = None
    email: Optional[EmailStr] = None
