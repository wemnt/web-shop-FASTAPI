from fastapi import APIRouter
from schemas.user import User

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/")
def create_user(user: User):
    return user
