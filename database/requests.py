import types
from io import BytesIO

from database.models import async_session
from database.models import User, Category, Item
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item_description(item_id: int) -> str:
    async with async_session() as session:
        result = await session.execute(select(Item.description).where(Item.id == item_id))
        description = result.scalars().first()
        return description if description else "Описание отсутствует."


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))


async def get_photo(image_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.image == image_id))
