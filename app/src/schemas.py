from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from enum import Enum


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    phone: str = Field(min_length=10, max_length=13)
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)


class RoleOptions(str, Enum):
    user = "user"
    admin = "admin"


class UserDb(BaseModel):
    id: int
    username: str
    phone: str
    email: EmailStr
    created_at: datetime
    role: RoleOptions
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class UserPassword(BaseModel):
    old_password: str = Field(min_length=6, max_length=20)
    new_password: str = Field(min_length=6, max_length=20)


class UserNewPassword(BaseModel):
    email: EmailStr
    new_password: str = Field(min_length=6, max_length=20)


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class Car(BaseModel):
    car_license: str


class CarResponse(BaseModel):
    car: Car
    detail: str
