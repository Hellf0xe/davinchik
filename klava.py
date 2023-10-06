from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardMarkup
from bd import *
userForm_keyboard=InlineKeyboardBuilder()
resetForm=InlineKeyboardButton(text="Reset form",callback_data="resetForm")
changePhoto=InlineKeyboardButton(text="Change photo",callback_data="changePhoto")
changeDesc=InlineKeyboardButton(text="Change description",callback_data="changeDesc")
searchForms=InlineKeyboardButton(text="Дивитися анкети",callback_data="searchForms")
userForm_keyboard.row(resetForm).row(changePhoto).row(changeDesc).row(searchForms)

choice_gender_keyboard=ReplyKeyboardBuilder()
gender_W=KeyboardButton(text="I am Woman")
gender_M=KeyboardButton(text="I am Man")
choice_gender_keyboard.add(gender_W,gender_M)

sG_keyboard=ReplyKeyboardBuilder()
search_W=KeyboardButton(text="Woman")
search_M=KeyboardButton(text="Man")
search_A=KeyboardButton(text="Any")
sG_keyboard.add(search_W,search_M,search_A)

sF_keyboard=ReplyKeyboardBuilder()
like_key=KeyboardButton(text="❤️")
dislike_key=KeyboardButton(text="👎")
menu_key=KeyboardButton(text="💤")
sF_keyboard.add(like_key,dislike_key,menu_key)

def menu_keyboard(userId):
    buttons = [
        [InlineKeyboardButton(text=" Моя анкета",callback_data="mProfile")],
        [InlineKeyboardButton(text=f"Скрити анкету {'❌'if get_profile_info(userId,'active')=='True'else'✅'}",callback_data="mProfileOff")],
        [searchForms]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard