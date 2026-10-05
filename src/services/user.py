from uuid import UUID

from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from models.user import User
from schemas.user import UserCreate, UserUpdate
from services.exceptions import UserAlreadyExistsError, UserNotFoundError


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    existing = await session.scalar(select(User).where(User.email == data.email))
    if existing is not None:
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


async def get_user(session: AsyncSession, user_id: UUID) -> User:
    query = select(User).where(
        User.id == user_id,
        User.is_active.is_(True),
        User.deleted_at.is_(None),
    )

    user = await session.scalar(query)
    if user is None:
        raise UserNotFoundError("User not found")
    return user


async def update_user(session: AsyncSession, user_id: UUID, data: UserUpdate) -> User:
    user = await get_user(session, user_id)
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "email" and value != user.email:
            existing = await session.scalar(select(User).where(User.email == value))
            if existing is not None:
                raise UserAlreadyExistsError("Email already exists")
        setattr(user, key, value)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExistsError("Email already exists") from None
    return user
