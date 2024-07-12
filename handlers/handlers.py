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
                         'Меня зовут Вадим, люблю делать всякие приколные штуки». \n \n'
                         'Заглядывай в каталог и ознакомься ', reply_markup=kb.main)


@router.message(Command('catalog'))
async def menu(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.message(Command('contact'))
async def menu(message: Message):
    await message.answer('Выберите, как хотите связаться с нами:', reply_markup=kb.contact)

@router.message(Command('id'))
async def send_user_id(message: Message):
    user_id = message.from_user.id
    await message.reply(f"Твой ID: {user_id}")
@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.message(F.text == 'Контакты')
async def catalog(message: Message):
    await message.answer('Выберите как хотите связаться с нами', reply_markup=kb.contact)


@router.message(Command('about'))
async def about(message: Message):
    await message.answer('________\n\n'
                        '_____\n')





# @router.message(F.photo)
# async def get_photo_id(message: Message):
#     await message.answer(f'ID фото: {message.photo[-1].file_id}')


@router.callback_query(F.data.startswith('categoryuser_'))
async def category(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery):
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
    _, item_id = callback.data.split(':')
    item_id = int(item_id)

    item_description = await rq.get_item_description(item_id)

    await callback.message.answer(item_description)


@router.callback_query(F.data.startswith('to_main'))
async def to_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите категорию', reply_markup=await kb.categories())
