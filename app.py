# app.py

# Модули по умолчанию
import asyncio
import os
from datetime import datetime

# Сторонние модули
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

# Загружаем переменные окружения
load_dotenv(find_dotenv())

# Мои модули
from handlers import user_private, user_group, admin_private
from middlewares.db import DataBaseSession
from database.engine import create_db, drop_db, session_maker


bot = Bot(token = os.getenv("TOKEN"), parse_mode = "HTML")

dp = Dispatcher()
dp.include_routers(
    user_private.router,
    user_group.router,
    admin_private.router
)


async def on_startup(bot):
    run_param = False  # Заменяем на True, если надо дропнуть БД

    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print("Bot shutdown")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool = session_maker))

    await bot.delete_webhook(drop_pending_updates = True)

    time_now = datetime.today()
    print(f"[{str(time_now)[:19]}]: Bot started")
    
    # В параметр allowed_updates передаём типы сообщений,
    # которые бот может обрабатывать
    await dp.start_polling(
        bot, allowed_updates = dp.resolve_used_update_types()
    )


# Запуск бота
if __name__ == "__main__":
    try:
        # Чтобы не было ошибки RuntimeError
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    
    except KeyboardInterrupt:
        print("Bot stopped")
