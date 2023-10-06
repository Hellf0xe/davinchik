from aiogram.filters.command import Command
from aiogram import F,Router,Bot
from aiogram.types import Message,CallbackQuery
from bd import *
from klava import *
import commands
import random
reg_router = Router()

async def reg_text(m:Message,text,atype):
    await m.answer(f"Enter {text}")
    await change_user_info(m.chat.id,'type_activ',atype)
async def g_text(m:Message,text,atype,keyboard):
    await m.answer(f"Enter {text}",reply_markup=keyboard)
    await change_user_info(m.chat.id,'type_activ',atype)

@reg_router.message(Command("start"))
async def cmd_start(m: Message):
    if commands.reg_check(m.chat.id):
        await commands.userForm(m,m.chat.id,userForm_keyboard.as_markup())
        await change_user_info(m.chat.id,"type_activ","profile")
    else:
        await create_user(m.chat.id)
        await reg_text(m=m,text="name",atype=commands.action_types.name)
# Entered name
@reg_router.message(F.text)
async def reg_name(m: Message):
    match get_user_info(m.chat.id,"type_activ"):
        case commands.action_types.name:
            await change_profile_info(m.chat.id,'name',m.text)
            await g_text(m=m,text="gender",atype=commands.action_types.gender,keyboard=choice_gender_keyboard.as_markup(resize_keyboard=True))
        case commands.action_types.gender:
            if m.text == "I am Woman" or m.text == "I am Man":
                gen="Woman" if m.text=="I am Woman" else "Man"
                await change_profile_info(m.chat.id,'gender',gen)
                await g_text(m=m,text="search gender",atype=commands.action_types.searchGender,keyboard=sG_keyboard.as_markup(resize_keyboard=True))
            else:
                await m.answer("ERROR")
        case commands.action_types.searchGender:
            if m.text == "Woman" or m.text == "Man" or m.text == "Any":
                await change_profile_info(m.chat.id,'search_gender',m.text)
                await g_text(m=m,text="age",atype=commands.action_types.age,keyboard=ReplyKeyboardRemove())
            else:
                await m.answer("ERROR")
        case commands.action_types.age:
            if m.text.isdigit() and int(m.text)<100:
                await change_profile_info(m.chat.id,'age',m.text)
                await reg_text(m=m,text="speciality",atype=commands.action_types.speciality)
            else:
                await m.answer("ERROR")
        case commands.action_types.speciality:
            if m.text in commands.speciality_list:
                await change_profile_info(m.chat.id,'speciality',m.text)
                await reg_text(m=m,text="description",atype=commands.action_types.description)
            else:
                await m.answer("ERROR")
        case commands.action_types.description:
            await change_profile_info(m.chat.id,'description',m.text)
            await reg_text(m=m,text="photo",atype=commands.action_types.photoUser)
        case commands.action_types.changeDescription:
            await change_profile_info(m.chat.id,'description',m.text)
            await commands.userForm(m,m.chat.id,userForm_keyboard.as_markup())


@reg_router.message(F.photo)
async def reg_photo(m: Message,bot: Bot):
    if get_user_info(m.chat.id,"type_activ")==commands.action_types.photoUser:
        await bot.download(
        m.photo[-1],
        destination=f"userPhoto/{m.chat.id}.jpg"
        )
        await change_profile_info(m.chat.id,'photo',f"/userPhoto/{m.chat.id}.jpg")
        await commands.userForm(m,m.chat.id,userForm_keyboard.as_markup())
        await change_user_info(m.chat.id,"type_activ","profile")
        
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
        await reg_text(m=c.message,text="description",atype=commands.action_types.changeDescription)

@reg_router.callback_query(F.data == "searchForms")
async def search_form(c:CallbackQuery):
    if get_user_info(c.message.chat.id,"type_activ")=="profile" and get_user_info(c.message.chat.id,"id")!=None or get_user_info(c.message.chat.id,"type_activ")=="menu" and get_user_info(c.message.chat.id,"id")!=None:
        await change_profile_info(c.message.chat.id,'active','True')
        users=get_user_forms(c.message.chat.id)
        if users!=[]:
            await commands.userForm(m=c.message,userId=random.choice(users)[0],keyboard=sF_keyboard.as_markup(resize_keyboard=True))
            await change_user_info(c.message.chat.id,"type_activ","search")
        else:
            await c.answer("No Form")
