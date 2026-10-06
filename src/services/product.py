from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from services.exceptions import ProductNotFoundError


async def create_product(session: AsyncSession, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    session.add(product)
    await session.commit()
    return product


async def get_product(
    session: AsyncSession, product_id: UUID, *, include_inactive: bool = False
) -> Product:
    product = await session.get(Product, product_id)
    if product is None or product.deleted_at is not None:
        raise ProductNotFoundError("Product not found")
    if not include_inactive and not product.is_active:
        raise ProductNotFoundError("Product not found")
    return product


async def update_product(
    session: AsyncSession, product_id: UUID, data: ProductUpdate
) -> Product:
    product = await get_product(session, product_id)
    update_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product_id: UUID) -> None:
    product = await get_product(session, product_id)
    product.deleted_at = datetime.now(tz=UTC)
    await session.commit()


async def list_products(
    session: AsyncSession,
    *,
    page: int,
    size: int,
    include_inactive: bool = False,
) -> list[Product]:
    query = select(Product).where(Product.deleted_at.is_(None))
    if not include_inactive:
        query = query.where(Product.is_active.is_(True))
    query = query.order_by(Product.created_at.desc()).limit(size).offset(page * size)

    result = await session.scalars(query)
    return list(result.all())
