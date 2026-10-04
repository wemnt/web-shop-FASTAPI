from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(max_length=32)
    date_birth: date | None = None
    mobile_number: PhoneNumber | None = None
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    name: str
    date_birth: date | None = None
    mobile_number: PhoneNumber | None = None


class UserUpdate(BaseModel):
    email: EmailStr
    name: str = Field(max_length=32)
    date_birth: date | None = None
    mobile_number: PhoneNumber | None = None
