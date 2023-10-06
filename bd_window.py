from bd import *
import os

while(True):
	name=input("Enter name:")
	userId=cur.execute(f"SELECT id FROM profile WHERE name=?",(name,)).fetchone()[0]
	cur.execute(f"DELETE from profile where id = {userId}")
	cur.execute(f"DELETE from user_info where id = {userId}")
	db.commit()
	os.remove(f"userPhoto/{userId}.jpg")