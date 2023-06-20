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
worker_but = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Мой профиль', callback_data='change_profile')
button2 = InlineKeyboardButton('Посмотреть заявки на работу', callback_data='find_work')
worker_but.add(button1, button2)

#def worker_prodile
worker_profile_but = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Имя', callback_data='worker_change_name')
button2 = InlineKeyboardButton('Специализацию', callback_data='worker_change_description')
button3 = InlineKeyboardButton('Номер телефона', callback_data='worker_change_phone')
button4 = InlineKeyboardButton('Возраст', callback_data='worker_change_age')
worker_profile_but.add(button1,button2,button3,button4)



#def send_commands_to_user - для заказчиков
client_but = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Мой профиль', callback_data='change_profile')
button2 = InlineKeyboardButton('Посмотреть заявки на работу')
client_but.add(button1, button2)

#def client_profile
client_profile_but = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Имя', callback_data='client_change_name')
button2 = InlineKeyboardButton('Номер телефона', callback_data='client_change_phone')
client_profile_but.add(button1,button2)

#def find_work
choise_how_to_find_work_button = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Фильтровать', callback_data='filter_find_work')
button2 = InlineKeyboardButton('Показать все заявки', callback_data='all_vacancy_find_work')
choise_how_to_find_work_button.add(button1, button2)
