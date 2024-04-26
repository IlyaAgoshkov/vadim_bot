import os
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
import keyboards.kb as kb
import database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f'{message.from_user.full_name}, добро пожаловать в мой мир! \n'
                         'Меня зовут Артем Шамин, заказчики называют меня  «Артем Правша». \n \n'
                         'Искусство, комфорт и качество – вот то, что я вкладываю в каждый предмет мебели, который создаю.',reply_markup=kb.main)


# @router.message(Command('menu'))
# async def menu(message: Message):
#     await bot.edit_message_reply_markup( reply_markup=kb.main)


@router.message(Command('contact'))
async def menu(message: Message):
    await message.answer('Выберите, как хотите связаться с нами:', reply_markup=kb.contact)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.message(F.text == 'Контакты')
async def catalog(message: Message):
    await message.answer('Выберите как хотите связаться с нами', reply_markup=kb.contact)





# @router.message(Command('admin'))
# async def admin_p(message: Message):
#     for admin_id in ADMIN_ID:
#         if message.from_user.id == admin_id:
#             await message.answer('Вы вошли как администратор', reply_markup=kb.admin_panel)


@router.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer()
    if item_data.image:
        file_id = item_data.image
        caption = (f'{item_data.name}\n\n'
                   f'Описание: {item_data.description}\n\n'
                   f'Цена: {item_data.price} руб.')
        await callback.message.answer_photo(photo=file_id, caption=caption, reply_markup=kb.item)
    else:
        message_text = (f'Название: {item_data.name}\n'
                        f'Описание: {item_data.description}\n'
                        f'Цена: {item_data.price} руб.')
        await callback.message.answer(message_text, reply_markup=kb.item)


@router.callback_query(F.Text(startswith="description"))
async def description(callback: CallbackQuery):
    # Разбираем callback_data для получения item_id
    _, item_id = callback.data.split(':')
    item_id = int(item_id)  # Преобразуем item_id в число

    # Запрос к базе данных для получения описания товара по item_id
    item_description = await rq.get_item_description(item_id)

    # Отправляем описание пользователю
    await callback.message.answer(item_description)

