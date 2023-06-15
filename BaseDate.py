import sqlite3
db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
sql=db.cursor()
db.row_factory=sqlite3.Row
# вставлять везде этот обработчик ошибок
# db = None
# try: 
#     db = sqlite3.connect('DataBases/workers.db')
#     sql = db.cursor()

# except sqlite3.Error as e:
#     if db: db.rollback() 
#     print (e)


# finally: 
#     if db: db.close()

#функция проверки зарегистрирован ли ползователь
def check_registration(username):
    db = None
    try: 
        from_worker = sql.execute(f"SELECT name FROM worker WHERE username == '{username}'")
        from_client = sql.execute(f"SELECT name FROM client WHERE username == '{username}'")
        if from_worker or from_client:
            return True
        else: 
            return False

    except sqlite3.Error as e:
        if db: db.rollback() 
        print (e)


    finally: 
        if db: db.close()



def load_worker(date, username):
    db = None

    worker_information = date[username]
    username = worker_information['username'].replace(' ', '_')
    first_name = worker_information['first_name'].replace(' ', '_')
    last_name = worker_information['last_name'].replace(' ', '_')
    resume = worker_information['resume'].replace(' ', '_')
    phone = worker_information['phone'].replace(' ', '_')
    age = worker_information['age']
    chat_id = worker_information['chat_id']

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
        if sql.execute(f"SELECT name FROM client WHERE username == '{username}'"): 
            return True
        else: #если такой записи нет  
            sql.execute(f"INSERT INTO client(name,phone_number,chat_id,username) VALUES('{name}','{phone_number}','{chat_id}','{username}')")
            sql.execute(f"UPDATE main_info SET client_count = client_count + 1")
            
            return False
    except sqlite3.Error as e: 
        if db: db.rollback()  
        print (e) 
 
 
    finally:  
        db.commit()
        if db: db.close()



def check_role(username):
    sql.execute(f"SELECT 'worker' as source, username FROM worker WHERE username='{username}' UNION ALL SELECT 'client' as source, username FROM client WHERE username='{username}'")
    rows = sql.fetchone()
    return rows[0]
