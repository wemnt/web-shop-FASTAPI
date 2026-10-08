from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    # Class Base конфликтует с ипизацией SQLAlchemy
    __mapper_args__ = {"eager_defaults": True}  # noqa: RUF012
