from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.security import decode_access_token
from db.session import SessionDep
from models.user import User
from services.exceptions import AuthTokenError, UserNotFoundError
from services.user import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> User:
    user_id = decode_access_token(token)
    try:
        return await get_user(session, user_id)
    except UserNotFoundError as e:
        raise AuthTokenError("Invalid token") from e


CurrentUserDep = Annotated[User, Depends(get_current_user)]
