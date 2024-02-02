import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import user
from config.cfg import load_config

logging.basicConfig(level=logging.INFO)
config = load_config()
bot_token = config.tg_bot.token

async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(user.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
