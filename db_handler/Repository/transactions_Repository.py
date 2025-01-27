import sqlite3

from config import DATABASE


def create_table_transactions(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, payment_id TEXT, amount REAL, type TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')

def insert_transaction(user_id, payment_id, amount, type_payment):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO transactions (user_id, payment_id, amount, type) VALUES (?, ?, ?, ?)",
                   (user_id, payment_id, amount, type_payment))

    connection.commit()
    cursor.close()
    connection.commit()

