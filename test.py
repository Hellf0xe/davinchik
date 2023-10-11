while(True):
	text=input("Enter: ")
	if len(text)==5 and text[2]=="-" and text[:2].isdigit() and text[3:].isdigit() and int(text[:2])>=17 and int(text[3:])<=30:
		print("true")
	else:
		print("false")
	