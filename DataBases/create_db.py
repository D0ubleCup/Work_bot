import sqlite3

db=sqlite3.connect('workers.db')
sql=db.cursor()
sql.execute('''CREATE TABLE "order_hour_black" (
	"id"	INTEGER NOT NULL UNIQUE,
	"client"	INTEGER,
	"title"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"adress"	TEXT,
	"count_workers"	INTEGER NOT NULL,
	"age"	INTEGER,
	"price"	INTEGER NOT NULL,
	"worker"	INTEGER,
	"message_id"	INTEGER NOT NULL,
	FOREIGN KEY("worker") REFERENCES "worker"("id"),
	FOREIGN KEY("client") REFERENCES "client"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
)''')
db.commit()
sql.close()