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
button1 = InlineKeyboardButton('заполнить анкету регистрации', callback_data='worker_registration')
info_for_worker_but.add(button1)