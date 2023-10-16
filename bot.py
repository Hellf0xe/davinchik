import asyncio
from hendlers.reg_user import reg_router
from hendlers.search_form import search_router
from dispatcher import dp,bot
from bd import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
async def timer(delay: float):
    await asyncio.sleep(delay)
    users = get_user_timer()
    for userId in users:
        if get_user_info(userId[0],'timer_num')==6:
            сont_search_keyboard=InlineKeyboardBuilder()
            сont_search_keyboard.add(InlineKeyboardButton(text="Продовжити пошук",callback_data="searchForms"))
            await bot.send_message(userId[0],"off sleep",reply_markup=сont_search_keyboard.as_markup())
            await change_user_info(userId[0],'start_timer','False')
            await change_user_info(userId[0],'timer_num',0)
            await del_forms(userId[0])
            print(f"{get_profile_info(userId[0],'name')}: ending sleep")
        else:
            num=get_user_info(userId[0],'timer_num')
            num+=1
            await change_user_info(userId[0],'timer_num',num)
            print(f"{get_profile_info(userId[0],'name')}: set {get_user_info(userId[0],'timer_num')}")
    await timer(3)
async def main():
    dp.include_routers(search_router,reg_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(dp.start_polling(bot),timer(3))

if __name__ == "__main__":
    asyncio.run(main())