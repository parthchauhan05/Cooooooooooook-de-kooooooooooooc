import sqlite3

conn = sqlite3.connect('db.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS user 
(id INTEGER PRIMARY KEY, fName TEXT, lName TEXT, email TEXT, pass TEXT, cPass TExt)""")