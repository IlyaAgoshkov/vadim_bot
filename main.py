import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.methods import DeleteWebhook
from dotenv import load_dotenv
from handlers.handlers import router
from admin.admin import admin_router
from database.models import async_main
from config.command_list import private



async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(admin_router)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
