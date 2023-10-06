import asyncio
from aiogram import Bot, Dispatcher
from hendlers.reg_user import reg_router
from hendlers.search_form import search_router
from config import BOT_API
async def main():
    bot = Bot(token=BOT_API)
    dp = Dispatcher()
    dp.include_routers(search_router,reg_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())