from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.security import create_access_token
from db.session import SessionDep
from schemas.auth import Token
from services.auth import authenticate_user

LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(form: LoginFormDep, session: SessionDep) -> Token:
    user = await authenticate_user(session, form.username, form.password)
    return Token(access_token=create_access_token(user.id))
