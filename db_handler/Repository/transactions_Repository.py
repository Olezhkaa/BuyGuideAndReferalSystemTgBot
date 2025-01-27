import psycopg2
from config import HOST, USER, PASSWORD

from config import DATABASE


def create_table_transactions(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS transactions (id SERIAL PRIMARY KEY, user_id TEXT, payment_id TEXT, amount REAL, type TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

def insert_transaction(user_id, payment_id, amount, type_payment):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute("INSERT INTO transactions (user_id, payment_id, amount, type) VALUES (%s, %s, %s, %s)",
                   (str(user_id), payment_id, amount, type_payment))

    connection.commit()
    cursor.close()
    connection.commit()

