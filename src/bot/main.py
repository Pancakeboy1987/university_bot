import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from src.bot.handlers import handlers_router as router


async def main():
    load_dotenv()

    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass