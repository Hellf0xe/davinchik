from bd import *
import itertools

users=get_user_forms(1016684077)
for n in get_form_list(1016684077):
    for index in range(0,len(users)):
        # print(n[0],users[index][0])
        if n[0] == users[index][0]:
            users.pop(0)
            break

print(get_liked_form(None,1016684077))
# users.pop(0)
# print(users)
# users.pop(0)
# print(users)