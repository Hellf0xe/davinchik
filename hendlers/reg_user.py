from aiogram.filters.command import Command
from aiogram import F,Router,Bot
from aiogram.types import Message,CallbackQuery
from bd import *
from klava import *
import commands
reg_router = Router()

async def reg_text(m:Message,text,atype):
    await m.answer("Як до тебе звертатись?")
    await change_user_info(m.chat.id,'type_activ',atype)
async def g_text(m:Message,text,atype,keyboard):
    await m.answer(f"Enter {text}",reply_markup=keyboard)
    await change_user_info(m.chat.id,'type_activ',atype)

@reg_router.message(Command("start"))
async def cmd_start(m: Message):
    if m.chat.id == 439258383:
        await m.answer("Иди нахуй")
    else:
        if commands.reg_check(m.chat.id):
            await change_user_info(m.chat.id,"type_activ","profile")
            await commands.userForm(m,m.chat.id,profile_keyboard(m.chat.id))
        else:
            await create_user(m.chat.id,m.from_user.username)
            await m.answer("Як до тебе звертатись?")
            await change_user_info(m.chat.id,'type_activ',commands.action_types.name)
# Entered name
@reg_router.message(F.text)
async def reg_name(m: Message):
    match get_user_info(m.chat.id,"type_activ"):
        case commands.action_types.name:
            await change_profile_info(m.chat.id,'name',m.text)
            await m.answer("Скільки тобі років?🔞")
            await change_user_info(m.chat.id,'type_activ',commands.action_types.age)
        case commands.action_types.age:
            if m.text.isdigit() and int(m.text)<100:
                await change_profile_info(m.chat.id,'age',m.text)
                await m.answer("Яка в тебе спеціальність? (приклад - 123)")
                await change_user_info(m.chat.id,'type_activ',commands.action_types.speciality)
            else:
                await m.answer("ERROR")
        case commands.action_types.speciality:
            if m.text in commands.speciality_list:
                await change_profile_info(m.chat.id,'speciality',m.text)
                await m.answer("Розкажи про себе, кого хочеш знайти, чим пропонуєш зайнятись.\nЦе допоможе краще підібрати тобі компанію🫂")
                await change_user_info(m.chat.id,'type_activ',commands.action_types.description)
            else:
                await m.answer("ERROR")
        case commands.action_types.description:
            await change_profile_info(m.chat.id,'description',m.text)
            await m.answer("Тепер обери стать👩‍❤️‍💋‍👨", reply_markup=choice_gender_keyboard.as_markup(resize_keyboard=True))
            await change_user_info(m.chat.id,'type_activ',commands.action_types.gender)
        case commands.action_types.gender:
            if m.text == "Я дівчина" or m.text == "Я хлопець":
                gen="Woman" if m.text=="Я дівчина" else "Man"
                await change_profile_info(m.chat.id,'gender',gen)
                await m.answer("Тепер надійшли фото, його побачать інші користувачі📸",reply_markup=ReplyKeyboardRemove())
                await change_user_info(m.chat.id,'type_activ',commands.action_types.photoUser)
            else:
                await m.answer("ERROR")
        case commands.action_types.searchGender:
            if m.text == "Дівчата" or m.text == "Хлопці" or m.text == "Все одно":
                gen="Woman" if m.text=="Дівчата" else "Man" if m.text=="Хлопці" else "Any"
                await change_profile_info(m.chat.id,'search_gender',gen)
                await m.answer("Який діапозон віку тобі підходить?(приклад:17-20)",reply_markup=ReplyKeyboardRemove())
                await change_user_info(m.chat.id,'type_activ',"d_age")
            else:
                await m.answer("ERROR")
        case "d_age":
            text=m.text
            if len(text)==5 and text[2]=="-" and text[:2].isdigit() and text[3:].isdigit() and int(text[:2])>=17 and int(text[3:])<=30:
                await change_profile_info(m.chat.id,'min_age',text[:2])
                await change_profile_info(m.chat.id,'max_age',text[3:])
                await commands.userForm(m,m.chat.id,profile_keyboard(m.chat.id))
            else:
                await m.answer("ERROR")
        case commands.action_types.changeDescription:
            await change_profile_info(m.chat.id,'description',m.text)
            await change_user_info(m.chat.id,'type_activ',"profile")
            await commands.userForm(m,m.chat.id,profile_keyboard(m.chat.id))


@reg_router.message(F.photo)
async def reg_photo(m: Message,bot: Bot):
    if get_user_info(m.chat.id,"type_activ")==commands.action_types.photoUser:
        await bot.download(
        m.photo[-1],
        destination=f"userPhoto/{m.chat.id}.jpg"
        )
        await change_profile_info(m.chat.id,'photo',f"/userPhoto/{m.chat.id}.jpg")
        await m.answer("Супер!🎉\nПрофиль готов, тепер давай налаштуємо для тебе пошук.🔍")
        await m.answer("Хто тебе цікавить?🤩",reply_markup=sG_keyboard.as_markup(resize_keyboard=True))
        await change_user_info(m.chat.id,"type_activ",commands.action_types.searchGender)
        
@reg_router.callback_query(F.data == "resetForm")
async def reset_form(c:CallbackQuery):
    if get_user_info(c.message.chat.id,"type_activ")=="profile" and get_user_info(c.message.chat.id,"id")!=None:
        await delete_user(c.message.chat.id)
        await cmd_start(c.message)

@reg_router.callback_query(F.data == "changePhoto")
async def change_photo(c:CallbackQuery):
    if get_user_info(c.message.chat.id,"type_activ")=="profile" and get_user_info(c.message.chat.id,"id")!=None:
        await reg_text(m=c.message,text="photo",atype=commands.action_types.photoUser)
    
@reg_router.callback_query(F.data == "changeDesc")
async def change_desc(c:CallbackQuery):
    if get_user_info(c.message.chat.id,"type_activ")=="profile" and get_user_info(c.message.chat.id,"id")!=None:
        await c.message.answer("Розкажи про себе, кого хочеш знайти, чим пропонуєш зайнятись.\nЦе допоможе краще підібрати тобі компанію🫂")
        await change_user_info(c.message.chat.id,'type_activ',commands.action_types.changeDescription)

@reg_router.callback_query(F.data == "searchForms")
async def search_form(c:CallbackQuery):
    if get_user_info(c.message.chat.id,"type_activ")=="profile" and get_user_info(c.message.chat.id,"id")!=None or get_user_info(c.message.chat.id,"type_activ")=="menu" and get_user_info(c.message.chat.id,"id")!=None:
        await commands.search(m=c.message,keyboard=sF_keyboard.as_markup(resize_keyboard=True))

@reg_router.callback_query(F.data == "profileSettings")
async def profileSettings (c:CallbackQuery):
    user=get_profile_info(c.message.chat.id,"*")
    await change_user_info(c.message.chat.id,'type_activ','profileSetting')
    await c.message.edit_caption(caption=commands.user_form.format(name=user[1],age=user[2],speciality=commands.speciality_list[user[3]],description=user[4])+"\n\nНалаштунки профілю",reply_markup=profile_keyboard(c.message.chat.id))

@reg_router.callback_query(F.data == "searchOptions")
async def profileSettings (c:CallbackQuery):
    user=get_profile_info(c.message.chat.id,"*")
    await change_user_info(c.message.chat.id,'type_activ','profileSearch')
    await c.message.edit_caption(caption=commands.user_form.format(name=user[1],age=user[2],speciality=commands.speciality_list[user[3]],description=user[4])+"\n\nПараметри пошуку",reply_markup=profile_keyboard(c.message.chat.id))

@reg_router.callback_query(F.data == "backToProfile")
async def profileSettings (c:CallbackQuery):
    user=get_profile_info(c.message.chat.id,"*")
    await change_user_info(c.message.chat.id,'type_activ','profile')
    await c.message.edit_caption(caption=commands.user_form.format(name=user[1],age=user[2],speciality=commands.speciality_list[user[3]],description=user[4]),reply_markup=profile_keyboard(c.message.chat.id))
