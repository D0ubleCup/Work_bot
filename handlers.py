"""
Здесь основной код бота, правила по использованию
1. Не нагружать кодом, функции и тексты писать в других файлах, тут только их вызов 
2. Даем коментарии к каждой функции, кратко описываем что она делает 
3. Изменения которые сделали сегодня записываем в общий txt файл

"""

import telebot  
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN 
from messages import start_mes, info_after_start_mes, info_for_worker_mes, worker_endregistration_mes, user_already_reg_mes, client_endregistration_mes, info_for_client_mes, you_client_comands_mes, you_worker_comands_mes
from markups import start_but, info_start_but, info_for_worker_but,client_but,choose_type_button, choise_how_to_find_work_button
from BaseDate import check_registration,reg_client,check_role,reg_worker, worker_change_name_bd, worker_change_description_bd,worker_change_phone_bd,worker_change_age_bd,client_change_name_bd,client_change_phone_bd, add_work_black,all_vacancy_find_work_db, find_chatid_client_for_worker_db
from markups import start_but, info_start_but, info_for_worker_but,info_for_client_but,worker_but, worker_profile_but,client_profile_but
from some_functions import phone_validator,age_validator 
from messages import profile_worker_mes, profile_client_mes, responce_worker_for_client_message
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from config import TOKEN 
from messages import start_mes, info_after_start_mes, info_for_worker_mes, worker_endregistration_mes, user_already_reg_mes, client_endregistration_mes, info_for_client_mes, you_client_comands_mes, you_worker_comands_mes
from markups import start_but, info_start_but, info_for_worker_but,client_but,choose_type_button, choise_how_to_find_work_button
from BaseDate import check_registration,reg_client,check_role,reg_worker, worker_change_name_bd, worker_change_description_bd,worker_change_phone_bd,worker_change_age_bd,client_change_name_bd,client_change_phone_bd, add_work_black,all_vacancy_find_work_db,select_admin_chat_id,accept_work_db,reject_work_db
from markups import start_but, info_start_but, info_for_worker_but,info_for_client_but,worker_but, worker_profile_but,client_profile_but, select_worker_chat_id
from some_functions import phone_validator,age_validator 
from messages import profile_worker_mes, profile_client_mes,all_vacancy_find_work_message, accept_worker_order_message




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
    username = call.from_user.username
    for one_vacancy in all_vacancy:
        id_vacancy = one_vacancy[0]
        client = one_vacancy[1]
        title = one_vacancy[2]
        description = one_vacancy[3]
        adres = one_vacancy[4]
        workers_count = one_vacancy[5]
        recomend_age = one_vacancy[6]
        price = one_vacancy[7]
        answer_message = all_vacancy_find_work_message(client, title, description,adres,workers_count, recomend_age, price)

        worker_responce_work_but = InlineKeyboardMarkup()
        button = InlineKeyboardButton('Откликнуться',callback_data=f'responce_worker_id={id_vacancy}={username}')
        worker_responce_work_but.add(button)

        bot.send_message(call.message.chat.id, text = answer_message, reply_markup= worker_responce_work_but)

@bot.callback_query_handler(func=lambda call: 'responce_worker' in call.data)
def responce_worker_for_client(call): 
    call_data = call.data
    call_data_spl = call_data.split('=')
    id_order = call_data_spl[1]
    username_worker = call_data_spl[2]
    chatid_client = find_chatid_client_for_worker_db(id_order)
    text_for_client = responce_worker_for_client_message(username_worker)

    responce_client_for_worker_button = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Принять работника', callback_data= f'accept_worker username={username_worker}={id_order}')
    button2 = InlineKeyboardButton('Отклонить предложение', callback_data='reject_worker')
    responce_client_for_worker_button.add(button1, button2)

    bot.send_message(chat_id=chatid_client, text = text_for_client, reply_markup=responce_client_for_worker_button)

@bot.callback_query_handler(func=lambda call: 'accept_worker' in call.data)
def accept_worker(call):
    call_data = call.data
    call_data_spl = call_data.split('=')
    id_order = call_data_spl[2]
    username_worker = call_data_spl[1]
    chatid_worker = select_worker_chat_id(username_worker)
    text_accept = accept_worker_order_message(id_order)
    bot.send_message(chat_id= chatid_worker, text = text_accept)

#id работника , заказ

#@bot.callback_query_handler(func=lambda call: call.data=='reject_worker')



# фильтрация заявок для работников 
# filter_find_work_dict = {}
# @bot.callback_query_handler(func=lambda call: call.data=='filter_find_work')
# def filter_find_work(call):
#     username = call.from_user.username
#     filter_find_work_dict[username] = {}
#     mes = bot.send_message(call.message.chat.id, 'Укажите минимальную цену')
#     bot.register_next_step_handler(mes, end_filter_worker)

# def end_filter_worker(message):
    




#Добавление работы в черновую базу данных со стороны заказчика
@bot.callback_query_handler(func=lambda call: call.data=='add_work')
def choose_type_work(call):
    client_add_work_dict[call.from_user.username]={}
    mes=bot.send_message(call.message.chat.id,'Выберите тип оплаты за работу',reply_markup=choose_type_button)
    bot.register_next_step_handler(mes,work_title)

def work_title(message):
    username=message.from_user.username
    if message.text=='Почасовая' or message.text=='Фиксированная':
        client_add_work_dict[username]['type']=message.text
        mes=bot.send_message(message.chat.id,'Введите название работы')
        bot.register_next_step_handler(mes,work_description)
    else:
        mes=bot.send_message(message.chat.id,'Пожалуйста, воспользуйтесь клавиатурой',reply_markup=choose_type_button)
        bot.register_next_step_handler(mes,work_title)

def work_description(message):
    username=message.from_user.username
    client_add_work_dict[username]['title']=message.text
    mes=bot.send_message(message.chat.id,'Введите подробное описание работы')
    bot.register_next_step_handler(mes,work_adress)

def work_adress(message):
    username=message.from_user.username
    client_add_work_dict[username]['description']=message.text
    mes=bot.send_message(message.chat.id,'Введите адрес работы. Если хотите пропустить, то введите /skip')
    bot.register_next_step_handler(mes,work_workers_count)

def work_workers_count(message):
    username=message.from_user.username
    if message.text.strip()=='/skip':
    
        client_add_work_dict[username]['adress']='Не указано'
    else:
        client_add_work_dict[username]['adress']=message.text
    mes=bot.send_message(message.chat.id,'Введите необходимое количество работников')
    bot.register_next_step_handler(mes,work_age)

def work_age(message):
    if message.text.strip().isnumeric():
        username=message.from_user.username
        client_add_work_dict[username]['workers_count']=int(message.text.strip())
        mes=bot.send_message(message.chat.id,'Введите желаемый возраст работников. Если хотите пропустить, то введите /skip')
        bot.register_next_step_handler(mes,work_price)
    #     bot.register_next_step_handler(mes,work_price)
    #     mes=bot.send_message(message.chat.id,'Введите желаемую оплату в рублях. Если она не соответсвует нормам, то с вами свяжется администратор для того, чтобы обсудить ее')
    #     bot.register_next_step_handler(mes,work_price)
    else:
        mes=bot.send_message(message.chat.id,'Пожалуйста, введите число.')
        bot.register_next_step_handler(mes,work_age)
def work_price(message):
    username=message.from_user.username
    if message.text.strip()=='/skip':
        client_add_work_dict[username]['age']='Не указано'
    else:
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
        last_id=add_work_black(client_add_work_dict,username)
        admin_chat_id=select_admin_chat_id()
        print(last_id)
        title=client_add_work_dict[username]['title']
        description=client_add_work_dict[username]['description']
        type=client_add_work_dict[username]['type']
        adres=client_add_work_dict[username]['adress']
        workers_count=client_add_work_dict[username]['workers_count']
        age=client_add_work_dict[username]['age']
        price=client_add_work_dict[username]['price']
        keyboard=InlineKeyboardMarkup()
        button_agree=InlineKeyboardButton('Одобрить',callback_data=f'work_accept_id={last_id}')
        button_reject=InlineKeyboardButton('Отклонить',callback_data=f'work_reject_id={last_id}')
        keyboard.add(button_agree)
        keyboard.add(button_reject)
        bot.send_message(admin_chat_id,f'Название : {title}\nОписание : {description}\nТип оплаты : {type}\nАдрес : {adres}\nКоличество работников : {workers_count}\nЖелаемый возраст:{age}\nОплата : {price}',reply_markup=keyboard)
    else:
        mes=bot.send_message(message.chat.id,'Пожалуйста, введите число.')
        bot.register_next_step_handler(mes,work_finish)
    

@bot.callback_query_handler(func=lambda call: 'work_accept' in call.data)
def accept_work(call):
    order_id=int(call.data.split('=')[1])
    client_chat_id=accept_work_db(order_id)
    bot.send_message(client_chat_id,'Ваша заявка опубликована')


@bot.callback_query_handler(func=lambda call: 'work_reject' in call.data)
def accept_work(call):
    order_id=int(call.data.split('=')[1])
    client_chat_id=reject_work_db(order_id)
    bot.send_message(client_chat_id,'Ваша заявка отклонена')






bot.polling(none_stop=True) 