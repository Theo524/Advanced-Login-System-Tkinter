import sqlite3
import os

connection = sqlite3.connect(os.getcwd() + '\\database\\users.db')
cursor = connection.cursor()
with connection:
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
    (username text, password text, email text, date_of_birth text)''')
