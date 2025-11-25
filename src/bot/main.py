import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from src.bot.handlers import handlers_router as router


async def main():
    load_dotenv()   # Загрузка переменных окружения из .env

    bot = Bot(token=os.getenv("TOKEN"))  # Получение токена
    dp = Dispatcher()

    dp.include_router(router)   # Подключение роутера
    await dp.start_polling(bot) # Запуск бота в режиме общения с серверами ТГ
                                # (т.е. бот не ждёт данных от сервера, а сам их запрашивает)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
