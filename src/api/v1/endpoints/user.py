from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate
from services.exceptions import UserAlreadyExistsError, UserNotFoundError
from services.user import create_user, get_user, update_user

router = APIRouter(prefix="/user", tags=["user"])


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    session: SessionDep,
) -> User:
    try:
        user = await create_user(session=session, data=data)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return user


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: UUID,
    session: SessionDep,
) -> User:
    try:
        user = await get_user(session=session, user_id=user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_by_id(
    user_id: UUID,
    data: UserUpdate,
    session: SessionDep,
) -> User:
    try:
        user = await update_user(session=session, user_id=user_id, data=data)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return user
