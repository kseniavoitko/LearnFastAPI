from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    firstname: str = Field(min_length=3, max_length=12)
    lastname: str = Field(min_length=3, max_length=12)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=12)
    born_date: date


class ResponseContact(BaseModel):
    id: int = 1
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    born_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=6, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    # roles: Role

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
