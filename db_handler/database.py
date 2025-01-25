import sqlite3
from config import DATABASE
from db_handler.Repository import users_Repository
from db_handler.Repository import promo_codes_Repository


def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    create_table(cursor)

    connection.commit()
    cursor.close()
    connection.close()

def create_table(cursor):
    users_Repository.create_table_user(cursor)
    create_table_transactions(cursor)
    create_table_promo_codes(cursor)

def user_exist(id_user): return users_Repository.the_user_exist(id_user)
def insert_user(id_user, full_name): users_Repository.insert_user(id_user, full_name)
def all_users(): return users_Repository.get_all_users()
def get_user_by_id(user_id): return users_Repository.get_user_by_id(user_id)
def update_user_balance_minus(id_user_tg, amount_withdrawal): users_Repository.update_user_balance_minus(id_user_tg, amount_withdrawal)
def update_user_balance_plus(id_user_tg, amount_withdrawal): users_Repository.update_user_balance_plus(id_user_tg, amount_withdrawal)
def update_user_promo(id_user_tg, promo): users_Repository.update_user_promo(id_user_tg, promo)


def create_table_transactions(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, payment_id TEXT, amount REAL, type TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')

def create_table_promo_codes(cursor): promo_codes_Repository.create_table_promo_codes(cursor)
def insert_promo_code(code, discount, owner_id): promo_codes_Repository.insert_promo_code(code, discount, owner_id)
def get_promo_by_code(code): return promo_codes_Repository.get_promo_by_code(code)
def get_code_by_user_id(user_id): return promo_codes_Repository.get_code_by_user_id(user_id)
def update_promo_code(user_id, promo): return promo_codes_Repository.update_promo_code(user_id, promo)
