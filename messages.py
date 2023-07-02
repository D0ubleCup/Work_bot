from BaseDate import profile_worker_db, profile_client_db, full_info_order


start_mes = 'Приветственное сообщение'

info_after_start_mes = 'Полная информация об этом боте (выберите кем вы являетесь)'

info_for_worker_mes = 'информация для работников, о форме заполнения и как что работает'

worker_endregistration_mes = 'Поздравление работника с окончанием регистрации, (инструкция по использованию)'

info_for_client_mes = 'информация для заказчиков, что и как'

client_endregistration_mes = 'Поздравление заказчика с окончанием регистрации, (инструкция по использованию)'

user_already_reg_mes = 'Вы уже зарегестрированы в системе. Нажмите /commands, чтобы увидеть ваши возможности'

you_worker_comands_mes = 'Вы работник'
you_client_comands_mes = 'Вы заказчик'

def all_vacancy_find_work_message(client,title, description,adres,workers_count, recomend_age, price):
    return f'{client}, {title}, {description},{adres},{workers_count}, {recomend_age}, {price}'

def profile_worker_mes(username):
    date_worker = profile_worker_db(username)
    name = date_worker[0]
    description = date_worker[1]
    phone = date_worker[2]
    age = date_worker[3]
    return f'имя - {name}\nописание - {description}\nномер телефона - {phone}\nвозраст - {age}'

def profile_client_mes(username):
    date_worker = profile_client_db(username)
    name = date_worker[0]
    phone = date_worker[1]
    return f'имя - {name}\nномер телефона - {phone}'

def responce_worker_for_client_message(username):
    date_worker = profile_worker_db(username)
    print(date_worker)
    name = date_worker[0]
    description = date_worker[1]
    phone = date_worker[2]
    age = date_worker[3]
    return f'На вашу работу откликнулись \nимя:{name} \nо себе:{description} \nномер телефона:{phone}  \nвозраст:{age}'

def accept_worker_order_message(id_order):
    order_list = full_info_order(id_order)
    title = order_list[2]
    description = order_list[3]
    adres = order_list[4]
    age = order_list[6]
    price = order_list[7]
    return f'Вам пришел отклилк с заказа, вы назначенны работником \nназвание-{title} \nописание-{description} \nадрес-{adres} \nвозраст-{age} \nцена-{price}'

