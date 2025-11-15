from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password


async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed_pw = hash_password(user_in.password)
    user = User(email=user_in.email, full_name=user_in.full_name,
                hashed_password=hashed_pw)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def list_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate):
    user = await get_user(db, user_id)
    if not user:
        return None
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
