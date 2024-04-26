from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.requests import get_categories, get_category_item, get_item_description

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог'),
                                     KeyboardButton(text='Корзина')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


admin_panel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Добавить товар')],
                                     [KeyboardButton(text='Удалить товар')],
                                     [KeyboardButton(text='Изменить товар')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


contact = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ВКонтакте', callback_data="vk", url='https://vk.com/artempravsha')],
    [InlineKeyboardButton(text='Telegram', callback_data='tg', url='https://t.me/artempravsha')],
    [InlineKeyboardButton(text='E-mail', callback_data="E-mail")],
    [InlineKeyboardButton(text='WhatsApp', callback_data="WhatsApp", url='https://wa.me/+79186626909')],
    [InlineKeyboardButton(text='Наш сайт', callback_data="Site", url='https://artempravsha.ru/')]])

item = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔍Описание', callback_data=f'description'),
     InlineKeyboardButton(text='🛒В корзину', callback_data='add to cart')],
])