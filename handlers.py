"""
Здесь основной код бота, правила по использованию
1. Не нагружать кодом, функции и тексты писать в других файлах, тут только их вызов 
2. Даем коментарии к каждой функции, кратко описываем что она делает 
3. Изменения которые сделали сегодня записываем в общий txt файл

"""

import telebot 
from config import TOKEN
from messages import start_mes, info_after_start_mes, info_for_worker_mes, worker_endregistration_mes
from markups import start_but, info_start_but, info_for_worker_but,info_for_client_but
from BaseDate import reg_client 

client_registration_dict={}

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start(message): 
    mes = bot.send_message(message.chat.id, text=start_mes , reply_markup=start_but)
    
@bot.callback_query_handler(func=lambda call: call.data=='continue')
def main_info(call):
    bot.send_message(call.message.chat.id, text=info_after_start_mes, reply_markup=info_start_but )


#информирование и регистрация работника 
@bot.callback_query_handler(func=lambda call: call.data=='worker')
def worker_reg_info(call):
    mes = bot.send_message(call.message.chat.id, text=info_for_worker_mes, reply_markup=info_for_worker_but)
    print(call.message.text)
    bot.register_next_step_handler(mes, worker_reg_name)


def worker_reg_name(message):
    username = message.from_user.first_name
    
    mes = bot.send_message(message.chat.id , 'Введите ваше имя')
    bot.register_next_step_handler(mes, worker_reg_surname)

def worker_reg_surname(message):
    first_name = message.text
    mes = bot.send_message(message.chat.id , 'Введите вашу фамилию')
    bot.register_next_step_handler(mes, worker_reg_resume)

def worker_reg_resume(message):
    mes = bot.send_message(message.chat.id , 'Напишите на чем вы специализируетесь или пару слов о себе')
    bot.register_next_step_handler(mes, worker_reg_phone)

def worker_reg_phone(message):  
    mes = bot.send_message(message.chat.id , 'Введите ваш номер телефона')
    bot.register_next_step_handler(mes, worker_reg_age)

def worker_reg_age(message):
    mes = bot.send_message(message.chat.id , 'Введите ваш возраст')
    bot.register_next_step_handler(mes, worker_end_reg)

def worker_end_reg(message):
    mes = bot.send_message(message.chat.id , text = worker_endregistration_mes)
  



#информирование и регистрация работодателя

@bot.callback_query_handler(func=lambda call: call.data=='employer')
def client_reg_info(call):
    mes = bot.send_message(call.message.chat.id, text="Написать текст", reply_markup=info_for_client_but)
    
    

@bot.callback_query_handler(func=lambda call: call.data=='client_registration')
def client_reg_name(call):
    print(1)
    chat_id=call.message.chat.id
    username=call.from_user.username
    client_registration_dict[username]={
    'username':username,
    'chat_id':chat_id   
    }
    mes = bot.send_message(call.message.chat.id , 'Введите ваше имя')
    bot.register_next_step_handler(mes, client_reg_surname)

def client_reg_surname(message):
    name=message.text
    username=message.from_user.username
    client_registration_dict[username]['name']=name
    mes = bot.send_message(message.chat.id , 'Введите ваш номер телефона')
    bot.register_next_step_handler(mes,client_reg_phone)

def client_reg_phone(message):
    print('Да')
    phone_number=message.text
    username=message.from_user.username
    client_registration_dict[username]['phone_number']=phone_number
    print(client_registration_dict)
    reg_client(client_registration_dict,username)
    bot.send_message(message.chat.id,'Вы зарегестрировались')









bot.polling(none_stop=True) 