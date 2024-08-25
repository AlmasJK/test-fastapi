from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.core.db import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from uuid import UUID
from typing import List

router = APIRouter()

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=List[User])
async def get_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all_users()

@router.post("/users", response_model=User)
async def create_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    return await user_service.create_user(user_data)

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, user_data: UserUpdate, user_service: UserService = Depends(get_user_service)):
    updated_user = await user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or not updated")
    return updated_user

@router.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    deleted_user = await user_service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
