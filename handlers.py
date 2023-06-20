"""
Здесь основной код бота, правила по использованию
1. Не нагружать кодом, функции и тексты писать в других файлах, тут только их вызов 
2. Даем коментарии к каждой функции, кратко описываем что она делает 
3. Изменения которые сделали сегодня записываем в общий txt файл

"""

import telebot  
from config import TOKEN 
from messages import start_mes, info_after_start_mes, info_for_worker_mes, worker_endregistration_mes, user_already_reg_mes, client_endregistration_mes, info_for_client_mes, you_client_comands_mes, you_worker_comands_mes
from markups import start_but, info_start_but, info_for_worker_but,client_but
from BaseDate import check_registration,reg_client,check_role,reg_worker, worker_change_name_bd, worker_change_description_bd,worker_change_phone_bd,worker_change_age_bd,client_change_name_bd,client_change_phone_bd
from markups import start_but, info_start_but, info_for_worker_but,info_for_client_but,worker_but, worker_profile_but,client_profile_but
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
    bot.register_next_step_handler(mes, worker_reg_resume)  

def worker_reg_resume(message):
    username=message.from_user.username
    first_name = message.text
    worker_registration_dict[username]['first_name'] = first_name
    mes = bot.send_message(message.chat.id , 'Напишите на чем вы специализируетесь или пару слов о себе')
    bot.register_next_step_handler(mes, worker_reg_phone)

def worker_reg_phone(message): 
    username=message.from_user.username 
    resume = message.text
    worker_registration_dict[username]['resume'] = resume
    mes = bot.send_message(message.chat.id , 'Введите ваш номер телефона')
    bot.register_next_step_handler(mes, worker_reg_age)

def worker_reg_age(message):
    username=message.from_user.username
    phone = message.text.strip()
    check_phone=phone_validator(phone)
    if check_phone:
        worker_registration_dict[username]['phone'] = phone
        mes = bot.send_message(message.chat.id , 'Введите ваш возраст')
        bot.register_next_step_handler(mes, worker_end_reg)
    else:
        mes=bot.send_message(message.chat.id,'Введите корректный номер телефона')
        bot.register_next_step_handler(mes,worker_reg_age)

def worker_end_reg(message):
    username=message.from_user.username
    age = message.text.strip()
    if age_validator (age):
        chat_id = message.chat.id
        worker_registration_dict[username]['age'] = age
        worker_registration_dict[username]['chat_id'] = chat_id
        reg_worker(worker_registration_dict, username) #функция для записи в бд
        del worker_registration_dict[username]
        mes = bot.send_message(message.chat.id , text = worker_endregistration_mes)
    else:
        mes = bot.send_message(message.chat.id , text = 'Возраст некорректен, введите корректный возраст')
        bot.register_next_step_handler(mes, worker_end_reg)
  



#информирование и регистрация работодателя
@bot.callback_query_handler(func=lambda call: call.data=='employer')
def client_reg_info(call):
    bot.send_message(call.message.chat.id, text=info_for_client_mes, reply_markup=info_for_client_but)

@bot.callback_query_handler(func=lambda call: call.data=='client_registration')
def client_reg_name(call):
    username=call.from_user.username
    chat_id=call.message.chat.id
    client_registration_dict[username]={
    'username':username,
    'chat_id':chat_id   
    }
    mes = bot.send_message(call.message.chat.id , 'Введите ваше имя')
    bot.register_next_step_handler(mes, client_reg_surname)

def client_reg_surname(message):
    username=message.from_user.username
    name=message.text
    client_registration_dict[username]['name']=name
    mes = bot.send_message(message.chat.id , 'Введите ваш номер телефона')
    bot.register_next_step_handler(mes,client_reg_phone)

def client_reg_phone(message):
    username=message.from_user.username
    phone_number=message.text.strip()
    check_phone=phone_validator(phone_number)
    if check_phone:
        client_registration_dict[username]['phone_number']=phone_number
        reg_client(client_registration_dict, username)
        bot.send_message(message.chat.id, text = client_endregistration_mes)
        del client_registration_dict[username]
    else:
        mes=bot.send_message(message.chat.id,'Введите корректный номер телефона')
        bot.register_next_step_handler(mes,client_reg_phone)
    



#командный пункт 
@bot.message_handler(commands=['commands'])
def send_commands_to_user(message):
    username=message.from_user.username
    if check_registration(username):
        role=check_role(username)
        if role=='worker':
            bot.send_message(message.chat.id,text = you_worker_comands_mes, reply_markup= worker_but )
        if role=='client':
            bot.send_message(message.chat.id,text = you_client_comands_mes  )  
    else:
        bot.send_message(message.chat.id, text ='Вы не зарегестрированы, зарегистрируйтесь', reply_markup= start_but)


#возможно логику пересылку на именно этот хендлеры нужно заменить
#логика профиля и его коректировки
@bot.callback_query_handler(func=lambda call: call.data=='change_profile')
@bot.message_handler(content_types='text')
def worker_profile (message):
    username = message.chat.id
    if message.text == 'Мой профиль':
        role = check_role(username)
        if role == 'worker':
            bot.send_message(message.chat.id, text = 'функция(работник)', reply_markup=worker_profile_but)
        elif role == 'client':
            bot.send_message(message.chat.id, text = 'функция(клиент)', reply_markup=client_profile_but)



#изменение имени у работника
@bot.callback_query_handler(func=lambda call: call.data=='worker_change_name')
def worker_change_name(call):
    mes = bot.send_message(call.message.chat.id, 'Введите новое имя пользователя')
    bot.register_next_step_handler(mes, worker_change_name2)
def worker_change_name2(message):
    username = message.from_user.username
    new_username = message.text
    answer_bd = worker_change_name_bd(username, new_username)
    bot.send_message(message.chat.id , text = answer_bd, reply_markup=worker_but)

#изменение описания у работника 
@bot.callback_query_handler(func=lambda call: call.data=='worker_change_description')
def worker_change_description(call):
    mes = bot.send_message(call.message.chat.id, 'Введите новое описание')
    bot.register_next_step_handler(mes, worker_change_description2)
def worker_change_description2(message):
    username = message.from_user.username
    new_description = message.text
    answer_bd = worker_change_description_bd(username, new_description)
    bot.send_message(message.chat.id , text = answer_bd, reply_markup= worker_but)
    
#изменение номера телефона у работника 
@bot.callback_query_handler(func=lambda call: call.data=='worker_change_phone')
def worker_change_phone(call):
    mes = bot.send_message(call.message.chat.id, 'Введите новый телефонный номер')
    bot.register_next_step_handler(mes, worker_change_phone2)
def worker_change_phone2(message):
    username = message.from_user.username
    new_phone_namber = message.text
    check_phone=phone_validator(new_phone_namber)
    if check_phone:
        answer_bd = worker_change_phone_bd(username, new_phone_namber)
        bot.send_message(message.chat.id , text = answer_bd, reply_markup=worker_but)
    else:
        mes=bot.send_message(message.chat.id,'Введите корректный номер телефона')
        bot.register_next_step_handler(mes,worker_change_phone2)
        
#изменение возраста у работника 
@bot.callback_query_handler(func=lambda call: call.data=='worker_change_age')
def worker_change_age(call):
    mes = bot.send_message(call.message.chat.id, 'Введите другой возраст')
    bot.register_next_step_handler(mes, worker_change_age2)
def worker_change_age2(message):
    username = message.from_user.username
    new_age = message.text
    check_age = age_validator (new_age)
    if check_age:
        answer_bd = worker_change_age_bd(username, new_age)
        bot.send_message(message.chat.id , text = answer_bd,reply_markup=worker_but)
    else:
        mes = bot.send_message(message.chat.id , text = 'Возраст некорректен, введите корректный возраст')
        bot.register_next_step_handler(mes, worker_change_age2)


# изменения профиля у заказчиков
@bot.callback_query_handler(func=lambda call: call.data=='client_change_name')
def client_change_name(call):
    mes = bot.send_message(call.message.chat.id, 'Введите новое имя пользователя')
    bot.register_next_step_handler(mes, client_change_name2)
def client_change_name2(message):
    username = message.from_user.username
    new_username = message.text
    answer_bd = client_change_name_bd(username, new_username)
    bot.send_message(message.chat.id , text = answer_bd, reply_markup=client_but)

#изменение номера телефона у клиента 
@bot.callback_query_handler(func=lambda call: call.data=='client_change_phone')
def client_change_phone(call):
    mes = bot.send_message(call.message.chat.id, 'Введите новый телефонный номер')
    bot.register_next_step_handler(mes, client_change_phone2)
def client_change_phone2(message):
    username = message.from_user.username
    new_phone_namber = message.text
    check_phone=phone_validator(new_phone_namber)
    if check_phone:
        answer_bd = client_change_phone_bd(username, new_phone_namber)
        bot.send_message(message.chat.id , text = answer_bd, reply_markup=client_but)
    else:
        mes=bot.send_message(message.chat.id,'Введите корректный номер телефона')
        bot.register_next_step_handler(mes,client_change_phone2)




bot.polling(none_stop=True) 