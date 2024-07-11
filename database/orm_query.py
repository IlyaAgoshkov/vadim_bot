from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Item


async def orm_add_product(session: AsyncSession, data: dict):
    obj = Item(
        category=data['category'],
        name=data["name"],
        description=data["description"],
        price=data["price"],
        image=data["image"],
    )
    session.add(obj)
    await session.commit()


async def orm_get_products(session: AsyncSession):
    query = select(Item)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Item).where(Item.id == product_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_product(session: AsyncSession, product_id: int, data):
    query = update(Item).where(Item.id == product_id).values(
        category=data['category'],
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],)
    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, item_id: int):
    query = delete(Item).where(Item.id == item_id)
    await session.execute(query)
    await session.commit()