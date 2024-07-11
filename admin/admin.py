from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config.config import ADMIN_ID
import database.requests as rq
from admin import admin_kb
from database.orm_query import orm_delete_product
from database.models import Item
from database.models import async_session

admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer("Что хотите сделать?", reply_markup=admin_kb.admin_panel)

@admin_router.message(F.text == 'Удалить товар')
async def catalog(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer('Выберите категорию', reply_markup=await admin_kb.categories())

@admin_router.callback_query(F.data.startswith('categoryadmin_'))
async def category(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите товар для удаления',
                                     reply_markup=await admin_kb.items(callback.data.split('_')[1]))

@admin_router.callback_query(F.data.startswith('itemadmin_'))
async def item(callback: CallbackQuery):
    item_id = callback.data.split('_')[1]
    item_data = await rq.get_item(item_id)
    await callback.answer()
    if item_data.image:
        file_id = item_data.image
        caption = (f'{item_data.name}\n\n'
                   f'Описание: {item_data.description}\n\n'
                   f'Цена: {item_data.price} руб.\n\n'
                   f'ID: {item_data.id}')
        await callback.message.answer_photo(photo=file_id, caption=caption, reply_markup=admin_kb.item_delete(item_id))
    else:
        message_text = (f'Название: {item_data.name}\n'
                        f'Описание: {item_data.description}\n'
                        f'Цена: {item_data.price} руб.\n\n'
                        f'ID: {item_data.id}')
        await callback.message.answer(message_text, reply_markup=admin_kb.item_delete(item_id))


@admin_router.callback_query(F.data.startswith('deleteitem_'))
async def delete_item(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[1])
    async with async_session() as session:
        async with session.begin():
            await orm_delete_product(session, item_id)

    await callback.answer("Товар удален")

    if callback.message.content_type == 'text':
        await callback.message.edit_text("Товар был успешно удален.")
    elif callback.message.content_type in ['photo', 'video', 'audio', 'document']:
        await callback.message.delete()
        await callback.message.answer("Товар был успешно удален.")
    else:
        await callback.message.answer("Неизвестный тип сообщения, но товар был удален.")
