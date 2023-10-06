from bd import *
import json
from aiogram.types import FSInputFile, Message

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

user_form="{name},{age},{speciality} - {description}"


async def userForm(m:Message,userId,keyboard):
    user_photo = FSInputFile(f"userPhoto/{userId}.jpg")
    user=get_profile_info(userId,"*")
    await m.answer_photo(
        user_photo,
        caption=user_form.format(name=user[1],age=user[2],speciality=speciality_list[user[3]],description=user[4]),
        reply_markup=keyboard
    )
    