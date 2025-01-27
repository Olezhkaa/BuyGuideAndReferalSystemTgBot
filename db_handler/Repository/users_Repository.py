import psycopg2
from config import HOST, USER, PASSWORD
from config import DATABASE
from db_handler.Repository.promo_codes_Repository import get_promo_by_code


def create_table_user(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id_user_tg TEXT UNIQUE, full_name TEXT, balance REAL DEFAULT 0, ref_code TEXT DEFAULT NULL, ref_by TEXT, guide_purchased BOOLEAN DEFAULT FALSE)')

def insert_user(id_user_tg, full_name):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    params = (str(id_user_tg), full_name)

    cursor.execute(
        'INSERT INTO users (id_user_tg, full_name) VALUES (%s, %s)', params)

    connection.commit()
    cursor.close()
    connection.close()

def get_all_users():
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users')
    users_list = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return users_list

def get_user_by_id(id_user_tg):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE id_user_tg=%s', (str(id_user_tg), ))
    user = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return user

def the_user_exist(id_user_tg):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE id_user_tg=%s', (str(id_user_tg),))
    user = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    if not user:
        return False
    else:
        return True

def get_users_ref_by(promo):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    ref_by = get_promo_by_code(promo)[2]

    cursor.execute('SELECT * FROM users WHERE ref_by=%s', (str(ref_by), ))
    users_list = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return users_list


def update_user_balance_minus(id_user_tg, amount_withdrawal):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET balance = balance - %s WHERE id_user_tg = %s", (amount_withdrawal, str(id_user_tg)))

    connection.commit()
    cursor.close()
    connection.close()

def update_user_balance_plus(id_user_tg, amount_withdrawal):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET balance = balance + %s WHERE id_user_tg = %s", (amount_withdrawal, str(id_user_tg)))

    connection.commit()
    cursor.close()
    connection.close()

def update_user_promo(id_user_tg, promo):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET ref_code = %s WHERE id_user_tg = %s", (promo, str(id_user_tg)))

    connection.commit()
    cursor.close()
    connection.close()

def update_user_guide_purchased_and_ref_by(user_id, ref_by):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET guide_purchased = TRUE, ref_by = %s WHERE id_user_tg = %s", (ref_by, str(user_id)))

    connection.commit()
    cursor.close()
    connection.close()

def insert_admin():
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    if get_user_by_id('0001') is None:
        cursor.execute(
            'INSERT INTO users (id_user_tg, full_name) VALUES (%s, %s)', ('0001', 'Admin'))

    connection.commit()
    cursor.close()
    connection.close()

def get_all_by_guide():
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute(
            'SELECT * FROM users WHERE guide_purchased=%s', (True, ))
    list_users = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return list_users