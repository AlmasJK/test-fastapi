from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserAuthCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "strongpassword123"
            }
        }

class UserAuthLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "testuser",
                "password": "strongpassword123"
            }
        }

class UserAuthResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "testuser",
                "email": "testuser@example.com",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class UserInfo(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "testuser",
                "email": "testuser@example.com",
                "is_superuser": False,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z"
            }
        }
