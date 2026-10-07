from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from db.session import SessionDep
from models.product import Product
from schemas.product import ProductCreate, ProductRead, ProductUpdate
from services.product import (
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(data: ProductCreate, session: SessionDep) -> Product:
    product = await create_product(data=data, session=session)
    return product


@router.get("/{product_id}", response_model=ProductRead)
async def get_product_endpoint(product_id: UUID, session: SessionDep) -> Product:
    return await get_product(product_id=product_id, session=session)


@router.get("", response_model=list[ProductRead])
async def get_products(
    session: SessionDep,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    page: Annotated[int, Query(ge=0)] = 0,
) -> list[Product]:
    return await list_products(session, page=page, size=size)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product_endpoint(
    product_id: UUID, data: ProductUpdate, session: SessionDep
) -> Product:
    return await update_product(
        product_id=product_id, data=data, session=session
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_endpoint(product_id: UUID, session: SessionDep) -> None:
    await delete_product(product_id=product_id, session=session)
