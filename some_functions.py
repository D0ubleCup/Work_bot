def phone_validator(str):
	return ((len(str)>=11) and (len(str)<=12) and (str[0]=='+' or str[0]=='8'))

def age_validator(age):
	if age.isnumeric():
		age = int(age)
		return (age>10 and age<70)
	else :
		return False
	
