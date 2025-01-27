import sqlite3
from config import DATABASE
from db_handler.Repository import users_Repository
from db_handler.Repository import promo_codes_Repository
from db_handler.Repository.users_Repository import insert_admin
from db_handler.Repository import  transactions_Repository


def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    create_table(cursor)
    insert_admin()

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
def get_users_ref_by(promo): return users_Repository.get_users_ref_by(promo)
def get_all_by_guide(): return  users_Repository.get_all_by_guide()
def update_user_guide_purchased_and_ref_by(user_id, ref_by): users_Repository.update_user_guide_purchased_and_ref_by(user_id, ref_by)

def create_table_promo_codes(cursor): promo_codes_Repository.create_table_promo_codes(cursor)
def insert_promo_code(code, discount, owner_id): promo_codes_Repository.insert_promo_code(code, discount, owner_id)
def get_promo_by_code(code): return promo_codes_Repository.get_promo_by_code(code)
def get_code_by_user_id(user_id): return promo_codes_Repository.get_code_by_user_id(user_id)
def update_promo_code(user_id, promo): return promo_codes_Repository.update_promo_code(user_id, promo)
def top_promo(limit): return promo_codes_Repository.top_promo(limit)

def create_table_transactions(cursor): transactions_Repository.create_table_transactions(cursor)
def insert_transaction(user_id, payment_id, amount, type_payment): transactions_Repository.insert_transaction(user_id, payment_id, amount, type_payment)

