from aiogram.filters.command import Command
from aiogram import F,Router,Bot
from aiogram.types import Message,CallbackQuery
from bd import *
from klava import *
import commands
import random
from .reg_user import cmd_start
search_router=Router()

@search_router.message(F.text=="👎")
async def dislike_form(m:Message):
	if get_user_info(m.chat.id,"type_activ")=="search" and get_user_info(m.chat.id,"id")!=None:
		users=get_user_forms(m.chat.id)
		await commands.userForm(m=m,userId=random.choice(users)[0],keyboard=sF_keyboard.as_markup(resize_keyboard=True))

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