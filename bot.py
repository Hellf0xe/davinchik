import asyncio
from hendlers.reg_user import reg_router
from hendlers.search_form import search_router
from dispatcher import dp,bot

async def main():
    
    dp.include_routers(search_router,reg_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())