from uuid import UUID

from fastapi import APIRouter, status

from db.session import SessionDep
from models.user import User
from schemas.user import PasswordChange, UserCreate, UserRead, UserUpdate
from services.user import (
    create_user,
    delete_user,
    get_user,
    update_password,
    update_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    session: SessionDep,
) -> User:
    return await create_user(session=session, data=data)


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: UUID,
    session: SessionDep,
) -> User:
    return await get_user(session=session, user_id=user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_by_id(
    user_id: UUID,
    data: UserUpdate,
    session: SessionDep,
) -> User:
    return await update_user(session=session, user_id=user_id, data=data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: UUID,
    session: SessionDep,
) -> None:
    await delete_user(session=session, user_id=user_id)


@router.post("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
    user_id: UUID,
    data: PasswordChange,
    session: SessionDep,
) -> None:
    await update_password(session=session, user_id=user_id, data=data)
