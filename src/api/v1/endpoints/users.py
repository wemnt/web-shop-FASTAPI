from uuid import UUID

from fastapi import APIRouter, status

from api.deps import AdminUserDep, CurrentUserDep
from db.session import SessionDep
from models.user import User
from schemas.user import PasswordChange, RoleUpdate, UserCreate, UserRead, UserUpdate
from services.user import (
    change_user_role,
    create_user,
    delete_user,
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


@router.get("/me", response_model=UserRead)
async def get_me(user: CurrentUserDep) -> User:
    return user


# @router.get("/{user_id}", response_model=UserRead) на будущее под админку
# async def get_user_by_id(
#    user: CurrentUserDep,
#    session: SessionDep,
# ) -> User:
#    return await get_user(session=session, user_id=user.id)


@router.patch("/me", response_model=UserRead)
async def update_user_by_id(
    user: CurrentUserDep,
    data: UserUpdate,
    session: SessionDep,
) -> User:
    return await update_user(session=session, user_id=user.id, data=data)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user: CurrentUserDep,
    session: SessionDep,
) -> None:
    await delete_user(session=session, user_id=user.id)


@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
    user: CurrentUserDep,
    data: PasswordChange,
    session: SessionDep,
) -> None:
    await update_password(session=session, user_id=user.id, data=data)


@router.patch("/{user_id}/role", response_model=UserRead)
async def change_user_role_by_id(
    user_id: UUID, data: RoleUpdate, session: SessionDep, admin: AdminUserDep
) -> User:

    return await change_user_role(
        session=session, user_id=user_id, actor_id=admin.id, role=data.role
    )
