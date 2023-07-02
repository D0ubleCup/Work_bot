import sqlite3
db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
sql=db.cursor()
db.row_factory=sqlite3.Row
# вставлять везде этот обработчик ошибок
# db = None
# try: 
# except sqlite3.Error as e:
#     if db: db.rollback() 
#     print (e)
# finally: 
#     db.commit()
#     if db: db.close()

#функция проверки зарегистрирован ли ползователь
def check_registration(username):
    db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
    sql=db.cursor()
    db = None
    try: 
        sql.execute(f"SELECT name FROM worker WHERE username == '{username}'")
        from_worker = sql.fetchone()
        sql.execute(f"SELECT name FROM client WHERE username == '{username}'")
        from_client = sql.fetchone()
        if from_worker != None or from_client != None:
            return True
        else: 
            return False
    except sqlite3.Error as e:
        if db: db.rollback() 
        print (e)
    finally: 
        if db: db.close()



#функция проверки роли пользователя
def check_role(username):
    try:
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"SELECT 'worker' as source, username FROM worker WHERE username='{username}' UNION ALL SELECT 'client' as source, username FROM client WHERE username='{username}'")
        rows = sql.fetchone()
        # print(rows)
        return rows[0]
    except:
        return 'Пользователь не найден'

#запись работника в бд
def reg_worker(date, username):
    db = None

    worker_information = date[username]
    username = worker_information['username'].replace(' ', '_')
    first_name = worker_information['first_name'].replace(' ', '_')
    resume = worker_information['resume'].replace(' ', '_')
    phone = worker_information['phone'].replace(' ', '_')
    age = worker_information['age']
    chat_id = worker_information['chat_id']
    if resume == '/next': #обработка пропуска 
        resume = 'Не указано'
    try: 
        db = sqlite3.connect('DataBases/workers.db')
        sql = db.cursor()

        
        sql.execute(f"INSERT INTO worker (username , name , specialization, phone_number, age, rate, chat_id) VALUES('{username}', '{first_name}','{resume}','{phone}', '{age}', '{0}', '{chat_id}')")
        sql.execute(f"UPDATE main_info SET workers_count = workers_count + 1")

    except sqlite3.Error as e:
        if db: db.rollback() 
        print (e)

    finally: 
        db.commit()
        if db: db.close()

def reg_client(client_info,username):               #функция записи заказчика в базу данных, принимает словарь и имя пользователя
    username=client_info[username]['username']
    chat_id=client_info[username]['chat_id']
    phone_number=client_info[username]['phone_number']
    name=client_info[username]['name']
    try:
        sql.execute(f"INSERT INTO client(name,phone_number,chat_id,username) VALUES('{name}','{phone_number}','{chat_id}','{username}')")
        sql.execute(f"UPDATE main_info SET client_count = client_count + 1")
    except sqlite3.Error as e: 
        if db: db.rollback()  
        print (e) 
    finally:  
        db.commit()
        db.close()


#изменение имени у работника
def worker_change_name_bd(username, new_username):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"UPDATE worker SET name = '{new_username}' WHERE username = '{username}'")
        return f'Успешно, ваше имя измененно на {new_username}'
    except sqlite3.Error as e:
        if db: db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()
#изменение описания у работника
def worker_change_description_bd(username, new_description):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"UPDATE worker SET specialization = '{new_description}' WHERE username = '{username}'")
        return f'Успешно, ваше описание измененно'
    except sqlite3.Error as e:
        if db: db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()
#изменение номера телефона у работника
def worker_change_phone_bd(username, new_phone_namber):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"UPDATE worker SET phone_number = '{new_phone_namber}' WHERE username = '{username}'")
        return f'Успешно, ваш номер успешно изменен на {new_phone_namber}'
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()
#изменение возраста у работника
def worker_change_age_bd(username, new_age):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"UPDATE worker SET age = '{new_age}' WHERE username = '{username}'")
        return f'Успешно, ваш возраст успешно изменен на{new_age}'
    except sqlite3.Error as e:
        if db: db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()


#изменение профиля у заказчика
#изменение имени у заказчика
def client_change_name_bd(username, new_username):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"UPDATE client SET name = '{new_username}' WHERE username = '{username}'")
        print ('name(1)')
        return f'Успешно, ваше имя измененно на {new_username}'
    except sqlite3.Error as e:
        if db: db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()
#изменение номера телефона у заказчика
def client_change_phone_bd(username, new_phone_namber):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"UPDATE client SET phone_number = '{new_phone_namber}' WHERE username = '{username}'")
        db.commit()
        return f'Успешно, ваш номер успешно изменен на {new_phone_namber}'
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()



def all_vacancy_find_work_db():
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"SELECT id, client, title, description, adress, workers_count, age, price FROM 'order' WHERE status = '1'") #достаю все записи из двух столбцов
        all_vacancy = sql.fetchall()
        return all_vacancy
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()

# print(all_vacancy_find_work_db())


#Добавление записи в таблицу черновая работа 
def add_work_black(work_dict,username):               #функция записи заказчика в базу данных, принимает словарь и имя пользователя
    # username=client_info[username]['username']
    # chat_id=client_info[username]['chat_id']
    # phone_number=client_info[username]['phone_number']
    # name=client_info[username]['name']
    username=username
    type_work=title=work_dict[username]['type']
    title=work_dict[username]['title']
    description=work_dict[username]['description']
    adress=work_dict[username]['adress']
    count_workers=work_dict[username]['workers_count']
    age=work_dict[username]['age']
    price=work_dict[username]['price']
    
   
    
    try:
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"SELECT id FROM client WHERE username=='{username}'")
        client=sql.fetchone()[0]
        print(client)
        
        sql.execute(f"INSERT INTO 'order' (client,title,description,adress,workers_count,age,price,type,status) VALUES('{client}','{title}','{description}','{adress}',{count_workers},'{age}','{price}','{type_work}',0)")
        sql.execute(f"UPDATE main_info SET orders_count = orders_count + 1")
        sql.execute(f"UPDATE main_info SET orders_sum = orders_sum + {price}")
        last_id = sql.execute('SELECT last_insert_rowid()').fetchone()[0]
        return last_id
    except sqlite3.Error as e: 
        if db: db.rollback()  
        print (e) 
    finally:  
        db.commit()
        db.close()

# add_work_black({'Hzorhz': {'type': 'Почасовая', 'title': 'название', 'description': 'Описание', 'adress': 'адрес', 'workers_count': 6, 'age': 12, 'price': 1789}},'Hzorhz')

def profile_worker_db(username):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"SELECT name, specialization, phone_number, age FROM worker WHERE username = '{username}'")
        date_worker = sql.fetchone()
        print(date_worker)
        return date_worker
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()
profile_worker_db('Alexei0212022')

def profile_client_db(username):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"SELECT name, phone_number FROM client WHERE username = '{username}'")
        date_client = sql.fetchone()
        return date_client
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close() 

# print (profile_client_db('Alexei0212022'))

#достает chatid заказчика для пересылки ему отклика работника 
def find_chatid_client_for_worker_db(id_order):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"SELECT client FROM 'order' WHERE id = '{id_order}'")
        client_id = sql.fetchone()[0]
        sql.execute(f'SELECT chat_id FROM client WHERE id = {client_id}')
        chatid_client = sql.fetchone()[0]
        return chatid_client
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()

        db.close() 


#Функция, которая возвращает чат айди админа

def select_admin_chat_id():
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"SELECT chat_id FROM admin")
        admin_chat_id = sql.fetchone()[0]

        return admin_chat_id
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close()

        db.close() 
#Функция одобрения работы и перевода ее в активное состояние. Также возвращает чат айди клиента, чтобы отправить ему сообщение о том, что заявка опубликована
def accept_work_db(order_id):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"UPDATE 'order' SET status = 1 WHERE id = {order_id}")
        client_id=sql.execute(f"SELECT client FROM 'order' WHERE id = {order_id}").fetchone()[0]
        
        chat_id=sql.execute(f"SELECT chat_id FROM 'client' WHERE id = {client_id}").fetchone()[0]      
                 
        return chat_id
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close() 

#Функция удаления работы из бд, если админ отклонил ее
def reject_work_db(order_id):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        
        client_id=sql.execute(f"SELECT client FROM 'order' WHERE id = {order_id}").fetchone()[0]
        
        chat_id=sql.execute(f"SELECT chat_id FROM 'client' WHERE id = {client_id}").fetchone()[0]      
        
        sql.execute(f"DELETE FROM 'order' WHERE id ={order_id}")         
        return chat_id
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close() 


def select_worker_chat_id(username):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"SELECT chat_id FROM worker WHERE username = '{username}'")
        worker_chatid = sql.fetchone()[0]
        return worker_chatid
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close() 

def full_info_order(order_id):
    try: 
        db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
        sql=db.cursor()
        sql.execute(f"SELECT * FROM 'order' WHERE id = {order_id}")
        order_info = sql.fetchone()
        return order_info
    except sqlite3.Error as e:
        db.rollback() 
        print (e)
        return 'Упс, что то пошло не так'
    finally: 
        db.commit()
        db.close() 

print(full_info_order(1))