'''тут мы работаем с бд'''

import sqlite3
db=sqlite3.connect('DataBases/workers.db',check_same_thread=False)
sql=db.cursor()

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