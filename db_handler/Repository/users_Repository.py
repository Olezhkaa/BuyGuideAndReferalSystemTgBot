import sqlite3

from config import DATABASE


def create_table_user(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id_user_tg TEXT UNIQUE, full_name TEXT, balance REAL DEFAULT 0, ref_code TEXT DEFAULT NULL, ref_by TEXT, course_purchased BOOLEAN DEFAULT FALSE)')

def insert_user(id_user_tg, full_name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    params = (id_user_tg, full_name)

    cursor.execute(
        'INSERT INTO users (id_user_tg, full_name) VALUES (?, ?)', params)

    connection.commit()
    cursor.close()
    connection.close()

def get_all_users():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users')
    users_list = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return users_list

def get_user_by_id(id_user_tg):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE id_user_tg=(?)', (str(id_user_tg), ))
    user = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return user

def the_user_exist(id_user_tg):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE id_user_tg=(?)', (str(id_user_tg),))
    user = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    if not user:
        return False
    else:
        return True

def update_user_balance_minus(id_user_tg, amount_withdrawal):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET balance = balance - ? WHERE id_user_tg = ?", (amount_withdrawal, id_user_tg))

    connection.commit()
    cursor.close()
    connection.close()

def update_user_balance_plus(id_user_tg, amount_withdrawal):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET balance = balance + ? WHERE id_user_tg = ?", (amount_withdrawal, id_user_tg))

    connection.commit()
    cursor.close()
    connection.close()

def update_user_promo(id_user_tg, promo):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET ref_code = (?) WHERE id_user_tg = ?", (promo, id_user_tg))

    connection.commit()
    cursor.close()
    connection.close()