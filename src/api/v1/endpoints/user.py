from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from db.session import SessionDep
from models.user import User
from schemas.user import PasswordChange, UserCreate, UserRead, UserUpdate
from services.exceptions import (
    IncorrectPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
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


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: UUID,
    session: SessionDep,
) -> None:
    try:
        await delete_user(session=session, user_id=user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
    user_id: UUID,
    data: PasswordChange,
    session: SessionDep,
) -> None:
    try:
        await update_password(session=session, user_id=user_id, data=data)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except IncorrectPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
