from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardMarkup
from bd import *
searchForms=InlineKeyboardButton(text="Дивитися анкети",callback_data="searchForms")
def profile_keyboard(userId):
    menu_buttons = [
        [InlineKeyboardButton(text="Налаштунки профілю",callback_data="profileSettings")],
        [InlineKeyboardButton(text="Параметри пошуку",callback_data="searchOptions")],
        [searchForms]
    ]
    menuSettings_buttons = [
        [InlineKeyboardButton(text="Заповнити анкету заново",callback_data="resetForm")],
        [InlineKeyboardButton(text="Змінити фото",callback_data="changePhoto")],
        [InlineKeyboardButton(text="Змінити текст анкети",callback_data="changeDesc")],
        [InlineKeyboardButton(text=f"Скрити анкету {'❌'if get_profile_info(userId,'active')=='True'else'✅'}",callback_data="mProfileOff")],
        [InlineKeyboardButton(text="Назад◀️", callback_data="backToProfile")]
    ]
    menuSearch_buttons = [
        [InlineKeyboardButton(text=f"Cтать:{'Дівчата' if get_profile_info(userId,'search_gender')=='Woman' else 'Хлопці' if get_profile_info(userId,'search_gender')=='Man' else 'Все одно'}",callback_data="changeSearchGen")],
        [InlineKeyboardButton(text="Діапозон віку",callback_data="changeDiap")],
        [
            InlineKeyboardButton(text=f"{get_profile_info(userId,'min_age')}",callback_data="changeDiap"),
            InlineKeyboardButton(text="-",callback_data="changeDiap"),
            InlineKeyboardButton(text=f"{get_profile_info(userId,'max_age')}",callback_data="changeDiap")
        ],
        [InlineKeyboardButton(text="Назад◀️", callback_data="backToProfile")]
    ]
    buttons=menu_buttons if get_user_info(userId,'type_activ')=="profile" else menuSettings_buttons if get_user_info(userId,'type_activ')=="profileSetting" else menuSearch_buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


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
        [searchForms]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

ac_fr_keyboard=InlineKeyboardBuilder()
ac_fr_keyboard.add(InlineKeyboardButton(text="👍",callback_data="searchForms"))

сont_search_keyboard=InlineKeyboardBuilder()
сont_search_keyboard.add(InlineKeyboardButton(text="Продовжити пошук",callback_data="searchForms"))
