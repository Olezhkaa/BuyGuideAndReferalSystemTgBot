import sqlite3

from config import DATABASE

def create_table_promo_codes(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS promo_codes (code TEXT PRIMARY KEY, discount REAL DEFAULT 50, owner_id TEXT)')

def insert_promo_code(code, discount, owner_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        'INSERT INTO promo_codes (code, discount, owner_id) VALUES (?, ?, ?)', (code, discount, owner_id)
    )

    connection.commit()
    cursor.close()
    connection.close()

def get_promo_by_code(code):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    promo_code = cursor.execute("SELECT * FROM promo_codes WHERE code = ?", (code,)).fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return promo_code

def get_code_by_user_id(owner_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    promo_code = cursor.execute("SELECT * FROM promo_codes WHERE owner_id = ?", (owner_id,)).fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return promo_code

def update_promo_code(user_id, promo):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("UPDATE promo_codes SET code = (?) WHERE owner_id = (?)", (promo, user_id))

    connection.commit()
    cursor.close()
    connection.close()