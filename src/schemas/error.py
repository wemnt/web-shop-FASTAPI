from pydantic import BaseModel


class FieldError(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    message: str
    detail: list[FieldError] | None = None
