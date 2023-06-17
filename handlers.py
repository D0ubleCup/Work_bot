"""
Здесь основной код бота, правила по использованию
1. Не нагружать кодом, функции и тексты писать в других файлах, тут только их вызов 
2. Даем коментарии к каждой функции, кратко описываем что она делает 
3. Изменения которые сделали сегодня записываем в общий txt файл

"""

import telebot  
from config import TOKEN 
from messages import start_mes, info_after_start_mes, info_for_worker_mes, worker_endregistration_mes, user_already_reg_mes
from markups import start_but, info_start_but, info_for_worker_but
from BaseDate import  check_registration,reg_client,check_role,load_worker
from markups import start_but, info_start_but, info_for_worker_but,info_for_client_but
from some_functions import phone_validator,age_validator 

client_registration_dict={}

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start(message): 
    bot.send_message(message.chat.id, text=start_mes , reply_markup=start_but)
    
@bot.callback_query_handler(func=lambda call: call.data=='continue')
def main_info(call):
    username = call.from_user.username
    check_user = check_registration(username)
    # if check_user:
    #     bot.send_message(call.message.chat.id, text=user_already_reg_mes)
        
    # else:
    #     bot.send_message(call.message.chat.id, text=info_after_start_mes, reply_markup=info_start_but )
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
    age = message.text.strip()
    if age_validator (age):
        username = message.from_user.username
        age = message.text
        chat_id = message.chat.id
        worker_registration_dict[username]['age'] = age
        worker_registration_dict[username]['chat_id'] = chat_id
        load_worker(worker_registration_dict, username) #функция для записи в бд
        del worker_registration_dict[username]
        mes = bot.send_message(message.chat.id , text = worker_endregistration_mes)
    else:
        mes = bot.send_message(message.chat.id , text = 'Возраст некорректен, введите корректный возраст')
        bot.register_next_step_handler(mes, worker_end_reg)
  



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
    
    phone_number=message.text.strip()
    check_phone=phone_validator(message.text)
    if check_phone:
        username=message.from_user.username
        client_registration_dict[username]['phone_number']=phone_number
        print(client_registration_dict)
        
        user_exist=reg_client(client_registration_dict,username)
        if not user_exist:
            bot.send_message(message.chat.id,'Вы зарегестрировались')
            
        else:
            bot.send_message(message.chat.id,'Вы уже зарегестрированы в системе. Нажмите /commands, чтобы увидеть ваши возможности ')
        del client_registration_dict[username]
        
    else:
        mes=bot.send_message(message.chat.id,'Введите корректный номер телефона')
        bot.register_next_step_handler(mes,client_reg_phone)

@bot.message_handler(commands='commands')
def send_commands_to_user(message):
    username=message.from_user.username
    if check_registration(username):
        role=check_role(username)
        if role=='worker':
            bot.send_message(message.chat.id,'Вы работник')
        if role=='client':
            bot.send_message(message.chat.id,'Вы заказчик')  
    else:
        bot.send_message(message.chat.id,'Вы не зарегестрированы')



bot.polling(none_stop=True) 