from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from bd import *
from klava import *
import commands
from .reg_user import cmd_start
from dispatcher import bot

search_router=Router()

@search_router.message(F.text=="👎")
async def dislike_form(m:Message):
	if get_user_info(m.chat.id,"type_activ")=="search" and get_user_info(m.chat.id,"id")!=None:
		if get_liked_form(get_user_info(m.chat.id,'current_ac'),m.chat.id)!=None:
			await delete_liked(m.chat.id,get_user_info(m.chat.id,'current_ac'))
		await commands.search(m=m,keyboard=sF_keyboard.as_markup(resize_keyboard=True))

@search_router.message(F.text=="💤")
async def menu(m:Message):
	if get_user_info(m.chat.id,"type_activ")=="search" and get_user_info(m.chat.id,"id")!=None:
		await m.answer("Почекаємо поки хтось побачить твою анкету",reply_markup=ReplyKeyboardRemove())
		await m.answer("➖➖📜Меню📜➖➖",reply_markup=menu_keyboard(m.chat.id))
		await change_user_info(m.chat.id,"type_activ","menu")

@search_router.callback_query(F.data == "mProfile")
async def profile(c:CallbackQuery):
	if get_user_info(c.message.chat.id,"type_activ")=="menu" and get_user_info(c.message.chat.id,"id")!=None:
		await cmd_start(m=c.message)

@search_router.message(F.text=="❤️")
async def dislike_form(m:Message):
	if get_user_info(m.chat.id,"type_activ")=="search" and get_user_info(m.chat.id,"id")!=None:
		cur_u=get_user_info(m.chat.id,'current_ac')
		if get_liked_form(cur_u,m.chat.id)!=None:
			lu_photo = commands.FSInputFile(f"userPhoto/{m.chat.id}.jpg")
			lu=get_profile_info(m.chat.id,"*")
			await bot.send_photo(chat_id=cur_u,
													photo=lu_photo,
													caption=commands.user_form.format(name=lu[1],age=lu[2],speciality=commands.speciality_list[lu[3]],description=lu[4]),
        reply_markup=ReplyKeyboardRemove())
			await bot.send_message(chat_id=get_user_info(m.chat.id,'current_ac'),text=f"💞Є взаємна симпатія! Починай спілкуватися @{get_user_info(m.chat.id,'nick')}",reply_markup=сont_search_keyboard.as_markup())
			await m.answer("🎉",reply_markup=ReplyKeyboardRemove())
			await m.answer(f"Супер! Сподіваюсь, гарно проведете час ;) Починай спілкуватися @{get_user_info(get_user_info(m.chat.id,'current_ac'),'nick')}",reply_markup=сont_search_keyboard.as_markup())
			await change_user_info(cur_u,'type_activ','menu')
			await change_user_info(m.chat.id,'type_activ','menu')
			await delete_liked(m.chat.id,get_user_info(m.chat.id,'current_ac'))
		else:
			if get_liked_form(m.chat.id,get_user_info(m.chat.id,'current_ac'))==None:
				await add_liked_form(m.chat.id)
				await bot.send_message(chat_id=get_user_info(m.chat.id,'current_ac'),
													text=f"Ти сподобався {len(get_liked_form(None,get_user_info(m.chat.id,'current_ac')))} людині, показати її?",reply_markup=ac_fr_keyboard.as_markup())
				await change_user_info(get_user_info(m.chat.id,'current_ac'),'type_activ','menu')
			await commands.search(m=m,keyboard=sF_keyboard.as_markup(resize_keyboard=True))