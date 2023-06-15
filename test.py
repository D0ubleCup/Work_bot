'''
файл для того что бы тестировать возможные решения и вспоминать как это все же работает
Ну ты сам знаешь 
'''

def norm_mob(str):
	
    return ((len(str)>=11) and (len(str)<=12) and (str[0]=='+') or (str[0]=='8'))
phone='89061071451'	    
print(norm_mob(phone))  
