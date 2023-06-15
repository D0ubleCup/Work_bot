"""
Здесь основной код бота, правила по использованию
1. Не нагружать кодом, функции и тексты писать в других файлах, тут только их вызов 
2. Даем коментарии к каждой функции, кратко описываем что она делает 
3. Изменения которые сделали сегодня записываем в общий txt файл

"""

import telebot  
from config import TOKEN 
from messages import start_mes, info_after_start_mes, info_for_worker_mes, worker_endregistration_mes
from markups import start_but, info_start_but, info_for_worker_but
from BaseDate import load_username, check_registration

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start(message): 
    mes = bot.send_message(message.chat.id, text=start_mes , reply_markup=start_but)
    
@bot.callback_query_handler(func=lambda call: call.data=='continue')
def main_info(call):
    username = call.from_user.username
    check_user = check_registration(username)
    if check_user:
        pass
    else:
        bot.send_message(call.message.chat.id, text=info_after_start_mes, reply_markup=info_start_but )
    



#информирование и регистрация работника 
worker_registration_dict = {}
@bot.callback_query_handler(func=lambda call: call.data=='worker')
def worker_reg_info(call):
    bot.send_message(call.message.chat.id, text=info_for_worker_mes, reply_markup=info_for_worker_but)

@bot.callback_query_handler(func=lambda call: call.data=='worker_registration')
def worker_reg_name(call):
    username = call.from_user.username
    worker_registration_dict[username] = {}
    worker_registration_dict[username]['username'] = username
    mes = bot.send_message(call.message.chat.id , 'введите ваше имя')
    bot.register_next_step_handler(mes, worker_reg_surname)

def worker_reg_surname(message):
    username = message.from_user.username
    first_name = message.text
    worker_registration_dict[username]['first_name'] = first_name
    mes = bot.send_message(message.chat.id , 'Введите вашу фамилию')
    bot.register_next_step_handler(mes, worker_reg_resume)

def worker_reg_resume(message):
    username = message.from_user.username
    last_name = message.text
    worker_registration_dict[username]['last_name'] = last_name
    mes = bot.send_message(message.chat.id , 'Напишите на чем вы специализируетесь или пару слов о себе')
    bot.register_next_step_handler(mes, worker_reg_phone)

def worker_reg_phone(message):  
    username = message.from_user.username
    resume = message.text
    worker_registration_dict[username]['resume'] = resume
    mes = bot.send_message(message.chat.id , 'Введите ваш номер телефона')
    bot.register_next_step_handler(mes, worker_reg_age)

def worker_reg_age(message):
    username = message.from_user.username
    phone = message.text
    worker_registration_dict[username]['phone'] = phone
    mes = bot.send_message(message.chat.id , 'Введите ваш возраст')
    bot.register_next_step_handler(mes, worker_end_reg)

def worker_end_reg(message):
    username = message.from_user.username
    age = message.text
    chat_id = message.chat.id
    worker_registration_dict[username]['age'] = age
    worker_registration_dict[username]['chat_id'] = chat_id
    load_username(worker_registration_dict, username) #функция для записи в бд
    del worker_registration_dict[username]
    mes = bot.send_message(message.chat.id , text = worker_endregistration_mes)
  




bot.polling(none_stop=True) 