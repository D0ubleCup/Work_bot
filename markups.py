'''
все кнопки к тг боту
к каждой записи, обязательно добовлять коментарий обозначающий принадлежность к той или иной функции
'''

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

#def start
start_but = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Продолжить', callback_data='continue')
start_but.add(button1)


#def main_info 
info_start_but = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text= 'Работник', callback_data= 'worker')
button2 = InlineKeyboardButton(text= 'Работодатель', callback_data= 'employer')
info_start_but.add(button1, button2)


#def worker_reg_info
info_for_worker_but = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Заполнить анкету регистрации', callback_data='worker_registration')
info_for_worker_but.add(button1)



#def client_reg_info
info_for_client_but = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Заполнить анкету регистрации',callback_data='client_registration')
info_for_client_but.add(button1)


#def send_commands_to_user - для работников 
worker_but = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton('Мой профиль')
button2 = KeyboardButton('Посмотреть заявки на работу')
worker_but.add(button1, button2)

#def worker_prodile
worker_profile_but = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Имя', callback_data='worker_change_name')
button2 = InlineKeyboardButton('Специализацию', callback_data='worker_change_description')
button3 = InlineKeyboardButton('Номер телефона', callback_data='worker_change_phone')
button4 = InlineKeyboardButton('Возраст', callback_data='worker_change_age')
worker_profile_but.add(button1,button2,button3,button4)



#def send_commands_to_user - для заказчиков
client_but = ReplyKeyboardMarkup()
button1 = KeyboardButton('')
button2 = KeyboardButton('Посмотреть заявки на работу')
client_but.add(button1, button2)