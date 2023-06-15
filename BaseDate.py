import sqlite3
db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
sql=db.cursor()

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


def check_registration(username):
    db = None
    try: 
        db = sqlite3.connect('DataBases/workers.db')
        sql = db.cursor()

        if sql.execute(f"SELECT name FROM worker WHERE username == '{username}'"):
            return True
        
        else: 
            return False

    except sqlite3.Error as e:
        if db: db.rollback() 
        print (e)


    finally: 
        if db: db.close()



def load_username(date, username):
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

        if sql.execute(f"SELECT name FROM worker WHERE username == '{username}'"):
            return 'такой юзер уже существует'
        else:
            sql.execute(f"INSERT INTO worker (username , name , specialization, phone_number, age, rate, chat_id) VALUES('{username}', '{first_name}','{resume}','{phone}', '{age}', '{0}', '{chat_id}')")


    except sqlite3.Error as e:
        if db: db.rollback() 
        print (e)


    finally: 
        db.commit()
        if db: db.close()
def reg_client(client_info,username):
        
    username=client_info[username]['username']
    chat_id=client_info[username]['chat_id']
    phone_number=client_info[username]['phone_number']
    name=client_info[username]['name']
    try:
        if sql.execute(f"SELECT name FROM client WHERE username == '{username}'"): 
            return True
        else: #если такой записи нет  
            sql.execute(f"INSERT INTO client(name,phone_number,chat_id,username) VALUES('{name}','{phone_number}','{chat_id}','{username}')")
            db.commit()
            sql.close()
            return False
    except sqlite3.Error as e: 
        if db: db.rollback()  
        print (e) 
 
 
    finally:  
        if db: db.close()
