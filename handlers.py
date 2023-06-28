"""
Здесь основной код бота, правила по использованию
1. Не нагружать кодом, функции и тексты писать в других файлах, тут только их вызов 
2. Даем коментарии к каждой функции, кратко описываем что она делает 
3. Изменения которые сделали сегодня записываем в общий txt файл

"""

import telebot  
from config import TOKEN 
from messages import start_mes, info_after_start_mes, info_for_worker_mes, worker_endregistration_mes, user_already_reg_mes, client_endregistration_mes, info_for_client_mes, you_client_comands_mes, you_worker_comands_mes
from markups import start_but, info_start_but, info_for_worker_but,client_but,choose_type_button, choise_how_to_find_work_button
from BaseDate import check_registration,reg_client,check_role,reg_worker, worker_change_name_bd, worker_change_description_bd,worker_change_phone_bd,worker_change_age_bd,client_change_name_bd,client_change_phone_bd, add_work_black,all_vacancy_find_work_db
from markups import start_but, info_start_but, info_for_worker_but,info_for_client_but,worker_but, worker_profile_but,client_profile_but
from some_functions import phone_validator,age_validator 
from messages import profile_worker_mes, profile_client_mes

from messages import all_vacancy_find_work_message

client_registration_dict={}
client_add_work_dict={}
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
    mes = bot.send_message(message.chat.id , 'Напишите на чем вы специализируетесь или пару слов о себе, что бы пропустить нажмите /next')
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
def client_reg(call):
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
    mes = bot.send_message(message.chat.id , 'Введите ваш номер телефона, что бы пропустить нажмите /next')
    bot.register_next_step_handler(mes,client_reg_phone)

def client_reg_phone(message):
    username=message.from_user.username
    if message.text == '/next':
        client_registration_dict[username]['phone_number']= 'Не указано'
    else:
        phone_number=message.text.strip()
        check_phone=phone_validator(phone_number)
        if check_phone:
            client_registration_dict[username]['phone_number']=phone_number
            
        else:
            mes=bot.send_message(message.chat.id,'Введите корректный номер телефона')
            bot.register_next_step_handler(mes,client_reg_phone)

    reg_client(client_registration_dict, username)
    bot.send_message(message.chat.id, text = client_endregistration_mes)
    del client_registration_dict[username]
    



#командный пункт 
@bot.message_handler(commands=['commands'])
def send_commands_to_user(message):
    username=message.from_user.username
    if check_registration(username):
        role=check_role(username)
        if role=='worker':
            bot.send_message(message.chat.id,text = you_worker_comands_mes, reply_markup= worker_but )
        if role=='client':
            bot.send_message(message.chat.id,text = you_client_comands_mes ,reply_markup=client_but )  
    else:
        bot.send_message(message.chat.id, text ='Вы не зарегестрированы, зарегистрируйтесь', reply_markup= start_but)


#возможно логику пересылку на именно этот хендлеры нужно заменить
#логика профиля и его коректировки
@bot.callback_query_handler(func=lambda call: call.data=='change_profile')
def user_profile (call):
    username = call.from_user.username
    role = check_role(username)
    if role == 'worker':
        bot.send_message(call.message.chat.id, text = profile_worker_mes(username), reply_markup=worker_profile_but)
    elif role == 'client':
        bot.send_message(call.message.chat.id, text = profile_client_mes(username), reply_markup=client_profile_but)




#изменение имени у работника
@bot.callback_query_handler(func=lambda call: call.data=='worker_change_name')
def worker_change_name(call):
    mes = bot.send_message(call.message.chat.id, 'Введите новое имя пользователя, что бы отменить, нажмите /skip')
    bot.register_next_step_handler(mes, worker_change_name2)
def worker_change_name2(message):
    if message.text == '/skip':
        bot.send_message(message.chat.id , text = 'функция(работник)', reply_markup=worker_but)
    else:
        username = message.from_user.username
        new_username = message.text
        answer_bd = worker_change_name_bd(username, new_username)
        bot.send_message(message.chat.id , text = answer_bd, reply_markup=worker_but)

#изменение описания у работника 
@bot.callback_query_handler(func=lambda call: call.data=='worker_change_description')
def worker_change_description(call):
    mes = bot.send_message(call.message.chat.id, 'Введите новое описание, что бы отменить, нажмите /skip')
    bot.register_next_step_handler(mes, worker_change_description2)
def worker_change_description2(message):
    if message.text == '/skip':
        bot.send_message(message.chat.id , text = 'функция(работник)', reply_markup=worker_but)
    else:
        username = message.from_user.username
        new_description = message.text
        answer_bd = worker_change_description_bd(username, new_description)
        bot.send_message(message.chat.id , text = answer_bd, reply_markup= worker_but)
    
#изменение номера телефона у работника 
@bot.callback_query_handler(func=lambda call: call.data=='worker_change_phone')
def worker_change_phone(call):
    mes = bot.send_message(call.message.chat.id, 'Введите новый телефонный номер, что бы отменить, нажмите /skip')
    bot.register_next_step_handler(mes, worker_change_phone2)
def worker_change_phone2(message):
    if message.text == '/skip':
        bot.send_message(message.chat.id , text = 'функция(работник)', reply_markup=worker_but)
    else:
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
    mes = bot.send_message(call.message.chat.id, 'Введите другой возраст, что бы отменить, нажмите /skip')
    bot.register_next_step_handler(mes, worker_change_age2)
def worker_change_age2(message):
    if message.text == '/skip':
        bot.send_message(message.chat.id , text = 'функция(работник)', reply_markup=worker_but)
    else:
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
    mes = bot.send_message(call.message.chat.id, 'Введите новое имя пользователя, что бы отменить, нажмите /skip')
    bot.register_next_step_handler(mes, client_change_name2)
def client_change_name2(message):
    if message.text == '/skip':
        bot.send_message(message.chat.id , text = 'функция(работник)', reply_markup=client_but)
    else:
        username = message.from_user.username
        new_username = message.text
        answer_bd = client_change_name_bd(username, new_username)
        bot.send_message(message.chat.id , text = answer_bd, reply_markup=client_but)

#изменение номера телефона у клиента 
@bot.callback_query_handler(func=lambda call: call.data=='client_change_phone')
def client_change_phone(call):
    mes = bot.send_message(call.message.chat.id, 'Введите новый телефонный номер, что бы отменить, нажмите /skip')
    bot.register_next_step_handler(mes, client_change_phone2)
def client_change_phone2(message):
    if message.text == '/skip':
        bot.send_message(message.chat.id , text = 'функция(работник)', reply_markup=client_but)
    else:
        username = message.from_user.username
        new_phone_namber = message.text
        check_phone=phone_validator(new_phone_namber)
        if check_phone:
            answer_bd = client_change_phone_bd(username, new_phone_namber)
            bot.send_message(message.chat.id , text = answer_bd, reply_markup=client_but)
        else:
            mes=bot.send_message(message.chat.id,'Введите корректный номер телефона')
            bot.register_next_step_handler(mes,client_change_phone2)


# выбор нужной команды для поиска работы работнику 
@bot.callback_query_handler(func=lambda call: call.data=='find_work')
def find_work(call):
    bot.send_message(call.message.chat.id, text = 'Выберите нужную команду', reply_markup=choise_how_to_find_work_button)

# показать все заявки на работу для работника
@bot.callback_query_handler(func=lambda call: call.data=='all_vacancy_find_work')
def all_vacancy_find_work(call):
    all_vacancy = all_vacancy_find_work_db()
    for one_vacancy in all_vacancy:
        client = one_vacancy[0]
        title = one_vacancy[1]
        description = one_vacancy[2]
        adres = one_vacancy[3]
        workers_count = one_vacancy[4]
        recomend_age = one_vacancy[5]
        price = one_vacancy[6]
        answer_message = all_vacancy_find_work_message(client, title, description,adres,workers_count, recomend_age, price)
        bot.send_message(call.message.chat.id, text = answer_message)

    

    

# фильтрация заявок для работников 
@bot.callback_query_handler(func=lambda call: call.data=='filter_find_work')
def filter_find_work(call):
    filter_find_work_dict = {}
    mes = bot.send_message(call.message.chat.id, 'Укажите желаемую цену через тире в формате 1000-2500')


#Добавление работы в черновую базу данных со стороны заказчика
@bot.callback_query_handler(func=lambda call: call.data=='add_work')
def choose_type_work(call):
    client_add_work_dict[call.from_user.username]={}
    mes=bot.send_message(call.message.chat.id,'Выберите тип оплаты за работу',reply_markup=choose_type_button)
    bot.register_next_step_handler(mes,work_title)

def work_title(message):
    username=message.from_user.username
    if message.text=='Почасовая':
        client_add_work_dict[username]['type']='Почасовая'
    if message.text=='Фиксированная':
        client_add_work_dict[username]['type']='Фиксированная'
    mes=bot.send_message(message.chat.id,'Введите название работы')
    bot.register_next_step_handler(mes,work_description)

def work_description(message):
    username=message.from_user.username
    client_add_work_dict[username]['title']=message.text
    mes=bot.send_message(message.chat.id,'Введите подробное описание работы')
    bot.register_next_step_handler(mes,work_adress)

def work_adress(message):
    username=message.from_user.username
    client_add_work_dict[username]['description']=message.text
    mes=bot.send_message(message.chat.id,'Введите адрес работы')
    bot.register_next_step_handler(mes,work_workers_count)

def work_workers_count(message):
    username=message.from_user.username
    client_add_work_dict[username]['adress']=message.text
    mes=bot.send_message(message.chat.id,'Введите необходимое количество работников')
    bot.register_next_step_handler(mes,work_age)

def work_age(message):
    if message.text.strip().isnumeric():
        username=message.from_user.username
        client_add_work_dict[username]['workers_count']=int(message.text.strip())
        mes=bot.send_message(message.chat.id,'Введите желаемый возраст работников')
        bot.register_next_step_handler(mes,work_price)
    #     bot.register_next_step_handler(mes,work_price)
    #     mes=bot.send_message(message.chat.id,'Введите желаемую оплату в рублях. Если она не соответсвует нормам, то с вами свяжется администратор для того, чтобы обсудить ее')
    #     bot.register_next_step_handler(mes,work_price)
    else:
        mes=bot.send_message(message.chat.id,'Пожалуйста, введите число.')
        bot.register_next_step_handler(mes,work_age)
def work_price(message):
    if message.text.strip().isnumeric():
        username=message.from_user.username
        client_add_work_dict[username]['age']=int(message.text.strip())
        mes=bot.send_message(message.chat.id,'Введите желаемую оплату в рублях. Если она не соответсвует нормам, то с вами свяжется администратор для того, чтобы обсудить ее')
        bot.register_next_step_handler(mes,work_finish)   
    else:
        mes=bot.send_message(message.chat.id,'Пожалуйста, введите число.')
        bot.register_next_step_handler(mes,work_price)
   

def work_finish(message):
    if message.text.strip().isnumeric():
        username=message.from_user.username
        client_add_work_dict[username]['price']=int(message.text.strip())
        mes=bot.send_message(message.chat.id,'Ваша вакансия отправлена администатору. В скором времени она будет опубликована и на нее начнут откликаться работники.')
        add_work_black(client_add_work_dict,username)
        print(client_add_work_dict)
    else:
        mes=bot.send_message(message.chat.id,'Пожалуйста, введите число.')
        bot.register_next_step_handler(mes,work_finish)
    
    

bot.polling(none_stop=True) 