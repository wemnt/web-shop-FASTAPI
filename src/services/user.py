from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from models.user import User
from schemas.user import UserCreate
from services.exceptions import UserAlreadyExistsError


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    existing = await session.scalar(select(User).where(User.email == data.email))
    if existing:
        raise UserAlreadyExistsError("Email already exists")

    hashed = await run_in_threadpool(hash_password, data.password)
    user = User(**data.model_dump(exclude={"password"}), hashed_password=hashed)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExistsError("Email already exists") from None
    await session.refresh(user)
    return user
