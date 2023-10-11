import sqlite3 as sq
import os

global db, cur
db = sq.connect('./data/bot.db')
cur = db.cursor()

async def create_user(user_id,nick):
    cur.execute(f"INSERT INTO user_info VALUES(?,'none',0,'{nick}')",(user_id,))
    cur.execute("INSERT INTO profile VALUES(?,'none',0,'none','none','none','none','none','True',0,0)",(user_id,))
    db.commit()

# User Info bd


def get_user_info(user_id, name_info):
    
    if user_id != None:
        if name_info == "*":
            return cur.execute(f"SELECT {name_info} FROM user_info WHERE id=?",(user_id,)).fetchone()
        else:
            return cur.execute(f"SELECT {name_info} FROM user_info WHERE id=?",(user_id,)).fetchone()[0]
    else:
        return cur.execute(f"SELECT {name_info} FROM user_info").fetchall()


async def change_user_info(user_id, name_info, value):
    cur.execute(f"UPDATE user_info SET {name_info} = ? WHERE id = ?", (value,user_id))
    db.commit()

# Profile Info bd


def get_profile_info(userId, name_info):
    if id != None:
        if name_info == "*":
            return cur.execute(f"SELECT {name_info} FROM profile WHERE id=?",(userId,)).fetchone()
        else:
            return cur.execute(f"SELECT {name_info} FROM profile WHERE id=?",(userId,)).fetchone()[0]
    else:
        return cur.execute(f"SELECT {name_info} FROM profile").fetchall()


async def change_profile_info(userId, name_info, value):
    cur.execute(f"UPDATE profile SET {name_info} = ? WHERE id = ?", (value,userId))
    db.commit()

def get_user_forms(userId):
    age=get_profile_info(userId,"age")
    return cur.execute(f"SELECT * FROM profile WHERE id!=? AND active='True' AND photo!='none'", (userId,)).fetchall()

async def delete_user(userId):
    cur.execute(f"DELETE from profile where id = {userId}")
    cur.execute(f"DELETE from user_info where id = {userId}")
    db.commit()
    os.remove(f"userPhoto/{userId}.jpg")

async def add_liked_form(userId):
    liked_user=get_user_info(userId,'current_ac')
    cur.execute("INSERT INTO liked_form VALUES(?,?)",(liked_user,userId))
    db.commit()

def get_liked_form(userId,liked_user):
    if userId!=None:
        return cur.execute("SELECT * FROM liked_form WHERE id=? AND liked_user=?",(liked_user,userId)).fetchone()
    else:
        return cur.execute(f"SELECT * FROM liked_form WHERE id=?", (liked_user,)).fetchall()
async def delete_liked(userId):
    cur.execute(f"DELETE from liked_form where liked_user = {userId}")