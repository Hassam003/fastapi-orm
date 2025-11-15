from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserOut, UserUpdate
from app.crud import user_crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_crud.create_user(db, user_in)


@router.get("/", response_model=List[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.list_users(db)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    updated_user = await user_crud.update_user(db, user_id, user_in)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    await user_crud.delete_user(db, user_id)
