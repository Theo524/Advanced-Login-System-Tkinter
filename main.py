import os
import sqlite3
from widgets.start import StartApp


if __name__ == "__main__":
    # create database
    conn = sqlite3.connect(os.getcwd() + '\\database\\users.db')
    c = conn.cursor()
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS users
        (username text, password text, email text, date_of_birth text)''')

    # LOGIN APPLICATION
    app = StartApp()