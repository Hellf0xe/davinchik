from bd import *
import json,random,time
from aiogram.types import FSInputFile, Message
from klava import ReplyKeyboardRemove, profile_keyboard
def reg_check(id):
    userlist = get_user_info(None, "id")
    check_id = False
    for item in userlist:
        if item[0] == id:
            check_id = True
            break
    return check_id

class action_types:
    name="regName"
    age="regAge"
    description="regDescription"
    speciality="regSpeciality"
    photoUser="regPhoto"
    changeDescription="changeDescription"
    gender="regGender"
    searchGender="regSearchGender"

with open("./data/specialties.json", "r", encoding="UTF-8") as f:
    speciality_list = json.load(f)

user_form="{name}, {age}, {speciality} - {description}{text}"


async def userForm(m:Message,userId,keyboard):
    user_photo = FSInputFile(f"userPhoto/{userId}.jpg")
    user=get_profile_info(userId,"*")
    text="\n\nНалаштунки профілю" if get_user_info(m.chat.id,"type_activ")=="profileSetting" else "\n\nПараметри пошуку" if get_user_info(m.chat.id,"type_activ")=="profileSearch" else ""
    await m.answer_photo(
        user_photo,
        caption=user_form.format(name=user[1],age=user[2],speciality=speciality_list[user[3]],description=user[4],text=text),
        reply_markup=keyboard
    )
async def search(m:Message,keyboard):
    await change_profile_info(m.chat.id,'active','True')
    liked_list=get_liked_form(None,m.chat.id)
    users=get_user_forms(m.chat.id)
    for n in get_form_list(m.chat.id):
        for index in range(0,len(users)):
            if n[0] == users[index][0]:
                users.pop(index)
                break
    if liked_list!=[] or users!=[]:
        userId=liked_list[0][1]if liked_list!=[] else random.choice(users)[0]
        await change_user_info(m.chat.id,"current_ac",userId)
        await set_form(m.chat.id,userId)
        await userForm(m=m,userId=userId,keyboard=keyboard)
        await change_user_info(m.chat.id,"type_activ","search")
    else:
        if get_user_forms(m.chat.id)!=[] and users==[]:
            if get_user_info(m.chat.id,'start_timer')=="False": await change_user_info(m.chat.id,'start_timer','True')
            mess=await m.answer("Ви подивилися усі доступні анкети. Ми повідомимо коли ви зможете дивитися анкети знову",reply_markup=ReplyKeyboardRemove())
            if get_user_info(m.chat.id,"type_activ")=='search':
                await change_user_info(m.chat.id,"type_activ","profile")
                await userForm(m,m.chat.id,profile_keyboard(m.chat.id))
            time.sleep(2)
            await mess.delete()
        else:
            mess=await m.answer("Немає належних анкет:(")
            time.sleep(2)
            await mess.delete()