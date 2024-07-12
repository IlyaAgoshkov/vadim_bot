from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import get_categories, get_category_item

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Добавить товар')],
        [KeyboardButton(text='Удалить товар')],
        [KeyboardButton(text='Удалить категорию и товары в ней')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню...'
)





async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"categoryadmin_{category.id}"))
    return keyboard.adjust(2).as_markup()

async def categories_to_delete_item():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"itemcategory_{category.id}"))
    return keyboard.adjust(2).as_markup()

async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"itemadmin_{item.id}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="tomainadmin_"))
    return keyboard.adjust(2).as_markup()

def item_delete(item_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"deleteitem_{item_id}"))
    InlineKeyboardButton(text="Назад", callback_data="to_main_admin")
    return keyboard.as_markup()