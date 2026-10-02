from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from models.user import User
from schemas.user import UserCreate, UserRead
from services.exceptions import UserAlreadyExistsError
from services.user import create_user

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
