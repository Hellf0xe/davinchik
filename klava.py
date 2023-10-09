from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardMarkup
from bd import *
userForm_keyboard=InlineKeyboardBuilder()
resetForm=InlineKeyboardButton(text="Заповнити анкету заново",callback_data="resetForm")
changePhoto=InlineKeyboardButton(text="Змінити фото",callback_data="changePhoto")
changeDesc=InlineKeyboardButton(text="Змінити текст анкети",callback_data="changeDesc")
searchForms=InlineKeyboardButton(text="Дивитися анкети",callback_data="searchForms")
userForm_keyboard.row(resetForm).row(changePhoto).row(changeDesc).row(searchForms)

choice_gender_keyboard=ReplyKeyboardBuilder()
gender_W=KeyboardButton(text="Я дівчина")
gender_M=KeyboardButton(text="Я хлопець")
choice_gender_keyboard.add(gender_W,gender_M)

sG_keyboard=ReplyKeyboardBuilder()
search_W=KeyboardButton(text="Дівчата")
search_M=KeyboardButton(text="Хлопці")
search_A=KeyboardButton(text="Все одно")
sG_keyboard.add(search_W,search_M,search_A)

sF_keyboard=ReplyKeyboardBuilder()
like_key=KeyboardButton(text="❤️")
dislike_key=KeyboardButton(text="👎")
menu_key=KeyboardButton(text="💤")
sF_keyboard.add(like_key,dislike_key,menu_key)

def menu_keyboard(userId):
    buttons = [
        [InlineKeyboardButton(text="Моя анкета",callback_data="mProfile")],
        [InlineKeyboardButton(text=f"Скрити анкету {'❌'if get_profile_info(userId,'active')=='True'else'✅'}",callback_data="mProfileOff")],
        [searchForms]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

ac_fr_keyboard=InlineKeyboardBuilder()
ac_fr_keyboard.add(InlineKeyboardButton(text="👍",callback_data="searchForms"))

сont_search_keyboard=InlineKeyboardBuilder()
сont_search_keyboard.add(InlineKeyboardButton(text="Продовжити пошук",callback_data="searchForms"))
