from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.requests import get_categories, get_category_item

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог'),
                                     KeyboardButton(text='Корзина')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"categoryuser_{category.id}"))
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


contact = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ВКонтакте', callback_data="vk", url=''),
     InlineKeyboardButton(text='Telegram', callback_data='tg', url='')],
    [InlineKeyboardButton(text='WhatsApp', callback_data="WhatsApp", url=''),
     InlineKeyboardButton(text='Наш сайт', callback_data="Site", url='')]])

item = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛒В корзину', callback_data='add to cart')],
])