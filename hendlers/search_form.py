from aiogram.filters.command import Command
from aiogram import F,Router,Bot
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
			await delete_liked(get_user_info(m.chat.id,'current_ac'))
		await commands.search(m=m,keyboard=sF_keyboard.as_markup(resize_keyboard=True))

@search_router.message(F.text=="💤")
async def menu(m:Message):
	if get_user_info(m.chat.id,"type_activ")=="search" and get_user_info(m.chat.id,"id")!=None:
		await m.answer("Почекаємо поки хтось побачить твою анкету",reply_markup=ReplyKeyboardRemove())
		await m.answer("----------------Навігація----------------",reply_markup=menu_keyboard(m.chat.id))
		await change_user_info(m.chat.id,"type_activ","menu")

@search_router.callback_query(F.data == "mProfile")
async def profile(c:CallbackQuery):
	if get_user_info(c.message.chat.id,"type_activ")=="menu" and get_user_info(c.message.chat.id,"id")!=None:
		await cmd_start(m=c.message)

@search_router.callback_query(F.data == "mProfileOff")
async def off_profile(c:CallbackQuery):
	if get_user_info(c.message.chat.id,"type_activ")=="menu" and get_user_info(c.message.chat.id,"id")!=None:
		if get_profile_info(c.message.chat.id,'active')=='True':
			await change_profile_info(c.message.chat.id,'active','False')
		else:
			await change_profile_info(c.message.chat.id,'active','True')
		await c.message.edit_text("----------------Навігація----------------",reply_markup=menu_keyboard(c.message.chat.id))

@search_router.message(F.text=="❤️")
async def dislike_form(m:Message):
	if get_user_info(m.chat.id,"type_activ")=="search" and get_user_info(m.chat.id,"id")!=None:
		if get_liked_form(get_user_info(m.chat.id,'current_ac'),m.chat.id)!=None:
			await bot.send_message(chat_id=get_user_info(m.chat.id,'current_ac'),text=f"@{get_user_info(m.chat.id,'nick')}")
			await m.answer(f"@{get_user_info(get_user_info(m.chat.id,'current_ac'),'nick')}")
		else:
			if get_liked_form(m.chat.id,get_user_info(m.chat.id,'current_ac'))==None:
				await add_liked_form(m.chat.id)
				await bot.send_message(chat_id=get_user_info(m.chat.id,'current_ac'),
													text=f"Ти сподобався {len(get_liked_form(None,get_user_info(m.chat.id,'current_ac')))} людині, показати її?",reply_markup=ac_fr_keyboard(m.chat.id))
				await change_user_info(get_user_info(m.chat.id,'current_ac'),'type_activ','menu')
			await commands.search(m=m,keyboard=sF_keyboard.as_markup(resize_keyboard=True))