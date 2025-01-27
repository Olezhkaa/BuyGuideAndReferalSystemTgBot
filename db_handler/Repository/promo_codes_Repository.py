import psycopg2
from config import HOST, USER, PASSWORD

from config import DATABASE

def create_table_promo_codes(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS promo_codes (code TEXT PRIMARY KEY, discount REAL DEFAULT 50, owner_id TEXT)')

def insert_promo_code(code, discount, owner_id):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute(
        'INSERT INTO promo_codes (code, discount, owner_id) VALUES (%s, %s, %s)', (str(code), discount, str(owner_id))
    )

    connection.commit()
    cursor.close()
    connection.close()

def get_promo_by_code(code):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM promo_codes WHERE code = %s", (str(code),))
    promo_code = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return promo_code

def get_code_by_user_id(owner_id):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM promo_codes WHERE owner_id = %s", (str(owner_id),))
    promo_code =cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return promo_code

def update_promo_code(user_id, promo):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute("UPDATE promo_codes SET code = (%s) WHERE owner_id = (%s)", (str(promo), str(user_id)))

    connection.commit()
    cursor.close()
    connection.close()

def top_promo(limit):
    connection = psycopg2.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD )
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 
        pc.code AS promo_code,
        COUNT(u.id_user_tg) AS users_count
    FROM 
        promo_codes pc
    LEFT JOIN 
        users u ON pc.owner_id = u.ref_by
    GROUP BY 
        pc.code
    ORDER BY 
        users_count DESC
    LIMIT %s;
    """, (limit, ))

    list_promo = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return list_promo