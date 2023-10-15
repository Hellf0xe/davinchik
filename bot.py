import asyncio
from hendlers.reg_user import reg_router
from hendlers.search_form import search_router
from dispatcher import dp,bot

async def timer(delay: float):
    await asyncio.sleep(delay)
    await timer(1)

async def main():
    dp.include_routers(search_router,reg_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(dp.start_polling(bot),timer(1))

if __name__ == "__main__":
    asyncio.run(main())