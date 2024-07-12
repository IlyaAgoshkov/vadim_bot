from aiogram import Router, F, types
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from config.config import ADMIN_ID
import database.requests as rq
from admin import admin_kb
from database.orm_query import orm_delete_product, orm_add_product, orm_delete_category
from database.models import Item, AsyncSessionLocal, Category
from database.models import async_session

admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer("Что хотите сделать?", reply_markup=admin_kb.admin_panel)

@admin_router.message(F.text == 'Удалить товар')
async def catalog(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer('Выберите категорию', reply_markup=await admin_kb.categories_to_delete_item())

@admin_router.message(F.text == 'Удалить категорию и товары в ней')
async def delete_category_start(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer('Выберите категорию для удаления', reply_markup=await admin_kb.categories())

@admin_router.callback_query(F.data.startswith('categoryadmin_'))
async def delete_category(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    async with async_session() as session:
        async with session.begin():
            await orm_delete_category(session, category_id)

    await callback.answer("Категория и все товары в ней удалены.")
    await callback.message.edit_text("Категория и все товары в ней были успешно удалены.")

@admin_router.callback_query(F.data.startswith('itemcategory_'))
async def item_category(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    await callback.message.edit_text('Выберите товар для удаления', reply_markup=await admin_kb.items(category_id))

@admin_router.callback_query(F.data.startswith('itemadmin_'))
async def item(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[1])
    item_data = await rq.get_item(item_id)
    await callback.answer()
    if item_data.image:
        file_id = item_data.image
        caption = (f'{item_data.name}\n\n'
                   f'Описание: {item_data.description}\n\n'
                   f'Цена: {item_data.price} руб.\n\n')
        await callback.message.answer_photo(photo=file_id, caption=caption, reply_markup=admin_kb.item_delete(item_id))
    else:
        message_text = (f'Название: {item_data.name}\n'
                        f'Описание: {item_data.description}\n'
                        f'Цена: {item_data.price} руб.\n\n')
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


@admin_router.callback_query(F.data.startswith('tomainadmin_'))
async def to_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите товар для удаления', reply_markup=await admin_kb.categories_to_delete_item())
class AddProductForm(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    image = State()

storage = MemoryStorage()

@admin_router.message(F.text == 'Добавить товар')
async def cmd_add_product(message: types.Message, state: FSMContext):
    await state.set_state(AddProductForm.category)
    await message.reply("Введите название категории для товара:")

@admin_router.message(AddProductForm.category)
async def process_category(message: types.Message, state: FSMContext):
    category_name = message.text
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category).where(Category.name == category_name))
        category = result.scalars().first()
        if not category:
            category = Category(name=category_name)
            session.add(category)
            await session.commit()
            await session.refresh(category)
    await state.update_data(category=category.id)
    await state.set_state(AddProductForm.name)
    await message.reply("Введите название товара:")

@admin_router.message(AddProductForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProductForm.description)
    await message.reply("Введите описание товара:")

@admin_router.message(AddProductForm.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProductForm.price)
    await message.reply("Введите цену товара:")

@admin_router.message(AddProductForm.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await state.set_state(AddProductForm.image)
    await message.reply("Отправьте изображение товара:")

@admin_router.message(AddProductForm.image)
async def process_image(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        await state.update_data(image=file_id)

        user_data = await state.get_data()

        async with AsyncSessionLocal() as session:
            await orm_add_product(session, user_data)

        await state.clear()
        await message.reply("Товар был успешно добавлен.")
    else:
        await message.reply("Пожалуйста, отправьте изображение товара.")
